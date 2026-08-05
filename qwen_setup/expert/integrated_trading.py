#!/usr/bin/env python3
"""
Integrated Trading System
Unifies all agents: TradingOrchestrator, GodelMachine, EnsembleTrader

This is the master orchestrator that coordinates:
- Data acquisition (ZeroCostScraper)
- Basic LLM inference (QwenClient)
- Ensemble consensus (EnsembleTrader)
- Meta-cognitive analysis (GodelMachine)
- Incompleteness detection
- Self-improvement

Usage:
    python integrated_trading.py --symbol BTCUSDT --mode godel
    python integrated_trading.py --symbol ETHUSDT --mode ensemble
    python integrated_trading.py --continuous --mode full
"""

import json
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Core components
from scraper_config import ZeroCostScraper
from prompt_compression import TradingPromptCompressor

try:
    from client import QwenClient
    test_client = QwenClient()
    if not test_client.health_check():
        from mock_client import MockQwenClient as QwenClient
except Exception:
    from mock_client import MockQwenClient as QwenClient

# Agent imports
from ensemble_trading import EnsembleTrader
from godel_machine import GodelMachine, GodelDecision
from prediction_tracker import PredictionTracker


class TradingMode(Enum):
    """Trading modes with different agent combinations"""
    BASIC = "basic"           # Just LLM + data
    ENSEMBLE = "ensemble"     # Add consensus voting
    GODEL = "godel"           # Add meta-cognitive analysis
    FULL = "full"             # All agents integrated


@dataclass
class IntegratedDecision:
    """Unified decision from all agents"""
    timestamp: datetime
    symbol: str
    price: float

    # Basic decision
    action: str
    confidence: float
    reason: str

    # Ensemble data (if enabled)
    ensemble_consensus: Optional[str] = None
    ensemble_votes: Optional[int] = None
    ensemble_agreement: Optional[float] = None

    # Godel data (if enabled)
    meta_confidence: Optional[float] = None
    incompleteness_detected: bool = False
    incompleteness_type: Optional[str] = None
    strange_loop_active: bool = False
    godel_number: Optional[int] = None
    philosophical_note: Optional[str] = None

    # Integrated metrics
    mode_used: str = "basic"
    latency_ms: float = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "price": self.price,
            "action": self.action,
            "confidence": round(self.confidence, 4),
            "reason": self.reason,
            "ensemble": {
                "consensus": self.ensemble_consensus,
                "votes": self.ensemble_votes,
                "agreement": self.ensemble_agreement
            } if self.ensemble_consensus else None,
            "godel": {
                "meta_confidence": self.meta_confidence,
                "incompleteness_detected": self.incompleteness_detected,
                "incompleteness_type": self.incompleteness_type,
                "strange_loop": self.strange_loop_active,
                "godel_number": self.godel_number,
                "philosophical_note": self.philosophical_note
            } if self.meta_confidence is not None else None,
            "mode": self.mode_used,
            "latency_ms": round(self.latency_ms, 2)
        }


class IntegratedTradingSystem:
    """
    Master orchestrator that unifies all trading agents.

    Combines:
    - ZeroCostScraper: Free data acquisition
    - QwenClient: Local LLM inference
    - EnsembleTrader: Multi-perspective consensus
    - GodelMachine: Meta-cognitive self-referential analysis

    The system can operate in different modes:
    - BASIC: Simple LLM analysis
    - ENSEMBLE: Add consensus voting for better accuracy
    - GODEL: Add incompleteness detection and meta-prediction
    - FULL: All agents working together
    """

    VERSION = "3.1.0-verified"

    def __init__(
        self,
        mode: TradingMode = TradingMode.FULL,
        config_path: str = "./trading_config.json",
        enable_self_improvement: bool = True
    ):
        self.mode = mode

        # Load config
        if Path(config_path).exists():
            self.config = json.loads(Path(config_path).read_text())
        else:
            self.config = {
                "paper_trading": True,
                "symbols": ["BTCUSDT", "ETHUSDT"],
                "interval": "1h",
                "max_position_size": 1000,
                "stop_loss_pct": 2.0,
                "mode": mode.value
            }

        # Initialize core components
        self.scraper = ZeroCostScraper()
        self.compressor = TradingPromptCompressor()
        self.llm = QwenClient()

        # Initialize agents based on mode
        self.ensemble: Optional[EnsembleTrader] = None
        self.godel: Optional[GodelMachine] = None

        if mode in [TradingMode.ENSEMBLE, TradingMode.FULL]:
            self.ensemble = EnsembleTrader(self.llm, num_models=5)
            print(f"[AGENT] EnsembleTrader initialized (5 perspectives)")

        if mode in [TradingMode.GODEL, TradingMode.FULL]:
            self.godel = GodelMachine(
                name="IntegratedGodelMachine",
                enable_self_improvement=enable_self_improvement,
                max_meta_depth=3,
                incompleteness_sensitivity=0.7
            )
            print(f"[AGENT] GodelMachine initialized (meta-cognitive)")

        # State tracking
        self.decision_history: List[IntegratedDecision] = []
        self.state = {
            "positions": {},
            "trades_history": [],
            "last_analysis": None
        }

        # Performance metrics
        self.perf = {
            "total_queries": 0,
            "avg_latency_ms": 0,
            "abstentions": 0,
            "ensemble_agreements": 0,
            "godel_loops_detected": 0
        }

        # Closed-loop prediction verification (measured hit rate, not theater)
        self.tracker = PredictionTracker(
            path=Path("prediction_ledger.jsonl"),
            horizon_s=float(self.config.get("prediction_horizon_s", 300)),
            deadband_pct=float(self.config.get("prediction_deadband_pct", 0.05)),
        )

        print(f"\n{'='*60}")
        print(f"INTEGRATED TRADING SYSTEM v{self.VERSION}")
        print(f"Mode: {mode.value.upper()}")
        print(f"Agents: {self._get_active_agents()}")
        print(f"Prediction ledger: {self.tracker.path}")
        print(f"{'='*60}\n")

    def _get_active_agents(self) -> str:
        agents = ["Scraper", "Compressor", "LLM"]
        if self.ensemble:
            agents.append("Ensemble")
        if self.godel:
            agents.append("Godel")
        return " + ".join(agents)

    def analyze(self, symbol: str, interval: str = "1h") -> IntegratedDecision:
        """
        Run full integrated analysis pipeline.

        Flow:
        1. Fetch data (Scraper)
        2. Compress for context (Compressor)
        3. Basic LLM analysis
        4. [ENSEMBLE] Multi-perspective consensus
        5. [GODEL] Meta-cognitive analysis + incompleteness detection
        6. Synthesize final decision
        """
        start_time = time.time()

        print(f"\n{'='*60}")
        print(f"INTEGRATED ANALYSIS: {symbol} @ {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")

        # Step 1: Data acquisition
        print("\n[1/5] Data Acquisition...")
        raw_data = self.scraper.get_crypto_ohlcv(symbol, interval)

        if not raw_data:
            return self._create_error_decision(symbol, "Failed to fetch data")

        print(f"      Retrieved {len(raw_data)} candles")

        # Step 2: Compression
        print("[2/5] Data Compression...")
        compressed = self.compressor.compress_ohlcv(raw_data)
        indicators = self.compressor.extract_key_indicators(raw_data)
        price = indicators.get('current_price', 0)

        print(f"      Price: ${price:,.2f} | 24h: {indicators.get('price_change_pct', 0):+.2f}%")

        # Step 3: Basic LLM analysis
        print("[3/5] Basic LLM Analysis...")
        basic_decision = self._basic_analysis(symbol, compressed, indicators)

        print(f"      Basic: {basic_decision['action'].upper()} ({basic_decision.get('confidence', 0)}/10)")

        # Step 4: Ensemble (if enabled)
        ensemble_result = None
        if self.ensemble:
            print("[4/5] Ensemble Consensus...")
            data_str = " ".join([f"c:{c['c']:.0f} v:{c['v']:.0f}" for c in compressed[-5:]])
            ensemble_result = self.ensemble.ensemble_predict(symbol, data_str)

            votes = f"{ensemble_result['consensus_votes']}/{ensemble_result['total_models']}"
            print(f"      Ensemble: {ensemble_result['consensus_action'].upper()} ({votes} votes)")

            if ensemble_result['diversity_score'] == 1:
                self.perf['ensemble_agreements'] += 1
        else:
            print("[4/5] Ensemble: SKIPPED (not enabled)")

        # Step 5: Godel analysis (if enabled)
        godel_decision = None
        if self.godel:
            print("[5/5] Godel Meta-Cognitive Analysis...")

            # Prepare market data for Godel
            market_data = {
                "price": price,
                "prev_price": indicators.get('prev_price', price),
                "volume": indicators.get('volume', 0),
                "rsi": indicators.get('rsi', 50),
                "macd": indicators.get('macd', 0),
                "momentum": indicators.get('momentum', 0),
                "trend": 1 if price > indicators.get('sma_20', price) else -1,
                "volatility": indicators.get('volatility'),
                "sentiment": None  # Could integrate sentiment source
            }

            godel_decision = self.godel.process_market_state(market_data)

            status = "INCOMPLETENESS" if godel_decision.incompleteness_detected else "OK"
            loop = " (strange loop)" if godel_decision.strange_loop_active else ""
            print(f"      Godel: {godel_decision.action.upper()} | Meta: {godel_decision.meta_confidence:.0%} | {status}{loop}")

            if godel_decision.strange_loop_active:
                self.perf['godel_loops_detected'] += 1
            if godel_decision.action == "abstain":
                self.perf['abstentions'] += 1
        else:
            print("[5/5] Godel: SKIPPED (not enabled)")

        # Synthesize final decision
        final_decision = self._synthesize_decision(
            symbol=symbol,
            price=price,
            basic=basic_decision,
            ensemble=ensemble_result,
            godel=godel_decision,
            start_time=start_time
        )

        # Record and return
        self.decision_history.append(final_decision)
        self.perf['total_queries'] += 1

        # Resolve any matured prior calls using current prices, then record this call
        resolved = self.tracker.resolve({symbol: price, symbol.replace("USDT", ""): price})
        if resolved:
            n_hit = sum(1 for p in resolved if p.hit is True)
            n_miss = sum(1 for p in resolved if p.hit is False)
            print(f"      Verified {len(resolved)} call(s): {n_hit} hit / {n_miss} miss")

        if final_decision.action.lower() in ("buy", "sell") and price > 0:
            self.tracker.record(
                symbol=symbol,
                side=final_decision.action.lower(),
                price=price,
                confidence=final_decision.confidence,
                reason=final_decision.reason or "",
            )

        latency = (time.time() - start_time) * 1000
        self.perf['avg_latency_ms'] = (
            (self.perf['avg_latency_ms'] * (self.perf['total_queries'] - 1) + latency) /
            self.perf['total_queries']
        )

        verified = self.tracker.summary()
        print(f"\n{'─'*60}")
        print(f"FINAL DECISION: {final_decision.action.upper()}")
        print(f"Confidence: {final_decision.confidence:.0%} | Latency: {latency:.0f}ms")
        print(f"Verified accuracy: {verified['badge']}")
        if final_decision.philosophical_note:
            print(f"Note: {final_decision.philosophical_note[:80]}...")
        print(f"{'─'*60}")

        return final_decision

    def _basic_analysis(
        self,
        symbol: str,
        compressed: List[Dict],
        indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Basic LLM analysis (same as TradingOrchestrator)"""

        # Few-shot prompt
        current = " ".join([f"c:{c['c']:.0f} v:{c['v']:.0f}" for c in compressed[-5:]])

        sma_20 = indicators.get('sma_20', 0)
        price = indicators.get('current_price', 0)
        trend = "bullish" if price > sma_20 else "bearish"

        prompt = f"""You are a trading bot. Analyze:
Symbol: {symbol}
Trend: {trend}
Recent: {current}

Examples:
Q: BTC c:45000 v:1.2B | A: {{"action": "hold", "confidence": 3}}
Q: BTC c:40000 v:2.5B c:41000 v:3.1B | A: {{"action": "buy", "confidence": 7}}

Q: {symbol} {current}
A:"""

        response = self.llm.complete(prompt, max_tokens=100)

        # Parse response
        try:
            if "{" in response:
                json_str = response[response.find("{"):response.rfind("}")+1]
                return json.loads(json_str)
        except:
            pass

        # Fallback parsing
        output = response.lower()
        if "buy" in output:
            return {"action": "buy", "confidence": 5, "reason": response[:100]}
        elif "sell" in output:
            return {"action": "sell", "confidence": 5, "reason": response[:100]}

        return {"action": "hold", "confidence": 2, "reason": "unclear signal"}

    def _synthesize_decision(
        self,
        symbol: str,
        price: float,
        basic: Dict[str, Any],
        ensemble: Optional[Dict[str, Any]],
        godel: Optional[GodelDecision],
        start_time: float
    ) -> IntegratedDecision:
        """
        Synthesize final decision from all agent outputs.

        Priority:
        1. If Godel detects incompleteness -> ABSTAIN
        2. If all agents agree -> HIGH confidence
        3. If disagreement -> Use Godel meta-confidence
        4. Fallback to ensemble consensus
        """

        latency = (time.time() - start_time) * 1000

        # Start with basic
        action = basic['action']
        confidence = basic.get('confidence', 5) / 10
        reason = basic.get('reason', '')

        # Godel override for incompleteness
        if godel and godel.action == "abstain":
            return IntegratedDecision(
                timestamp=datetime.now(),
                symbol=symbol,
                price=price,
                action="abstain",
                confidence=0.0,
                reason=godel.reasoning,
                meta_confidence=godel.meta_confidence,
                incompleteness_detected=True,
                incompleteness_type=godel.incompleteness_type.name if godel.incompleteness_type else None,
                philosophical_note=godel.philosophical_note,
                mode_used=self.mode.value,
                latency_ms=latency
            )

        # Check agreement between agents
        actions = [basic['action']]
        if ensemble:
            actions.append(ensemble['consensus_action'])
        if godel:
            actions.append(godel.action)

        # Perfect agreement boosts confidence
        if len(set(actions)) == 1:
            confidence = min(0.95, confidence * 1.3)
            reason = f"All agents agree: {action}"

        # Ensemble consensus can override
        if ensemble and ensemble['consensus_votes'] >= 4:  # 4/5 or 5/5 agreement
            action = ensemble['consensus_action']
            confidence = ensemble['avg_confidence'] / 10

        # Godel meta-confidence adjusts final confidence
        if godel:
            # Weight by meta-confidence
            confidence = (confidence + godel.meta_confidence) / 2

            if godel.strange_loop_active:
                confidence *= 0.8  # Reduce confidence on strange loops

        return IntegratedDecision(
            timestamp=datetime.now(),
            symbol=symbol,
            price=price,
            action=action,
            confidence=confidence,
            reason=reason,
            ensemble_consensus=ensemble['consensus_action'] if ensemble else None,
            ensemble_votes=ensemble['consensus_votes'] if ensemble else None,
            ensemble_agreement=1 - (ensemble['diversity_score'] / 3) if ensemble else None,
            meta_confidence=godel.meta_confidence if godel else None,
            incompleteness_detected=godel.incompleteness_detected if godel else False,
            incompleteness_type=godel.incompleteness_type.name if godel and godel.incompleteness_type else None,
            strange_loop_active=godel.strange_loop_active if godel else False,
            godel_number=godel.godel_number if godel else None,
            philosophical_note=godel.philosophical_note if godel else None,
            mode_used=self.mode.value,
            latency_ms=latency
        )

    def _create_error_decision(self, symbol: str, error: str) -> IntegratedDecision:
        """Create error decision"""
        return IntegratedDecision(
            timestamp=datetime.now(),
            symbol=symbol,
            price=0,
            action="hold",
            confidence=0,
            reason=f"ERROR: {error}",
            mode_used=self.mode.value,
            latency_ms=0
        )

    def execute_paper_trade(self, decision: IntegratedDecision):
        """Execute paper trade"""
        if decision.action in ['hold', 'abstain']:
            print(f"   No trade: {decision.action.upper()}")
            return

        trade = {
            "symbol": decision.symbol,
            "action": decision.action,
            "timestamp": decision.timestamp.isoformat(),
            "confidence": decision.confidence,
            "price": decision.price,
            "mode": decision.mode_used,
            "godel_number": decision.godel_number
        }

        self.state['trades_history'].append(trade)

        # Log to file
        log_file = Path("integrated_trades.jsonl")
        with log_file.open("a") as f:
            f.write(json.dumps(trade) + "\n")

        print(f"   PAPER TRADE: {trade['action'].upper()} {decision.symbol} @ ${decision.price:,.2f}")

    def run_continuous(self, interval_seconds: int = 300):
        """Run continuous trading loop"""
        print(f"\n{'#'*60}")
        print("INTEGRATED TRADING SYSTEM - CONTINUOUS MODE")
        print(f"{'#'*60}")
        print(f"Mode: {self.mode.value.upper()}")
        print(f"Symbols: {self.config.get('symbols', [])}")
        print(f"Interval: {interval_seconds}s")
        print(f"Press Ctrl+C to stop\n")

        iteration = 0
        while True:
            try:
                iteration += 1
                print(f"\n{'#'*60}")
                print(f"Iteration #{iteration} @ {datetime.now()}")

                for symbol in self.config.get('symbols', ['BTCUSDT']):
                    decision = self.analyze(symbol)

                    if self.config.get('paper_trading', True):
                        self.execute_paper_trade(decision)

                    time.sleep(2)

                print(f"\nSleeping {interval_seconds}s...")
                time.sleep(interval_seconds)

            except KeyboardInterrupt:
                print("\n\nStopped by user")
                self.print_summary()
                break
            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(60)

    def print_summary(self):
        """Print trading summary"""
        print(f"\n{'='*60}")
        print("INTEGRATED TRADING SUMMARY")
        print(f"{'='*60}")
        print(f"Mode: {self.mode.value.upper()}")
        print(f"Total Queries: {self.perf['total_queries']}")
        print(f"Avg Latency: {self.perf['avg_latency_ms']:.0f}ms")
        print(f"Abstentions (Incompleteness): {self.perf['abstentions']}")
        print(f"Ensemble Perfect Agreements: {self.perf['ensemble_agreements']}")
        print(f"Strange Loops Detected: {self.perf['godel_loops_detected']}")

        verified = self.tracker.summary()
        print(f"\nVerified predictions (closed loop):")
        print(f"  Badge: {verified['badge']}")
        print(f"  Graded: {verified['graded']}  Hits: {verified['hits']}  Misses: {verified['misses']}")
        print(f"  Pending: {verified['pending']}  Dropped: {verified['dropped']}")
        if verified.get("avg_confidence_hits") is not None:
            print(
                f"  Avg conf hits: {verified['avg_confidence_hits']:.2f}  "
                f"misses: {verified.get('avg_confidence_misses')}"
            )

        if self.godel:
            print(f"\nGodel Machine Status:")
            state = self.godel.get_machine_state()
            print(f"  Self-Improvements: {state['self_improvements']}")
            print(f"  Paradoxes: {state['paradoxes_encountered']}")

    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "version": self.VERSION,
            "mode": self.mode.value,
            "active_agents": self._get_active_agents(),
            "performance": self.perf,
            "decisions": len(self.decision_history),
            "godel_state": self.godel.get_machine_state() if self.godel else None
        }


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Integrated Trading System")
    parser.add_argument("--symbol", default="BTCUSDT", help="Trading symbol")
    parser.add_argument("--interval", default="1h", help="Candle interval")
    parser.add_argument("--mode", default="full",
                        choices=["basic", "ensemble", "godel", "full"],
                        help="Trading mode")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--sleep", type=int, default=300, help="Sleep between iterations")

    args = parser.parse_args()

    # Create system
    mode = TradingMode(args.mode)
    system = IntegratedTradingSystem(mode=mode)

    if args.continuous:
        system.run_continuous(interval_seconds=args.sleep)
    else:
        # Single analysis
        decision = system.analyze(args.symbol, args.interval)
        print(f"\n{json.dumps(decision.to_dict(), indent=2)}")
