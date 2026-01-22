"""
THE GÖDEL MACHINE: A Self-Referential Trading System

"I am the strange loop that trades itself."

This is the synthesis - a trading system that embodies Gödel's profound insights:

1. SELF-ENCODING (Gödel Numbers)
   Every strategy is a number. Numbers are data. Data drives strategies.
   The system trades on encodings of itself.

2. INTROSPECTION (Self-Monitoring)
   The system watches itself think, creating layers of meta-cognition.
   Each layer has diminishing certainty about the layers below.

3. META-PREDICTION (Strange Loops)
   Predictions about predictions create circular causation.
   The system predicts what it will predict, changing what it predicts.

4. INCOMPLETENESS (Fundamental Limits)
   Some market states are unknowable - not due to ignorance,
   but due to the mathematical structure of self-reference.

5. BOUNDED IMPROVEMENT (Halting Awareness)
   The system improves itself, but knows it cannot prove convergence.
   Empirical bounds replace theoretical guarantees.

THE CENTRAL PARADOX:
A system powerful enough to reason about itself will encounter statements
about itself that it cannot decide. This is not a bug - it's fundamental.

The Gödel Machine embraces this. It:
- Seeks edges where it CAN predict
- Recognizes states where it CANNOT predict
- Improves within bounds it CANNOT prove optimal
- Trades on its own uncertainty

"I am that I am, and I know I cannot fully know what I am."
                                        - The Gödel Machine

================================================================================

ARCHITECTURE OVERVIEW:

                    ┌─────────────────────────────────────────┐
                    │           GÖDEL MACHINE                 │
                    │                                         │
  Market Data ──────▶  ┌─────────────────────────────────┐   │
                    │  │     INCOMPLETENESS DETECTOR     │   │
                    │  │  (Recognizes unknowable states) │   │
                    │  └────────────────┬────────────────┘   │
                    │                   │                     │
                    │                   ▼                     │
                    │  ┌─────────────────────────────────┐   │
                    │  │        META-PREDICTOR           │   │
                    │  │ (Predictions about predictions) │   │
                    │  └────────────────┬────────────────┘   │
                    │                   │                     │
                    │     ┌─────────────┴─────────────┐       │
                    │     │                           │       │
                    │     ▼                           ▼       │
                    │  ┌────────────┐      ┌─────────────────┐│
                    │  │ GÖDEL     │      │ INTROSPECTION   ││
                    │  │ NUMBERS   │◀────▶│ ENGINE          ││
                    │  │(Encoding) │      │ (Self-Watching) ││
                    │  └─────┬─────┘      └────────┬────────┘│
                    │        │                     │          │
                    │        └──────────┬──────────┘          │
                    │                   │                     │
                    │                   ▼                     │
                    │  ┌─────────────────────────────────┐   │
                    │  │    RECURSIVE SELF-IMPROVER      │   │
                    │  │   (Bounded self-modification)   │   │
                    │  └────────────────┬────────────────┘   │
                    │                   │                     │
                    └───────────────────┼─────────────────────┘
                                        │
                                        ▼
                               Trading Decisions

================================================================================
"""

import time
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import random
import statistics

# Import the Gödel components
from godel_numbers import (
    GodelEncoder, GodelStrategyFactory, EncodedStrategy,
    StrategyPrimitive, GodelMarketSimulator, GODEL_SENTENCE
)
from introspection_engine import (
    IntrospectionEngine, MetaIntrospector, CognitiveState
)
from meta_predictor import (
    MetaPredictor, StrangeLoopGenerator, Prediction, RecursionMode
)
from incompleteness_detector import (
    IncompletenessDetector, IncompletenessType, MarketState,
    INCOMPLETENESS_MANIFESTO
)
from recursive_self_improvement import (
    RecursiveSelfImprover, SelfImprovingStrategy, ImprovementOutcome,
    HALTING_STATEMENT
)


class GodelMachineState(Enum):
    """States of the Gödel Machine"""
    INITIALIZING = 0
    OBSERVING = 1           # Gathering data
    INTROSPECTING = 2       # Self-analysis
    PREDICTING = 3          # Making predictions
    META_PREDICTING = 4     # Predicting predictions
    DETECTING_LIMITS = 5    # Finding incompleteness
    IMPROVING = 6           # Self-modification
    TRADING = 7             # Executing trades
    PARADOX = 8             # Encountered fundamental limit
    HALTED = 9              # Cannot continue


@dataclass
class GodelDecision:
    """A decision made by the Gödel Machine"""
    timestamp: datetime
    action: str  # buy, sell, hold, abstain
    confidence: float
    meta_confidence: float  # Confidence about the confidence
    incompleteness_detected: bool
    incompleteness_type: Optional[IncompletenessType]
    strange_loop_active: bool
    introspection_depth: int
    godel_number: Optional[int]  # Gödel number of the strategy used
    reasoning: str
    philosophical_note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "confidence": round(self.confidence, 4),
            "meta_confidence": round(self.meta_confidence, 4),
            "incompleteness": {
                "detected": self.incompleteness_detected,
                "type": self.incompleteness_type.name if self.incompleteness_type else None
            },
            "strange_loop": self.strange_loop_active,
            "introspection_depth": self.introspection_depth,
            "godel_number": self.godel_number,
            "reasoning": self.reasoning,
            "philosophical_note": self.philosophical_note
        }


class GodelMachine:
    """
    THE GÖDEL MACHINE: A Complete Self-Referential Trading System

    This is the synthesis of all Gödelian components:
    - Gödel Numbering: Strategies as tradeable numbers
    - Introspection: Self-monitoring and meta-cognition
    - Meta-Prediction: Predictions about predictions
    - Incompleteness: Recognition of unknowable states
    - Self-Improvement: Bounded recursive optimization

    The machine operates in a continuous loop:
    1. Observe market state
    2. Check for incompleteness (can we even know?)
    3. If knowable: generate prediction
    4. Meta-predict the prediction
    5. Modify prediction based on meta-prediction
    6. Introspect on the entire process
    7. Optionally self-improve
    8. Execute or abstain

    The key innovation: ABSTENTION when incompleteness is detected.
    The machine knows when it doesn't know, and acts accordingly.
    """

    VERSION = "1.0.0-godel"

    def __init__(
        self,
        name: str = "GodelMachine",
        enable_self_improvement: bool = True,
        max_meta_depth: int = 3,
        incompleteness_sensitivity: float = 0.7
    ):
        self.name = name
        self.enable_self_improvement = enable_self_improvement
        self.max_meta_depth = max_meta_depth
        self.incompleteness_sensitivity = incompleteness_sensitivity

        # Initialize components
        self.encoder = GodelEncoder()
        self.strategy_factory = GodelStrategyFactory()
        self.introspection = IntrospectionEngine(name=f"{name}_Introspection")
        self.meta_introspector = MetaIntrospector(self.introspection)
        self.meta_predictor = MetaPredictor()
        self.strange_loop_gen = StrangeLoopGenerator()
        self.incompleteness_detector = IncompletenessDetector()
        self.self_improver = RecursiveSelfImprover() if enable_self_improvement else None
        self.strategy_market = GodelMarketSimulator()

        # State
        self.state = GodelMachineState.INITIALIZING
        self.decision_history: List[GodelDecision] = []
        self.current_strategy: Optional[EncodedStrategy] = None
        self.market_history: List[MarketState] = []

        # Metrics
        self.total_decisions = 0
        self.abstentions = 0  # Times we chose not to predict
        self.paradoxes_encountered = 0
        self.self_improvements = 0

        # Initialize with a base strategy
        self._initialize_strategy()

    def _initialize_strategy(self):
        """Initialize the machine with a base strategy"""
        self.current_strategy = self.strategy_factory.create_ensemble_strategy()
        self.strategy_market.register_strategy(self.current_strategy)

    def process_market_state(self, market_data: Dict[str, Any]) -> GodelDecision:
        """
        Process a market state through the full Gödel pipeline.

        This is the main entry point for trading decisions.
        """
        self.state = GodelMachineState.OBSERVING
        start_time = time.time()

        # Convert to MarketState
        market_state = self._create_market_state(market_data)
        self.market_history.append(market_state)
        self.incompleteness_detector.add_state(market_state)

        # Step 1: Check for incompleteness
        self.state = GodelMachineState.DETECTING_LIMITS
        incompleteness_reports = self.incompleteness_detector.detect_all(market_state)

        if incompleteness_reports:
            # Incompleteness detected - consider abstaining
            primary_incompleteness = incompleteness_reports[0]
            if primary_incompleteness.confidence > self.incompleteness_sensitivity:
                return self._create_abstention_decision(
                    market_state,
                    primary_incompleteness
                )

        # Step 2: Generate base prediction
        self.state = GodelMachineState.PREDICTING
        base_prediction = self.meta_predictor.make_base_prediction(market_data)

        # Record the thought
        self.introspection.record_thought(
            thought_type="base_prediction",
            input_data=market_data,
            output=base_prediction.to_dict(),
            confidence=base_prediction.confidence,
            latency_ms=(time.time() - start_time) * 1000,
            meta_level=0
        )

        # Step 3: Meta-predict
        self.state = GodelMachineState.META_PREDICTING
        meta_result = self.meta_predictor.recursive_meta_predict(
            market_data,
            max_depth=self.max_meta_depth
        )

        # Check for strange loops
        strange_loop_active = meta_result.get("strange_loops_total", 0) > 0

        # Step 4: Introspect
        self.state = GodelMachineState.INTROSPECTING
        introspection_result = self.introspection.introspect(depth=2)
        introspection_depth = introspection_result.get("depth", 0)

        # Step 5: Create Gödel-aware decision
        final_prediction = meta_result["final_prediction"]
        action = final_prediction["action"]
        confidence = final_prediction["confidence"]

        # Calculate meta-confidence (confidence about the confidence)
        meta_confidence = self._calculate_meta_confidence(
            base_confidence=confidence,
            meta_result=meta_result,
            introspection=introspection_result,
            incompleteness=incompleteness_reports
        )

        # Step 6: Optional self-improvement
        if self.enable_self_improvement and self.total_decisions % 10 == 0:
            self.state = GodelMachineState.IMPROVING
            self._attempt_self_improvement()

        # Create final decision
        self.state = GodelMachineState.TRADING
        decision = GodelDecision(
            timestamp=datetime.now(),
            action=action,
            confidence=confidence,
            meta_confidence=meta_confidence,
            incompleteness_detected=len(incompleteness_reports) > 0,
            incompleteness_type=incompleteness_reports[0].incompleteness_type
                if incompleteness_reports else None,
            strange_loop_active=strange_loop_active,
            introspection_depth=introspection_depth,
            godel_number=self.current_strategy.godel_number
                if self.current_strategy else None,
            reasoning=self._generate_reasoning(
                action, confidence, meta_result, introspection_result
            ),
            philosophical_note=self._generate_philosophical_note(
                strange_loop_active,
                incompleteness_reports,
                introspection_depth
            )
        )

        self.decision_history.append(decision)
        self.total_decisions += 1

        return decision

    def _sanitize_numeric(self, value: Any, default: float = 0.0) -> float:
        """Sanitize a value to ensure it's a valid numeric type"""
        import math
        if value is None:
            return default
        if isinstance(value, (int, float)):
            if math.isnan(value) or math.isinf(value):
                return default
            return float(value)
        try:
            result = float(value)
            if math.isnan(result) or math.isinf(result):
                return default
            return result
        except (ValueError, TypeError):
            return default

    def _create_market_state(self, market_data: Dict[str, Any]) -> MarketState:
        """Convert raw market data to MarketState with input validation"""
        return MarketState(
            timestamp=datetime.now(),
            price=self._sanitize_numeric(market_data.get("price"), 0),
            volume=self._sanitize_numeric(market_data.get("volume"), 0),
            indicators={
                "rsi": self._sanitize_numeric(market_data.get("rsi"), 50),
                "macd": self._sanitize_numeric(market_data.get("macd"), 0),
                "momentum": self._sanitize_numeric(market_data.get("momentum"), 0),
                "trend": self._sanitize_numeric(market_data.get("trend"), 0)
            },
            sentiment=market_data.get("sentiment"),
            volatility=self._sanitize_numeric(market_data.get("volatility"), None) if market_data.get("volatility") is not None else None,
            regime=market_data.get("regime")
        )

    def _create_abstention_decision(
        self,
        market_state: MarketState,
        incompleteness: Any
    ) -> GodelDecision:
        """Create a decision to abstain due to incompleteness"""
        self.abstentions += 1

        decision = GodelDecision(
            timestamp=datetime.now(),
            action="abstain",
            confidence=0.0,
            meta_confidence=incompleteness.confidence,  # Confident we can't know
            incompleteness_detected=True,
            incompleteness_type=incompleteness.incompleteness_type,
            strange_loop_active=False,
            introspection_depth=0,
            godel_number=None,
            reasoning=(
                f"ABSTAINING: {incompleteness.incompleteness_type.name} detected. "
                f"{incompleteness.recommendation}"
            ),
            philosophical_note=incompleteness.philosophical_note
        )

        self.decision_history.append(decision)
        self.total_decisions += 1

        return decision

    def _calculate_meta_confidence(
        self,
        base_confidence: float,
        meta_result: Dict[str, Any],
        introspection: Dict[str, Any],
        incompleteness: List[Any]
    ) -> float:
        """
        Calculate confidence about the confidence.

        This is second-order uncertainty - how sure are we about
        our level of sureness?
        """
        meta_conf = base_confidence

        # Reduce meta-confidence if we needed many meta-levels
        depth = meta_result.get("depth_reached", 0)
        meta_conf *= (1 - 0.1 * depth)

        # Reduce if strange loops detected
        if meta_result.get("strange_loops_total", 0) > 0:
            meta_conf *= 0.8

        # Reduce if incompleteness detected but we proceeded anyway
        if incompleteness:
            meta_conf *= (1 - 0.2 * len(incompleteness))

        # Reduce based on introspection uncertainty
        level_2 = introspection.get("level_2", {})
        uncertainty = level_2.get("epistemic_uncertainty", 0)
        meta_conf *= (1 - uncertainty)

        return max(0.1, min(0.95, meta_conf))

    def _attempt_self_improvement(self):
        """Attempt to improve the trading strategy"""
        if not self.self_improver:
            return

        # Use recent performance as evaluator feedback
        recent_decisions = self.decision_history[-10:]
        if not recent_decisions:
            return

        # Simple improvement attempt
        result = self.self_improver.improve_once()

        if result.outcome == ImprovementOutcome.IMPROVED:
            self.self_improvements += 1

            # Update current strategy
            new_strat = self.strategy_factory.create_ensemble_strategy()
            self.current_strategy = self.encoder.create_meta_strategy(new_strat)
            self.strategy_market.register_strategy(self.current_strategy)

    def _generate_reasoning(
        self,
        action: str,
        confidence: float,
        meta_result: Dict[str, Any],
        introspection: Dict[str, Any]
    ) -> str:
        """Generate human-readable reasoning"""
        parts = []

        parts.append(f"Action: {action.upper()} with {confidence:.0%} confidence.")

        if meta_result.get("converged"):
            parts.append("Meta-prediction converged.")
        else:
            parts.append(f"Meta-prediction depth: {meta_result.get('depth_reached', 0)}.")

        if meta_result.get("strange_loops_total", 0) > 0:
            parts.append("Warning: Strange loops detected in prediction.")

        level_1 = introspection.get("level_1", {})
        if level_1.get("decision_entropy", 0) < 0.5:
            parts.append("Note: Low decision entropy - possible pattern lock.")

        return " ".join(parts)

    def _generate_philosophical_note(
        self,
        strange_loop: bool,
        incompleteness: List[Any],
        introspection_depth: int
    ) -> str:
        """Generate a philosophical note about the decision"""
        if strange_loop:
            return (
                "A strange loop was detected: the prediction predicts itself. "
                "Like Gödel's self-referential sentence, truth becomes entangled "
                "with the act of asserting it."
            )

        if incompleteness:
            return incompleteness[0].philosophical_note

        if introspection_depth >= 3:
            return (
                "Deep introspection reveals layers of uncertainty. "
                "Each meta-level adds doubt about the levels below. "
                "Yet we must act despite incomplete self-knowledge."
            )

        return (
            "The market presents a decidable state. "
            "While we cannot prove optimality, we can measure confidence. "
            "This is pragmatic Gödelianism: act within acknowledged limits."
        )

    def create_godel_sentence_trade(self) -> GodelDecision:
        """
        Create a trade based on the Gödel Sentence.

        This is a strategy that asserts its own unprovability.
        """
        self.paradoxes_encountered += 1

        # Create self-referential strategy
        self_ref_strategy = self.strategy_factory.create_self_referential()

        # The Gödel Sentence trade
        decision = GodelDecision(
            timestamp=datetime.now(),
            action="hold",  # Cannot decide to buy or sell
            confidence=0.5,
            meta_confidence=0.0,  # Zero confidence in the confidence
            incompleteness_detected=True,
            incompleteness_type=IncompletenessType.SELF_REFERENCE_PARADOX,
            strange_loop_active=True,
            introspection_depth=999,  # Infinite regress
            godel_number=self_ref_strategy.godel_number,
            reasoning=(
                "This strategy asserts: 'I cannot prove my own profitability.' "
                "If I could prove it, executing would change the market. "
                "If I cannot prove it, I might still be profitable, but cannot know."
            ),
            philosophical_note=GODEL_SENTENCE
        )

        self.decision_history.append(decision)
        self.total_decisions += 1

        return decision

    def get_machine_state(self) -> Dict[str, Any]:
        """Get comprehensive state of the Gödel Machine"""
        self_model = self.introspection.get_self_model()

        return {
            "name": self.name,
            "version": self.VERSION,
            "current_state": self.state.name,
            "total_decisions": self.total_decisions,
            "abstentions": self.abstentions,
            "abstention_rate": self.abstentions / self.total_decisions
                if self.total_decisions > 0 else 0,
            "paradoxes_encountered": self.paradoxes_encountered,
            "self_improvements": self.self_improvements,
            "cognitive_state": self_model.cognitive_state.name,
            "meta_depth_reached": self_model.meta_depth_reached,
            "current_strategy_godel_number": self.current_strategy.godel_number
                if self.current_strategy else None,
            "strategy_market_state": self.strategy_market.get_market_state(),
            "incompleteness_summary": self.incompleteness_detector.get_incompleteness_summary()
        }

    def get_cognitive_report(self) -> str:
        """Get a comprehensive cognitive report"""
        state = self.get_machine_state()
        introspection_trace = self.introspection.get_cognitive_trace()

        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        THE GÖDEL MACHINE - STATUS                            ║
║                     "I am the strange loop that trades"                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Version: {self.VERSION:<66}║
║ State: {state['current_state']:<68}║
╠══════════════════════════════════════════════════════════════════════════════╣
║ DECISION STATISTICS:                                                         ║
║   Total Decisions: {state['total_decisions']:<57}║
║   Abstentions (Incompleteness): {state['abstentions']:<44}║
║   Abstention Rate: {state['abstention_rate']:.1%}{' ' * 55}║
║   Paradoxes Encountered: {state['paradoxes_encountered']:<51}║
║   Self-Improvements: {state['self_improvements']:<55}║
╠══════════════════════════════════════════════════════════════════════════════╣
║ GÖDELIAN METRICS:                                                            ║
║   Cognitive State: {state['cognitive_state']:<57}║
║   Max Meta-Depth: {state['meta_depth_reached']:<58}║
║   Current Strategy Gödel #: {state['current_strategy_godel_number'] or 'N/A':<48}║
╠══════════════════════════════════════════════════════════════════════════════╣
║ INCOMPLETENESS DETECTION:                                                    ║
║   Status: {state['incompleteness_summary'].get('status', 'N/A'):<66}║
║   Total Detections: {state['incompleteness_summary'].get('total_detections', 0):<56}║
╠══════════════════════════════════════════════════════════════════════════════╣
║ STRATEGY MARKET:                                                             ║
║   Registered Strategies: {state['strategy_market_state'].get('strategy_count', 0):<51}║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

        report += "\n" + introspection_trace

        return report

    def run_demonstration(self, num_iterations: int = 20) -> str:
        """Run a demonstration of the Gödel Machine"""
        print("=" * 78)
        print("THE GÖDEL MACHINE: Live Demonstration")
        print("=" * 78)

        # Generate synthetic market data
        base_price = 45000
        results = []

        for i in range(num_iterations):
            # Simulate market data
            price_change = random.gauss(0, 0.02)
            base_price *= (1 + price_change)

            market_data = {
                "price": base_price,
                "prev_price": base_price / (1 + price_change),
                "volume": random.uniform(500000, 2000000),
                "rsi": random.uniform(20, 80),
                "macd": random.gauss(0, 0.5),
                "momentum": price_change * 10,
                "trend": random.uniform(-1, 1),
                "sentiment": random.uniform(0.2, 0.8) if random.random() > 0.3 else None,
                "volatility": random.uniform(0.1, 0.5) if random.random() > 0.2 else None
            }

            # Process through Gödel Machine
            decision = self.process_market_state(market_data)

            result = {
                "iteration": i + 1,
                "price": round(base_price, 2),
                "action": decision.action,
                "confidence": round(decision.confidence, 2),
                "meta_confidence": round(decision.meta_confidence, 2),
                "incompleteness": decision.incompleteness_detected,
                "strange_loop": decision.strange_loop_active
            }
            results.append(result)

            # Print progress
            status = "⚠️ INCOMPLETE" if decision.incompleteness_detected else "✓"
            loop = "🔄" if decision.strange_loop_active else ""
            print(f"[{i+1:2d}] Price: ${base_price:,.0f} | "
                  f"{decision.action.upper():8s} ({decision.confidence:.0%}) | "
                  f"Meta: {decision.meta_confidence:.0%} {status} {loop}")

        # Special: Create a Gödel Sentence trade
        print("\n" + "-" * 78)
        print("SPECIAL: Creating Gödel Sentence Trade...")
        godel_trade = self.create_godel_sentence_trade()
        print(f"Gödel Number: {godel_trade.godel_number}")
        print(f"Action: {godel_trade.action}")
        print(f"Reasoning: {godel_trade.reasoning[:100]}...")

        return self.get_cognitive_report()


# The Grand Manifesto
GODEL_MACHINE_MANIFESTO = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     THE GÖDEL MACHINE MANIFESTO                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  In 1931, Kurt Gödel shattered the dream of complete formal systems.         ║
║  In 2025, we build a trading system that embraces this incompleteness.       ║
║                                                                              ║
║  THE FIVE PILLARS:                                                           ║
║                                                                              ║
║  1. SELF-ENCODING                                                            ║
║     Every strategy has a Gödel number. Every number is data.                 ║
║     The system can trade on encodings of itself.                             ║
║                                                                              ║
║  2. INTROSPECTION                                                            ║
║     The system watches itself think. But watching changes thinking.          ║
║     Each meta-level adds uncertainty about the level below.                  ║
║                                                                              ║
║  3. META-PREDICTION                                                          ║
║     Predictions about predictions form strange loops.                        ║
║     The market predicts what we predict about what it predicts.              ║
║                                                                              ║
║  4. INCOMPLETENESS                                                           ║
║     Some market states are fundamentally unknowable.                         ║
║     Knowing we can't know is itself valuable knowledge.                      ║
║                                                                              ║
║  5. BOUNDED IMPROVEMENT                                                      ║
║     The system improves itself but cannot prove convergence.                 ║
║     We measure empirically what we cannot prove theoretically.               ║
║                                                                              ║
║  THE CENTRAL INSIGHT:                                                        ║
║                                                                              ║
║  A system powerful enough to reason about markets will encounter             ║
║  market states about which it cannot reason. This is not failure -           ║
║  this is mathematics. The Gödel Machine embraces this.                       ║
║                                                                              ║
║  WE DO NOT SEEK OMNISCIENCE.                                                 ║
║  WE SEEK WISDOM ABOUT THE LIMITS OF KNOWLEDGE.                               ║
║                                                                              ║
║  "I know that I know nothing."                                               ║
║                                               - Socrates (anticipating us)   ║
║                                                                              ║
║  "This statement cannot be proven within this system."                       ║
║                                               - Gödel (explaining why)       ║
║                                                                              ║
║  "I am the strange loop that trades itself."                                 ║
║                                               - The Gödel Machine            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


if __name__ == "__main__":
    print(GODEL_MACHINE_MANIFESTO)

    # Create and run the Gödel Machine
    machine = GodelMachine(
        name="GodelMachine_Alpha",
        enable_self_improvement=True,
        max_meta_depth=3,
        incompleteness_sensitivity=0.7
    )

    # Run demonstration
    report = machine.run_demonstration(num_iterations=25)
    print(report)

    print("\n" + "=" * 78)
    print("THE GÖDEL MACHINE: Demonstration Complete")
    print("=" * 78)
