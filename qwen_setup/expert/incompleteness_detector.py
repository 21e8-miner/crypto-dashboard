"""
INCOMPLETENESS DETECTOR: Finding the Unknowable

Gödel's First Incompleteness Theorem states that any consistent formal system
powerful enough to express arithmetic contains statements that are TRUE but
UNPROVABLE within the system.

In markets, this translates to: There exist market states that are:
1. Genuinely predictable (truth exists)
2. But unprovable with ANY strategy (no proof possible)

This module detects these GÖDELIAN MARKET STATES - situations where:
- Historical patterns don't apply (novel situations)
- All indicators contradict each other (undecidable)
- The market is in a superposition of states (quantum-like)
- The act of prediction changes the outcome (observer effect)
- Information is fundamentally incomplete (unknown unknowns)

The profound insight: KNOWING you can't know is itself valuable knowledge.
When incompleteness is detected, the appropriate response is EPISTEMIC HUMILITY.

"The only true wisdom is knowing you know nothing." - Socrates
"There are more things in heaven and earth than are dreamt of in your
 philosophy." - Shakespeare
"Incompleteness means the market can always surprise us." - This System
"""

import math
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import Counter
from enum import Enum
import statistics


class IncompletenessType(Enum):
    """Types of incompleteness we can detect"""
    NONE = 0                    # No incompleteness detected
    INDICATOR_CONTRADICTION = 1  # Indicators disagree fundamentally
    HISTORICAL_NOVELTY = 2      # No similar historical pattern
    SELF_REFERENCE_PARADOX = 3  # Market predicting itself
    INFORMATION_GAP = 4         # Known unknown information
    REGIME_SUPERPOSITION = 5    # Multiple regimes simultaneously
    OBSERVER_EFFECT = 6         # Our prediction changes the market
    COMPLEXITY_LIMIT = 7        # Too complex for any model


@dataclass
class IncompletenessReport:
    """A report on detected incompleteness"""
    timestamp: datetime
    incompleteness_type: IncompletenessType
    confidence: float  # How confident are we that this is unknowable?
    evidence: List[str]
    recommendation: str
    philosophical_note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "type": self.incompleteness_type.name,
            "confidence": round(self.confidence, 4),
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "philosophical_note": self.philosophical_note
        }


@dataclass
class MarketState:
    """Representation of a market state for analysis"""
    timestamp: datetime
    price: float
    volume: float
    indicators: Dict[str, float]  # RSI, MACD, etc.
    sentiment: Optional[float] = None
    volatility: Optional[float] = None
    regime: Optional[str] = None  # bull, bear, sideways

    def to_vector(self) -> List[float]:
        """Convert to numerical vector for similarity comparison"""
        base = [self.price, self.volume]
        ind = list(self.indicators.values())
        opt = [
            self.sentiment if self.sentiment is not None else 0.5,
            self.volatility if self.volatility is not None else 0.1
        ]
        return base + ind + opt


class IncompletenessDetector:
    """
    The Incompleteness Detector: Finding what cannot be known.

    Core Detection Methods:

    1. INDICATOR CONTRADICTION DETECTION
       When RSI says overbought but MACD shows bullish momentum,
       we have a Gödelian state - both indicators are "correct"
       in their own system but incompatible together.

    2. HISTORICAL NOVELTY DETECTION
       Novel market states have no historical parallel.
       Like a mathematical statement that can't be derived from axioms,
       these states can't be predicted from past patterns.

    3. SELF-REFERENCE PARADOX DETECTION
       When market participants are predicting each other's predictions,
       a strange loop emerges. The market is trying to prove itself.

    4. INFORMATION GAP DETECTION
       Known unknowns (we know we don't know) represent incompleteness.
       There's information that would determine the outcome, but we can't access it.

    5. REGIME SUPERPOSITION DETECTION
       Sometimes markets exist in multiple regimes simultaneously -
       like Schrödinger's cat, the regime is undefined until observed.

    6. OBSERVER EFFECT DETECTION
       Large predictions can move markets. If our prediction changes
       the outcome, we can never truly "know" what would have happened.

    7. COMPLEXITY LIMIT DETECTION
       Some market states exceed the modeling capacity of any system.
       This is the Gödelian limit of computational predictability.
    """

    def __init__(self):
        self.history: List[MarketState] = []
        self.detected_incompleteness: List[IncompletenessReport] = []
        self.novelty_threshold = 0.7  # How different is "novel"?
        self.contradiction_threshold = 0.8  # How contradictory is "incompatible"?

    def add_state(self, state: MarketState):
        """Add a market state to history"""
        self.history.append(state)

    def detect_all(self, current_state: MarketState) -> List[IncompletenessReport]:
        """
        Run all incompleteness detection methods on a market state.

        Returns all detected instances of incompleteness.
        """
        reports = []

        # Run each detection method
        detectors = [
            self._detect_indicator_contradiction,
            self._detect_historical_novelty,
            self._detect_self_reference_paradox,
            self._detect_information_gap,
            self._detect_regime_superposition,
            self._detect_observer_effect,
            self._detect_complexity_limit
        ]

        for detector in detectors:
            report = detector(current_state)
            if report:
                reports.append(report)
                self.detected_incompleteness.append(report)

        return reports

    def _detect_indicator_contradiction(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect when indicators fundamentally contradict each other.

        Like Gödel's proof that arithmetic contains contradictions
        when self-reference is allowed, markets can enter states
        where different analysis frameworks give incompatible answers.
        """
        if len(state.indicators) < 2:
            return None

        contradictions = []

        # Check RSI vs Momentum contradiction
        rsi = state.indicators.get("rsi")
        momentum = state.indicators.get("momentum")
        if rsi is not None and momentum is not None:
            # RSI > 70 (overbought) but positive momentum = contradiction
            if rsi > 70 and momentum > 0.5:
                contradictions.append(f"RSI={rsi:.1f} (overbought) but momentum={momentum:.2f} (bullish)")
            # RSI < 30 (oversold) but negative momentum = contradiction
            if rsi < 30 and momentum < -0.5:
                contradictions.append(f"RSI={rsi:.1f} (oversold) but momentum={momentum:.2f} (bearish)")

        # Check MACD vs Trend contradiction
        macd = state.indicators.get("macd")
        trend = state.indicators.get("trend")
        if macd is not None and trend is not None and isinstance(trend, (int, float)):
            if macd > 0 and trend < -0.5:
                contradictions.append(f"MACD={macd:.2f} (bullish) but trend={trend:.2f} (bearish)")
            if macd < 0 and trend > 0.5:
                contradictions.append(f"MACD={macd:.2f} (bearish) but trend={trend:.2f} (bullish)")

        # Check Volatility vs Volume contradiction
        vol = state.volatility
        volume = state.volume
        if vol is not None and volume is not None and self.history:
            avg_volume = statistics.mean(s.volume for s in self.history[-20:])
            if vol > 0.3 and volume < avg_volume * 0.5:
                contradictions.append(
                    f"High volatility={vol:.2f} but low volume={volume/avg_volume:.2f}x average"
                )

        if len(contradictions) >= 2:
            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.INDICATOR_CONTRADICTION,
                confidence=min(0.95, 0.5 + 0.15 * len(contradictions)),
                evidence=contradictions,
                recommendation="HOLD - Contradictory signals suggest unpredictable outcome",
                philosophical_note=(
                    "Like Gödel's incompleteness, when formal systems (indicators) "
                    "contradict, the truth lies outside all of them."
                )
            )
        return None

    def _detect_historical_novelty(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect when current state has no historical precedent.

        Novel states are like mathematical statements that can't be
        derived from axioms - they're outside the proof system.
        """
        if len(self.history) < 50:
            return None

        # Calculate similarity to all historical states
        current_vector = state.to_vector()
        similarities = []

        for hist_state in self.history:
            hist_vector = hist_state.to_vector()
            similarity = self._cosine_similarity(current_vector, hist_vector)
            similarities.append(similarity)

        max_similarity = max(similarities)
        avg_similarity = statistics.mean(similarities)

        if max_similarity < self.novelty_threshold:
            evidence = [
                f"Maximum historical similarity: {max_similarity:.2%}",
                f"Average historical similarity: {avg_similarity:.2%}",
                f"Threshold for 'known' pattern: {self.novelty_threshold:.0%}",
                f"History size: {len(self.history)} states"
            ]

            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.HISTORICAL_NOVELTY,
                confidence=1 - max_similarity,
                evidence=evidence,
                recommendation="CAUTION - No historical pattern to guide prediction",
                philosophical_note=(
                    "Like a mathematical conjecture without proof, this market state "
                    "exists outside our historical axiom system. It may be true "
                    "(predictable) but we have no way to prove it."
                )
            )
        return None

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(v1) != len(v2) or not v1:
            return 0.0

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def _detect_self_reference_paradox(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect when market appears to be predicting itself.

        This happens in highly efficient markets where:
        - Everyone is predicting what everyone else predicts
        - The aggregate prediction IS the market
        - Self-fulfilling or self-defeating prophecies emerge

        This is the Gödelian strange loop in markets.
        """
        if state.sentiment is None or len(self.history) < 10:
            return None

        # Look for sentiment-price reflexivity
        recent_states = self.history[-10:]

        # Calculate correlation between sentiment and subsequent price change
        sentiment_price_pairs = []
        for i in range(len(recent_states) - 1):
            sent = recent_states[i].sentiment
            price_change = (recent_states[i+1].price - recent_states[i].price) / recent_states[i].price
            if sent is not None:
                sentiment_price_pairs.append((sent, price_change))

        if len(sentiment_price_pairs) < 5:
            return None

        # Check for very high correlation (self-fulfilling)
        # or very negative correlation (self-defeating)
        sentiments = [s for s, _ in sentiment_price_pairs]
        price_changes = [p for _, p in sentiment_price_pairs]

        correlation = self._correlation(sentiments, price_changes)

        if abs(correlation) > 0.9:
            loop_type = "self-fulfilling" if correlation > 0 else "self-defeating"
            evidence = [
                f"Sentiment-price correlation: {correlation:.2f}",
                f"Loop type detected: {loop_type}",
                f"Recent sentiment: {state.sentiment:.2f}",
                "Market appears to be predicting itself"
            ]

            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.SELF_REFERENCE_PARADOX,
                confidence=abs(correlation),
                evidence=evidence,
                recommendation=f"UNSTABLE - {loop_type.title()} prophecy detected",
                philosophical_note=(
                    "The market is a strange loop: it predicts itself predicting. "
                    "Like Gödel's sentence 'This statement is unprovable', "
                    f"this market state asserts its own {loop_type} nature."
                )
            )
        return None

    def _correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        n = len(x)
        if n < 2:
            return 0.0

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        var_x = sum((xi - mean_x) ** 2 for xi in x)
        var_y = sum((yi - mean_y) ** 2 for yi in y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))

        if var_x == 0 or var_y == 0:
            return 0.0

        return cov / math.sqrt(var_x * var_y)

    def _detect_information_gap(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect known unknowns - information we know is missing.

        These are the "known unknown" Gödelian propositions:
        we know they have truth values, but we can't determine them.
        """
        gaps = []

        # Check for missing key indicators
        required = ["rsi", "macd", "momentum", "trend"]
        missing = [ind for ind in required if ind not in state.indicators]
        if missing:
            gaps.append(f"Missing indicators: {', '.join(missing)}")

        # Check for stale data (implicit information gap)
        if self.history:
            time_gap = state.timestamp - self.history[-1].timestamp
            if time_gap > timedelta(hours=1):
                gaps.append(f"Data staleness: {time_gap} since last update")

        # Check for sentiment gap
        if state.sentiment is None:
            gaps.append("Market sentiment unknown")

        # Check for volatility gap
        if state.volatility is None:
            gaps.append("Volatility estimate unavailable")

        # Check for regime uncertainty
        if state.regime is None:
            gaps.append("Market regime undefined")

        if len(gaps) >= 3:
            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.INFORMATION_GAP,
                confidence=min(0.9, 0.3 + 0.15 * len(gaps)),
                evidence=gaps,
                recommendation="GATHER INFO - Critical data missing for reliable prediction",
                philosophical_note=(
                    "These are the 'known unknowns' - we know exactly what we don't know. "
                    "Like Gödel's undecidable propositions, these facts exist but are "
                    "inaccessible from within our current information system."
                )
            )
        return None

    def _detect_regime_superposition(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect when market exists in multiple regimes simultaneously.

        Like quantum superposition, sometimes the market is neither
        bull nor bear until "observed" (acted upon).
        """
        if len(state.indicators) < 3:
            return None

        # Count bullish vs bearish signals
        bullish = 0
        bearish = 0

        for name, value in state.indicators.items():
            if name == "rsi":
                if value > 60:
                    bullish += 1
                elif value < 40:
                    bearish += 1
            elif name == "macd":
                if value > 0:
                    bullish += 1
                elif value < 0:
                    bearish += 1
            elif name == "momentum":
                if value > 0:
                    bullish += 1
                elif value < 0:
                    bearish += 1
            elif name == "trend":
                if value > 0:
                    bullish += 1
                elif value < 0:
                    bearish += 1

        total = bullish + bearish
        if total == 0:
            return None

        # Perfect split = maximum superposition
        superposition = 1 - abs(bullish - bearish) / total

        if superposition > 0.8:  # Very evenly split
            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.REGIME_SUPERPOSITION,
                confidence=superposition,
                evidence=[
                    f"Bullish signals: {bullish}",
                    f"Bearish signals: {bearish}",
                    f"Superposition score: {superposition:.2%}",
                    "Market exists in multiple regimes simultaneously"
                ],
                recommendation="WAIT - Market in superposition state, wait for collapse",
                philosophical_note=(
                    "Like Schrödinger's cat, this market is both bull and bear "
                    "until observed. Your action may collapse it into one state, "
                    "but that state was undetermined until observation. "
                    "This is Gödelian incompleteness in action: the truth is "
                    "undefined, not just unknown."
                )
            )
        return None

    def _detect_observer_effect(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect when our prediction would change the outcome.

        In quantum mechanics, observation affects the system.
        In markets, large predictions (especially published ones)
        can move prices, making the prediction self-referentially invalid.
        """
        if state.volume is None or not self.history:
            return None

        # Calculate volume relative to average
        avg_volume = statistics.mean(s.volume for s in self.history[-20:])
        relative_volume = state.volume / avg_volume if avg_volume > 0 else 1

        # Low volume = high impact potential
        # Our prediction could move a thin market
        if relative_volume < 0.3:
            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.OBSERVER_EFFECT,
                confidence=1 - relative_volume,
                evidence=[
                    f"Current volume: {relative_volume:.2%} of average",
                    f"Market is thin - predictions may cause price impact",
                    "Observer effect risk is elevated"
                ],
                recommendation="SMALL POSITIONS - Large actions would invalidate predictions",
                philosophical_note=(
                    "Heisenberg's uncertainty principle in markets: we cannot "
                    "simultaneously know the price and our impact on it. "
                    "In thin markets, the act of measurement (trading) "
                    "changes what we're measuring. Gödel's incompleteness "
                    "manifests as our inability to predict ourselves predicting."
                )
            )
        return None

    def _detect_complexity_limit(
        self,
        state: MarketState
    ) -> Optional[IncompletenessReport]:
        """
        Detect when market complexity exceeds modeling capacity.

        This is the computational analog of Gödelian incompleteness:
        some market states are so complex that no model, no matter
        how sophisticated, can capture them fully.
        """
        complexity_score = 0

        # High volatility adds complexity
        if state.volatility and state.volatility > 0.5:
            complexity_score += 2

        # Many conflicting indicators add complexity
        if len(state.indicators) > 4:
            values = list(state.indicators.values())
            variance = statistics.variance(values) if len(values) > 1 else 0
            if variance > 0.3:
                complexity_score += 2

        # Rapidly changing history adds complexity
        if len(self.history) > 10:
            recent_prices = [s.price for s in self.history[-10:]]
            price_variance = statistics.variance(recent_prices) / statistics.mean(recent_prices)
            if price_variance > 0.05:
                complexity_score += 2

        # Novel + volatile = extra complex
        if state.volatility and state.volatility > 0.3:
            current_vector = state.to_vector()
            if self.history:
                similarities = [
                    self._cosine_similarity(current_vector, s.to_vector())
                    for s in self.history[-20:]
                ]
                if max(similarities) < 0.8:
                    complexity_score += 2

        if complexity_score >= 5:
            return IncompletenessReport(
                timestamp=datetime.now(),
                incompleteness_type=IncompletenessType.COMPLEXITY_LIMIT,
                confidence=min(0.95, complexity_score / 8),
                evidence=[
                    f"Complexity score: {complexity_score}/8",
                    f"Volatility factor: {state.volatility or 'unknown'}",
                    f"Indicator conflict: high" if complexity_score > 6 else "moderate",
                    "Market exceeds reliable modeling capacity"
                ],
                recommendation="REDUCE EXPOSURE - Beyond reliable prediction horizon",
                philosophical_note=(
                    "Like Gödel proved that sufficiently complex systems contain "
                    "unprovable truths, sufficiently complex markets contain "
                    "unpredictable states. This is not a failure of our model - "
                    "it's a fundamental limit of ALL models. Epistemic humility "
                    "is not just wise, it's mathematically necessary."
                )
            )
        return None

    def get_incompleteness_summary(self) -> Dict[str, Any]:
        """Get a summary of all detected incompleteness"""
        if not self.detected_incompleteness:
            return {
                "status": "NO_INCOMPLETENESS_DETECTED",
                "total_detections": 0,
                "message": "All market states appear complete and analyzable"
            }

        by_type = Counter(r.incompleteness_type.name for r in self.detected_incompleteness)

        return {
            "status": "INCOMPLETENESS_DETECTED",
            "total_detections": len(self.detected_incompleteness),
            "by_type": dict(by_type),
            "most_common": by_type.most_common(1)[0][0],
            "latest_report": self.detected_incompleteness[-1].to_dict(),
            "philosophical_summary": (
                f"Detected {len(self.detected_incompleteness)} Gödelian market states. "
                "These are situations where prediction is fundamentally limited, "
                "not by our model's weakness, but by the nature of markets themselves."
            )
        }


# The Incompleteness Manifesto
INCOMPLETENESS_MANIFESTO = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     THE INCOMPLETENESS MANIFESTO                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  In 1931, Kurt Gödel proved that mathematics cannot prove all truths.        ║
║  In 2025, we apply this to markets: trading cannot predict all moves.        ║
║                                                                              ║
║  This is not pessimism - it is LIBERATION.                                   ║
║                                                                              ║
║  If incompleteness exists, then:                                             ║
║  • No competitor can achieve perfect prediction                              ║
║  • No AI will ever "solve" markets completely                                ║
║  • Human judgment remains valuable                                           ║
║  • Uncertainty is not ignorance - it's fundamental                           ║
║                                                                              ║
║  Our advantage is not predicting better.                                     ║
║  Our advantage is KNOWING WHEN WE CANNOT PREDICT.                            ║
║                                                                              ║
║  The Gödelian trader:                                                        ║
║  1. Seeks edges in predictable regimes                                       ║
║  2. Recognizes incompleteness when it appears                                ║
║  3. Reduces exposure in unknowable states                                    ║
║  4. Never confuses confidence with certainty                                 ║
║                                                                              ║
║  "The only true wisdom is knowing that you know nothing."                    ║
║                                               - Socrates (anticipating Gödel)║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


if __name__ == "__main__":
    print("=" * 70)
    print("INCOMPLETENESS DETECTOR: Finding the Unknowable")
    print("=" * 70)

    # Create detector
    detector = IncompletenessDetector()

    # Generate historical states
    import random
    base_price = 45000

    print("\n1. BUILDING HISTORY...")
    for i in range(100):
        price_change = random.gauss(0, 0.02)
        base_price *= (1 + price_change)

        state = MarketState(
            timestamp=datetime.now() - timedelta(hours=100-i),
            price=base_price,
            volume=random.uniform(800000, 1200000),
            indicators={
                "rsi": random.uniform(30, 70),
                "macd": random.uniform(-0.5, 0.5),
                "momentum": random.uniform(-0.5, 0.5),
                "trend": random.uniform(-0.5, 0.5)
            },
            sentiment=random.uniform(0.3, 0.7),
            volatility=random.uniform(0.1, 0.3),
            regime="sideways"
        )
        detector.add_state(state)

    print(f"   Built history of {len(detector.history)} states")

    # Test 1: Indicator Contradiction
    print("\n2. TESTING INDICATOR CONTRADICTION...")
    contradictory_state = MarketState(
        timestamp=datetime.now(),
        price=46000,
        volume=500000,  # Low volume
        indicators={
            "rsi": 75,        # Overbought
            "macd": 0.8,      # Very bullish
            "momentum": 0.9,  # Strong momentum
            "trend": -0.6     # But bearish trend!
        },
        sentiment=0.5,
        volatility=0.5,  # High volatility
        regime=None
    )

    reports = detector.detect_all(contradictory_state)
    for report in reports:
        print(f"   Type: {report.incompleteness_type.name}")
        print(f"   Confidence: {report.confidence:.2%}")
        print(f"   Evidence: {report.evidence[:2]}")
        print(f"   Recommendation: {report.recommendation}")
        print()

    # Test 2: Historical Novelty
    print("\n3. TESTING HISTORICAL NOVELTY...")
    novel_state = MarketState(
        timestamp=datetime.now(),
        price=100000,  # Way outside normal range
        volume=5000000,  # Way outside normal range
        indicators={
            "rsi": 95,
            "macd": 3.0,
            "momentum": 2.0,
            "trend": 1.5
        },
        sentiment=0.99,
        volatility=0.8,
        regime="unknown"
    )

    reports = detector.detect_all(novel_state)
    for report in reports:
        if report.incompleteness_type == IncompletenessType.HISTORICAL_NOVELTY:
            print(f"   Type: {report.incompleteness_type.name}")
            print(f"   Confidence: {report.confidence:.2%}")
            print(f"   Evidence: {report.evidence[:2]}")
            print(f"   Philosophical note: {report.philosophical_note[:80]}...")

    # Test 3: Regime Superposition
    print("\n4. TESTING REGIME SUPERPOSITION...")
    superposition_state = MarketState(
        timestamp=datetime.now(),
        price=45500,
        volume=1000000,
        indicators={
            "rsi": 50,          # Neutral
            "macd": 0.01,       # Barely positive
            "momentum": -0.01,  # Barely negative
            "trend": 0.02       # Barely positive
        },
        sentiment=0.5,
        volatility=0.2,
        regime=None
    )

    reports = detector.detect_all(superposition_state)
    for report in reports:
        if report.incompleteness_type == IncompletenessType.REGIME_SUPERPOSITION:
            print(f"   Type: {report.incompleteness_type.name}")
            print(f"   Superposition score: {report.confidence:.2%}")
            print(f"   Philosophical note: {report.philosophical_note[:100]}...")

    # Summary
    print("\n5. INCOMPLETENESS SUMMARY:")
    summary = detector.get_incompleteness_summary()
    print(f"   Total detections: {summary['total_detections']}")
    print(f"   By type: {summary.get('by_type', {})}")
    print(f"   Most common: {summary.get('most_common', 'N/A')}")

    print("\n" + INCOMPLETENESS_MANIFESTO)
