#!/usr/bin/env python3
"""
Prediction Tracker — closed-loop verification for trading signals.

Records directional buy/sell calls, resolves them against realized price
moves after a fixed horizon, and reports measured hit rate.

No self-reported accuracy formulas. No randomness.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Prediction:
    id: str
    symbol: str
    side: str  # buy | sell
    price: float
    confidence: float
    t_open: float
    horizon_s: float
    reason: str = ""
    resolved: bool = False
    t_close: Optional[float] = None
    exit_price: Optional[float] = None
    ret_pct: Optional[float] = None
    hit: Optional[bool] = None
    dropped: bool = False  # too stale / invalid to score
    drop_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Prediction":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__ if k in d})


class PredictionTracker:
    """
    Server-side ledger for directional calls.

    Scoring rule (default):
      - Horizon: 300s (5 minutes)
      - Deadband: ±0.05% — moves inside deadband count as neither hit nor miss
        (recorded as resolved with hit=None)
      - Max age: 3× horizon — if still unresolved past max age when resolve()
        is called without a price, the call is dropped (not graded late)
    """

    def __init__(
        self,
        path: str | Path = "prediction_ledger.jsonl",
        horizon_s: float = 300.0,
        deadband_pct: float = 0.05,
        max_age_mult: float = 3.0,
    ):
        self.path = Path(path)
        self.horizon_s = horizon_s
        self.deadband_pct = deadband_pct
        self.max_age_s = horizon_s * max_age_mult
        self.predictions: List[Prediction] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                self.predictions.append(Prediction.from_dict(json.loads(line)))
            except Exception:
                continue

    def _append(self, pred: Prediction) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(pred.to_dict()) + "\n")

    def _rewrite(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            for p in self.predictions:
                f.write(json.dumps(p.to_dict()) + "\n")

    def record(
        self,
        symbol: str,
        side: str,
        price: float,
        confidence: float,
        reason: str = "",
        t: Optional[float] = None,
    ) -> Optional[Prediction]:
        """Record a directional call. Holds/abstains are ignored."""
        side = (side or "").lower().strip()
        if side not in ("buy", "sell"):
            return None
        if price is None or price <= 0:
            return None
        pred = Prediction(
            id=uuid.uuid4().hex[:12],
            symbol=symbol.upper(),
            side=side,
            price=float(price),
            confidence=float(confidence or 0.0),
            t_open=float(t if t is not None else time.time()),
            horizon_s=self.horizon_s,
            reason=(reason or "")[:200],
        )
        self.predictions.append(pred)
        self._append(pred)
        return pred

    def resolve(
        self,
        prices: Dict[str, float],
        now: Optional[float] = None,
    ) -> List[Prediction]:
        """
        Score matured open predictions using current prices.

        prices: map symbol -> last price
        Returns list of newly resolved (or dropped) predictions.
        """
        now = float(now if now is not None else time.time())
        changed: List[Prediction] = []
        dirty = False

        for p in self.predictions:
            if p.resolved or p.dropped:
                continue
            age = now - p.t_open
            px = prices.get(p.symbol) or prices.get(p.symbol.replace("USDT", ""))
            # try a few key shapes
            if px is None:
                for k, v in prices.items():
                    if k.upper().startswith(p.symbol[:3]):
                        px = v
                        break

            if age < p.horizon_s:
                continue

            if px is None or px <= 0:
                if age > self.max_age_s:
                    p.dropped = True
                    p.resolved = True
                    p.drop_reason = "stale_no_price"
                    p.t_close = now
                    changed.append(p)
                    dirty = True
                continue

            if age > self.max_age_s:
                # too late to grade fairly
                p.dropped = True
                p.resolved = True
                p.drop_reason = "stale"
                p.t_close = now
                p.exit_price = float(px)
                changed.append(p)
                dirty = True
                continue

            ret = (float(px) / p.price - 1.0) * 100.0
            p.ret_pct = ret
            p.exit_price = float(px)
            p.t_close = now
            p.resolved = True

            if abs(ret) < self.deadband_pct:
                p.hit = None  # flat — not scored as win/loss
            elif p.side == "buy":
                p.hit = ret > 0
            else:
                p.hit = ret < 0

            changed.append(p)
            dirty = True

        if dirty:
            self._rewrite()
        return changed

    def summary(self) -> Dict[str, Any]:
        graded = [p for p in self.predictions if p.resolved and not p.dropped and p.hit is not None]
        pending = [p for p in self.predictions if not p.resolved and not p.dropped]
        dropped = [p for p in self.predictions if p.dropped]
        hits = [p for p in graded if p.hit is True]
        misses = [p for p in graded if p.hit is False]
        n = len(graded)
        hit_rate = (len(hits) / n) if n else None
        conf_hit = (
            sum(p.confidence for p in hits) / len(hits) if hits else None
        )
        conf_miss = (
            sum(p.confidence for p in misses) / len(misses) if misses else None
        )
        return {
            "total_recorded": len(self.predictions),
            "pending": len(pending),
            "dropped": len(dropped),
            "graded": n,
            "hits": len(hits),
            "misses": len(misses),
            "hit_rate": hit_rate,
            "hit_rate_pct": (hit_rate * 100.0) if hit_rate is not None else None,
            "avg_confidence_hits": conf_hit,
            "avg_confidence_misses": conf_miss,
            "horizon_s": self.horizon_s,
            "deadband_pct": self.deadband_pct,
            "min_samples_for_badge": 10,
            "badge": (
                f"{hit_rate * 100:.0f}% hit (n={n})"
                if hit_rate is not None and n >= 10
                else "measuring"
            ),
        }


def _self_test() -> None:
    """Deterministic self-test — no network."""
    import tempfile

    tmp = Path(tempfile.mkdtemp()) / "ledger.jsonl"
    tr = PredictionTracker(path=tmp, horizon_s=10.0, deadband_pct=0.05)

    t0 = 1_000_000.0
    tr.record("BTCUSDT", "buy", 100.0, 0.8, t=t0)
    tr.record("BTCUSDT", "sell", 100.0, 0.7, t=t0)
    tr.record("ETHUSDT", "buy", 50.0, 0.6, t=t0)
    tr.record("ETHUSDT", "hold", 50.0, 0.9, t=t0)  # ignored

    assert len(tr.predictions) == 3

    # Too early
    out = tr.resolve({"BTCUSDT": 101.0, "ETHUSDT": 49.0}, now=t0 + 5)
    assert out == []

    # Mature — buy BTC wins, sell BTC loses, buy ETH loses
    out = tr.resolve({"BTCUSDT": 101.0, "ETHUSDT": 49.0}, now=t0 + 11)
    assert len(out) == 3
    hits = {p.symbol + p.side: p.hit for p in out}
    assert hits["BTCUSDTbuy"] is True
    assert hits["BTCUSDTsell"] is False
    assert hits["ETHUSDTbuy"] is False

    s = tr.summary()
    assert s["graded"] == 3
    assert s["hits"] == 1
    assert abs(s["hit_rate"] - 1 / 3) < 1e-9
    assert s["badge"] == "measuring"  # n < 10

    # Deadband
    tr2 = PredictionTracker(path=tmp.with_suffix(".2.jsonl"), horizon_s=10.0)
    tr2.record("X", "buy", 100.0, 0.5, t=t0)
    tr2.resolve({"X": 100.02}, now=t0 + 11)  # +0.02% < 0.05%
    g = [p for p in tr2.predictions if p.resolved]
    assert g[0].hit is None

    # Stale drop
    tr3 = PredictionTracker(path=tmp.with_suffix(".3.jsonl"), horizon_s=10.0)
    tr3.record("Y", "buy", 10.0, 0.5, t=t0)
    tr3.resolve({}, now=t0 + 100)
    assert tr3.predictions[0].dropped is True

    print("prediction_tracker self-test: PASS")
    print(json.dumps(s, indent=2))


if __name__ == "__main__":
    _self_test()
