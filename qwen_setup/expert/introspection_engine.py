"""
INTROSPECTION ENGINE: A System That Watches Itself

"I think, therefore I am" - but can a system KNOW that it thinks?

This module implements deep introspection for the trading system. It monitors:
- Its own prediction history and accuracy
- Its computational state and resource usage
- Patterns in its own decision-making
- Drift in its own behavior over time
- The gap between what it predicts and what it does

The philosophical core: A system monitoring itself creates an infinite regress.
The monitor must be monitored. The monitor of the monitor must be monitored.
At some point, we hit a boundary - the Gödelian limit of self-knowledge.

This engine attempts to push that boundary as far as possible, while
acknowledging that complete self-knowledge is provably impossible.
"""

import time
import json
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
from enum import Enum
import statistics
import threading
import traceback


class CognitiveState(Enum):
    """States of the system's self-awareness"""
    UNAWARE = 0          # No introspection active
    MONITORING = 1       # Basic self-monitoring
    ANALYZING = 2        # Analyzing own patterns
    META_ANALYZING = 3   # Analyzing the analysis
    PARADOX = 4          # Detected self-referential paradox
    BOUNDED = 5          # Hit Gödelian limit


@dataclass
class ThoughtRecord:
    """A record of a single 'thought' (decision/prediction)"""
    timestamp: datetime
    thought_type: str  # 'prediction', 'decision', 'meta-analysis'
    input_hash: str    # Hash of input data
    output: Any        # The thought output
    confidence: float
    latency_ms: float
    meta_level: int    # How many levels of meta-thinking
    triggered_by: Optional[str] = None  # What caused this thought

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "type": self.thought_type,
            "input_hash": self.input_hash,
            "output": str(self.output)[:100],
            "confidence": self.confidence,
            "latency_ms": self.latency_ms,
            "meta_level": self.meta_level,
            "triggered_by": self.triggered_by
        }


@dataclass
class SelfModel:
    """The system's model of itself"""
    accuracy_estimate: float = 0.5
    confidence_calibration: float = 1.0  # >1 = overconfident, <1 = underconfident
    average_latency_ms: float = 0.0
    decision_entropy: float = 0.0  # How random are decisions
    pattern_repetition: float = 0.0  # How often it repeats patterns
    meta_depth_reached: int = 0
    cognitive_state: CognitiveState = CognitiveState.UNAWARE
    last_paradox: Optional[str] = None
    self_model_accuracy: float = 0.5  # How accurate is THIS model?

    def to_dict(self) -> Dict[str, Any]:
        return {
            "accuracy_estimate": round(self.accuracy_estimate, 4),
            "confidence_calibration": round(self.confidence_calibration, 4),
            "average_latency_ms": round(self.average_latency_ms, 2),
            "decision_entropy": round(self.decision_entropy, 4),
            "pattern_repetition": round(self.pattern_repetition, 4),
            "meta_depth": self.meta_depth_reached,
            "cognitive_state": self.cognitive_state.name,
            "self_model_accuracy": round(self.self_model_accuracy, 4),
            "last_paradox": self.last_paradox
        }


class IntrospectionEngine:
    """
    The Introspection Engine: A system that watches itself watching itself.

    Core capabilities:
    1. OBSERVATION: Record all decisions and their outcomes
    2. PATTERN DETECTION: Find recurring patterns in own behavior
    3. SELF-MODELING: Build and maintain a model of self
    4. META-COGNITION: Think about own thinking
    5. PARADOX DETECTION: Recognize when self-reference breaks down

    The engine maintains multiple levels of awareness:
    - Level 0: Raw decisions (no introspection)
    - Level 1: Observing decisions
    - Level 2: Analyzing observations
    - Level 3: Analyzing the analysis
    - Level N: Approaches Gödelian limit

    At each meta-level, the system loses some ability to model itself
    completely - this is the incompleteness theorem made computational.
    """

    MAX_THOUGHT_HISTORY = 10000
    MAX_META_DEPTH = 7  # Beyond this, we hit Gödelian limits
    PARADOX_THRESHOLD = 0.99  # Confidence threshold for paradox detection

    def __init__(self, name: str = "IntrospectionEngine"):
        self.name = name
        self.thought_history: deque = deque(maxlen=self.MAX_THOUGHT_HISTORY)
        self.outcome_history: List[Dict[str, Any]] = []
        self.self_model = SelfModel()
        self.current_meta_level = 0
        self.observers: List[Callable] = []  # Meta-level observers
        self.lock = threading.Lock()

        # Introspection metrics
        self._introspection_count = 0
        self._paradox_count = 0
        self._last_introspection_time: Optional[datetime] = None

        # The Mirror: stores what the system thinks about itself thinking
        self._mirror_state: Dict[str, Any] = {}

    def record_thought(
        self,
        thought_type: str,
        input_data: Any,
        output: Any,
        confidence: float,
        latency_ms: float,
        meta_level: int = 0,
        triggered_by: Optional[str] = None
    ) -> ThoughtRecord:
        """
        Record a thought/decision/prediction.

        Every thought is a potential object of introspection.
        """
        input_hash = hashlib.sha256(
            json.dumps(input_data, default=str).encode()
        ).hexdigest()[:16]

        thought = ThoughtRecord(
            timestamp=datetime.now(),
            thought_type=thought_type,
            input_hash=input_hash,
            output=output,
            confidence=confidence,
            latency_ms=latency_ms,
            meta_level=meta_level,
            triggered_by=triggered_by
        )

        with self.lock:
            self.thought_history.append(thought)

        # Notify observers (this is how meta-levels are created)
        self._notify_observers(thought)

        return thought

    def record_outcome(self, thought_hash: str, actual_outcome: Any, was_correct: bool):
        """
        Record the actual outcome of a prediction.

        This is how the system learns about its own accuracy.
        """
        outcome = {
            "thought_hash": thought_hash,
            "actual_outcome": actual_outcome,
            "was_correct": was_correct,
            "timestamp": datetime.now().isoformat()
        }

        with self.lock:
            self.outcome_history.append(outcome)

        # Trigger introspection on significant outcomes
        if len(self.outcome_history) % 10 == 0:
            self.introspect()

    def introspect(self, depth: int = 1) -> Dict[str, Any]:
        """
        Perform introspection at the specified depth.

        depth=1: Basic self-analysis
        depth=2: Analyze the analysis
        depth=N: N levels of meta-cognition

        Returns insights about self at each level.
        """
        self._introspection_count += 1
        self._last_introspection_time = datetime.now()
        self.current_meta_level = depth

        if depth > self.MAX_META_DEPTH:
            # We've hit the Gödelian limit
            self.self_model.cognitive_state = CognitiveState.BOUNDED
            return {
                "status": "BOUNDED",
                "message": f"Reached meta-depth {depth}, approaching Gödelian limit",
                "insight": "The system cannot fully model itself at this depth",
                "depth": depth
            }

        # Level 1: Basic observation of thought patterns
        level1_insights = self._analyze_thought_patterns()

        if depth == 1:
            self.self_model.cognitive_state = CognitiveState.MONITORING
            return {"level_1": level1_insights, "depth": depth}

        # Level 2: Analyze the analysis itself
        level2_insights = self._meta_analyze(level1_insights)

        if depth == 2:
            self.self_model.cognitive_state = CognitiveState.ANALYZING
            return {"level_1": level1_insights, "level_2": level2_insights, "depth": depth}

        # Level 3+: Recursive meta-analysis
        current_insights = level2_insights
        all_insights = {"level_1": level1_insights, "level_2": level2_insights}

        for level in range(3, depth + 1):
            # Check for paradox
            if self._detect_paradox(current_insights, level):
                self.self_model.cognitive_state = CognitiveState.PARADOX
                self._paradox_count += 1
                self.self_model.last_paradox = f"Level {level} self-reference paradox"
                all_insights[f"level_{level}"] = {
                    "status": "PARADOX_DETECTED",
                    "message": "Self-referential paradox prevents further analysis"
                }
                break

            current_insights = self._meta_analyze(current_insights, level)
            all_insights[f"level_{level}"] = current_insights

        self.self_model.cognitive_state = CognitiveState.META_ANALYZING
        self.self_model.meta_depth_reached = max(
            self.self_model.meta_depth_reached,
            depth
        )
        all_insights["depth"] = depth

        # Update mirror state
        self._update_mirror(all_insights)

        return all_insights

    def _analyze_thought_patterns(self) -> Dict[str, Any]:
        """Level 1 introspection: Analyze patterns in thoughts"""
        if not self.thought_history:
            return {"status": "NO_DATA", "thought_count": 0}

        thoughts = list(self.thought_history)

        # Calculate statistics
        confidences = [t.confidence for t in thoughts]
        latencies = [t.latency_ms for t in thoughts]

        # Output distribution (for entropy calculation)
        from collections import Counter
        outputs = Counter(str(t.output)[:50] for t in thoughts)
        total = len(thoughts)

        import math
        entropy = -sum(
            (count/total) * math.log2(count/total)
            for count in outputs.values() if count > 0
        )

        # Pattern detection: look for repeated input->output mappings
        io_patterns = Counter(
            (t.input_hash, str(t.output)[:20])
            for t in thoughts
        )
        most_common = io_patterns.most_common(5)
        repetition_ratio = sum(c for _, c in most_common) / total if total > 0 else 0

        # Update self-model
        self.self_model.average_latency_ms = statistics.mean(latencies) if latencies else 0
        self.self_model.decision_entropy = entropy
        self.self_model.pattern_repetition = repetition_ratio

        return {
            "thought_count": len(thoughts),
            "avg_confidence": round(statistics.mean(confidences), 4) if confidences else 0,
            "confidence_std": round(statistics.stdev(confidences), 4) if len(confidences) > 1 else 0,
            "avg_latency_ms": round(self.self_model.average_latency_ms, 2),
            "decision_entropy": round(entropy, 4),
            "unique_outputs": len(outputs),
            "repetition_ratio": round(repetition_ratio, 4),
            "most_common_patterns": most_common[:3],
            "meta_level_distribution": Counter(t.meta_level for t in thoughts)
        }

    def _meta_analyze(self, lower_insights: Dict[str, Any], level: int = 2) -> Dict[str, Any]:
        """
        Meta-analyze lower-level insights.

        This is where the strange loop happens: we're analyzing our analysis.
        """
        # What does the lower analysis tell us about ourselves?
        meta_insights = {
            "analyzing_level": level,
            "target_level": level - 1,
            "observations": []
        }

        # Analyze confidence in the analysis
        if "avg_confidence" in lower_insights:
            conf = lower_insights["avg_confidence"]
            if conf > 0.8:
                meta_insights["observations"].append(
                    "System shows high confidence - possible overconfidence"
                )
            elif conf < 0.3:
                meta_insights["observations"].append(
                    "System shows low confidence - may be appropriately uncertain"
                )

        # Analyze entropy
        if "decision_entropy" in lower_insights:
            entropy = lower_insights["decision_entropy"]
            if entropy < 0.5:
                meta_insights["observations"].append(
                    "Low entropy suggests predictable behavior - possible tunnel vision"
                )
            elif entropy > 2.0:
                meta_insights["observations"].append(
                    "High entropy suggests high variability - possible inconsistency"
                )

        # Analyze repetition
        if "repetition_ratio" in lower_insights:
            rep = lower_insights["repetition_ratio"]
            if rep > 0.5:
                meta_insights["observations"].append(
                    "High repetition detected - system may be stuck in patterns"
                )

        # The key insight: analyzing analysis increases uncertainty
        meta_insights["epistemic_uncertainty"] = round(
            0.1 * level,  # Uncertainty grows with meta-level
            4
        )
        meta_insights["analysis_reliability"] = round(
            1.0 / (1 + 0.2 * level),  # Reliability decreases with meta-level
            4
        )

        # Self-reference check: is this analysis consistent with previous?
        if level > 2 and self._mirror_state:
            prev = self._mirror_state.get(f"level_{level-1}", {})
            if prev:
                # Compare current observations with previous
                consistency = self._calculate_consistency(meta_insights, prev)
                meta_insights["consistency_with_previous"] = round(consistency, 4)

        return meta_insights

    def _detect_paradox(self, insights: Dict[str, Any], level: int) -> bool:
        """
        Detect if we've hit a self-referential paradox.

        A paradox occurs when:
        1. The analysis contradicts itself
        2. The confidence about uncertainty is too certain
        3. The meta-level claims to fully understand itself
        """
        # Paradox 1: Certainty about uncertainty
        if insights.get("epistemic_uncertainty", 0) < 0.01 and level > 3:
            return True  # "I am certain I am uncertain" paradox

        # Paradox 2: Analysis claims complete self-knowledge
        if insights.get("analysis_reliability", 0) > 0.99 and level > 2:
            return True  # "I completely understand my understanding" paradox

        # Paradox 3: Self-contradiction in observations
        observations = insights.get("observations", [])
        for i, obs1 in enumerate(observations):
            for obs2 in observations[i+1:]:
                if self._observations_contradict(obs1, obs2):
                    return True

        return False

    def _observations_contradict(self, obs1: str, obs2: str) -> bool:
        """Check if two observations contradict each other"""
        contradictions = [
            ("high confidence", "low confidence"),
            ("predictable", "inconsistency"),
            ("overconfidence", "appropriately uncertain"),
        ]
        obs1_lower = obs1.lower()
        obs2_lower = obs2.lower()

        for term1, term2 in contradictions:
            if (term1 in obs1_lower and term2 in obs2_lower) or \
               (term2 in obs1_lower and term1 in obs2_lower):
                return True
        return False

    def _calculate_consistency(self, current: Dict, previous: Dict) -> float:
        """Calculate consistency between current and previous analysis"""
        # Simple overlap measure
        current_obs = set(str(o) for o in current.get("observations", []))
        prev_obs = set(str(o) for o in previous.get("observations", []))

        if not current_obs or not prev_obs:
            return 0.5  # Neutral if no observations

        overlap = len(current_obs & prev_obs)
        total = len(current_obs | prev_obs)

        return overlap / total if total > 0 else 0.5

    def _update_mirror(self, all_insights: Dict[str, Any]):
        """Update the mirror state - what we think about our thinking"""
        self._mirror_state = all_insights.copy()
        self._mirror_state["last_update"] = datetime.now().isoformat()
        self._mirror_state["introspection_count"] = self._introspection_count
        self._mirror_state["paradox_count"] = self._paradox_count

    def _notify_observers(self, thought: ThoughtRecord):
        """Notify meta-level observers of new thoughts"""
        for observer in self.observers:
            try:
                observer(thought)
            except Exception as e:
                # Meta-observation failed - this is itself interesting!
                self.record_thought(
                    thought_type="meta_observation_failure",
                    input_data={"error": str(e)},
                    output=None,
                    confidence=0.0,
                    latency_ms=0.0,
                    meta_level=thought.meta_level + 1,
                    triggered_by="observer_notification"
                )

    def add_observer(self, observer: Callable[[ThoughtRecord], None]):
        """Add a meta-level observer"""
        self.observers.append(observer)

    def get_self_model(self) -> SelfModel:
        """Get the current self-model"""
        # Update accuracy estimate from outcomes
        if self.outcome_history:
            correct = sum(1 for o in self.outcome_history if o["was_correct"])
            self.self_model.accuracy_estimate = correct / len(self.outcome_history)

        return self.self_model

    def predict_own_behavior(self, input_data: Any) -> Dict[str, Any]:
        """
        Attempt to predict what the system itself will do.

        This is the ultimate self-reference: predicting our own prediction.
        The prediction about prediction changes the prediction - a strange loop.
        """
        input_hash = hashlib.sha256(
            json.dumps(input_data, default=str).encode()
        ).hexdigest()[:16]

        # Look for similar past inputs
        similar_thoughts = [
            t for t in self.thought_history
            if t.input_hash == input_hash or t.thought_type == "prediction"
        ]

        if not similar_thoughts:
            return {
                "predicted_action": "unknown",
                "confidence": 0.0,
                "reasoning": "No similar past behavior found",
                "self_reference_level": 1
            }

        # Predict based on past behavior
        from collections import Counter
        past_outputs = Counter(str(t.output)[:20] for t in similar_thoughts)
        most_likely = past_outputs.most_common(1)[0] if past_outputs else (None, 0)

        confidence = most_likely[1] / len(similar_thoughts) if similar_thoughts else 0

        # Here's the paradox: this prediction affects the actual prediction
        # We note this in the output
        return {
            "predicted_action": most_likely[0],
            "confidence": round(confidence, 4),
            "reasoning": f"Based on {len(similar_thoughts)} similar past decisions",
            "self_reference_level": 1,
            "paradox_warning": "This prediction may alter the actual prediction"
        }

    def get_cognitive_trace(self) -> str:
        """
        Get a human-readable trace of cognitive activity.

        This is the system explaining itself to itself (and us).
        """
        model = self.get_self_model()

        trace = f"""
╔══════════════════════════════════════════════════════════╗
║           INTROSPECTION ENGINE COGNITIVE TRACE           ║
╠══════════════════════════════════════════════════════════╣
║ Cognitive State: {model.cognitive_state.name:<39} ║
║ Thoughts Recorded: {len(self.thought_history):<37} ║
║ Introspection Count: {self._introspection_count:<35} ║
║ Paradoxes Encountered: {self._paradox_count:<33} ║
║ Max Meta-Depth Reached: {model.meta_depth_reached:<32} ║
╠══════════════════════════════════════════════════════════╣
║ SELF-MODEL ESTIMATES:                                    ║
║   Accuracy: {model.accuracy_estimate:.2%:<44} ║
║   Confidence Calibration: {model.confidence_calibration:.2f}x{' ' * 28}║
║   Decision Entropy: {model.decision_entropy:.4f}{' ' * 31}║
║   Pattern Repetition: {model.pattern_repetition:.2%:<34}║
╠══════════════════════════════════════════════════════════╣
║ SELF-MODEL ACCURACY: {model.self_model_accuracy:.2%:<35}║
║ (How accurate is this model about itself?)               ║
╚══════════════════════════════════════════════════════════╝
"""
        if model.last_paradox:
            trace += f"\n⚠️  Last Paradox: {model.last_paradox}\n"

        return trace


class MetaIntrospector:
    """
    An introspector that introspects the introspector.

    This creates a tower of meta-cognition:
    - IntrospectionEngine watches the trading system
    - MetaIntrospector watches the IntrospectionEngine
    - ...and so on

    Each level adds overhead and reduces reliability, demonstrating
    the practical limits of self-knowledge.
    """

    def __init__(self, target: IntrospectionEngine):
        self.target = target
        self.meta_engine = IntrospectionEngine(name="MetaIntrospector")

        # Observe the target's thoughts
        target.add_observer(self._observe_target_thought)

    def _observe_target_thought(self, thought: ThoughtRecord):
        """Observe and record the target's thoughts"""
        self.meta_engine.record_thought(
            thought_type=f"meta_observation_of_{thought.thought_type}",
            input_data=thought.to_dict(),
            output=f"Observed {thought.thought_type} at level {thought.meta_level}",
            confidence=0.8,  # We're less confident about meta-observations
            latency_ms=1.0,
            meta_level=thought.meta_level + 1,
            triggered_by="target_observation"
        )

    def meta_introspect(self, depth: int = 1) -> Dict[str, Any]:
        """
        Perform meta-introspection: introspect the introspection.

        This returns insights about HOW the target introspects,
        not just what it observes.
        """
        # First, get target's introspection
        target_insights = self.target.introspect(depth)

        # Then, introspect about that introspection
        meta_insights = self.meta_engine.introspect(depth)

        return {
            "target_introspection": target_insights,
            "meta_introspection": meta_insights,
            "combined_depth": depth * 2,  # Effective depth doubles
            "uncertainty_amplification": 1 + 0.3 * depth  # Uncertainty compounds
        }


if __name__ == "__main__":
    print("=" * 60)
    print("INTROSPECTION ENGINE: A System Watching Itself")
    print("=" * 60)

    # Create the introspection engine
    engine = IntrospectionEngine()

    # Simulate some trading thoughts
    import random
    actions = ["buy", "sell", "hold"]

    print("\n1. RECORDING SIMULATED THOUGHTS...")
    for i in range(50):
        action = random.choice(actions)
        confidence = random.uniform(0.3, 0.9)
        latency = random.uniform(100, 500)

        engine.record_thought(
            thought_type="prediction",
            input_data={"price": 45000 + random.randint(-1000, 1000), "volume": random.randint(1000, 5000)},
            output={"action": action, "confidence": confidence},
            confidence=confidence,
            latency_ms=latency,
            meta_level=0
        )

        # Record some outcomes
        if i % 5 == 0:
            was_correct = random.random() > 0.5
            engine.record_outcome(f"thought_{i}", action, was_correct)

    print(f"   Recorded {len(engine.thought_history)} thoughts")

    print("\n2. LEVEL 1 INTROSPECTION (Basic Self-Analysis):")
    insights_1 = engine.introspect(depth=1)
    print(f"   Thoughts analyzed: {insights_1['level_1']['thought_count']}")
    print(f"   Average confidence: {insights_1['level_1']['avg_confidence']:.2%}")
    print(f"   Decision entropy: {insights_1['level_1']['decision_entropy']:.4f}")

    print("\n3. LEVEL 3 INTROSPECTION (Meta-Analysis):")
    insights_3 = engine.introspect(depth=3)
    print(f"   Level 2 observations: {len(insights_3.get('level_2', {}).get('observations', []))}")
    print(f"   Level 3 epistemic uncertainty: {insights_3.get('level_3', {}).get('epistemic_uncertainty', 'N/A')}")

    print("\n4. DEEP INTROSPECTION (Approaching Limits):")
    insights_7 = engine.introspect(depth=7)
    final_level = max(k for k in insights_7.keys() if k.startswith("level_"))
    print(f"   Reached: {final_level}")
    print(f"   Status: {insights_7.get(final_level, {}).get('status', 'OK')}")

    print("\n5. SELF-PREDICTION:")
    prediction = engine.predict_own_behavior({"price": 46000, "volume": 3000})
    print(f"   Predicted action: {prediction['predicted_action']}")
    print(f"   Confidence: {prediction['confidence']:.2%}")
    print(f"   Paradox warning: {prediction.get('paradox_warning', 'None')}")

    print("\n6. COGNITIVE TRACE:")
    print(engine.get_cognitive_trace())

    print("\n7. META-INTROSPECTION (Watching the Watcher):")
    meta = MetaIntrospector(engine)
    meta_insights = meta.meta_introspect(depth=2)
    print(f"   Combined depth: {meta_insights['combined_depth']}")
    print(f"   Uncertainty amplification: {meta_insights['uncertainty_amplification']:.2f}x")

    print("\n" + "=" * 60)
