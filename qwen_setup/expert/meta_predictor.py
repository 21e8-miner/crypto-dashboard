"""
META-PREDICTOR: Predictions About Predictions

"To predict the predictor changes the prediction."

This module implements meta-prediction: the system predicting what it
will predict, then using those meta-predictions to modify its actual
predictions, which in turn affects future meta-predictions.

This creates a STRANGE LOOP - the quintessential Gödelian structure:

    Prediction → Meta-Prediction → Modified Prediction → New Meta-Prediction → ...

The profound insight: A system that predicts its own predictions creates
information that it cannot have predicted (because the act of prediction
changes the prediction). This is market reflexivity meets Gödel.

George Soros called this "reflexivity" in markets.
Douglas Hofstadter called these "strange loops" in consciousness.
We call it META-PREDICTION.
"""

import time
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
from enum import Enum
import statistics
import random


@dataclass
class Prediction:
    """A single prediction with metadata"""
    id: str
    timestamp: datetime
    input_data: Dict[str, Any]
    predicted_action: str
    confidence: float
    reasoning: str
    meta_level: int  # 0 = base prediction, 1+ = meta-predictions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.predicted_action,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "meta_level": self.meta_level
        }


@dataclass
class MetaPrediction:
    """A prediction ABOUT a prediction"""
    id: str
    timestamp: datetime
    target_prediction_id: str  # What prediction is this about?
    predicted_accuracy: float  # How accurate will the target be?
    predicted_confidence_calibration: float  # Will confidence match accuracy?
    meta_level: int
    strange_loop_detected: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "target": self.target_prediction_id,
            "predicted_accuracy": self.predicted_accuracy,
            "confidence_calibration": self.predicted_confidence_calibration,
            "meta_level": self.meta_level,
            "strange_loop": self.strange_loop_detected
        }


class RecursionMode(Enum):
    """How to handle recursive meta-prediction"""
    NONE = 0           # No meta-prediction
    SINGLE = 1         # One level of meta-prediction
    BOUNDED = 2        # Multiple levels with bound
    STRANGE_LOOP = 3   # Allow circular reference


class MetaPredictor:
    """
    The Meta-Predictor: A system that predicts its own predictions.

    Core Mechanics:
    1. BASE PREDICTION: Standard market prediction
    2. META-PREDICTION: Predict accuracy of base prediction
    3. MODIFICATION: Adjust base prediction based on meta-prediction
    4. RECURSION: Meta-predict the modification
    5. CONVERGENCE or DIVERGENCE: Loop stabilizes or explodes

    The Strange Loop:
    When the meta-prediction affects the base prediction, and the modified
    base prediction is what the meta-prediction was about, we have a strange
    loop. The prediction predicts itself predicting itself.

    This is computationally tractable (unlike true self-reference) but
    captures the essential strangeness of Gödel's insight.
    """

    MAX_RECURSION_DEPTH = 5
    CONVERGENCE_THRESHOLD = 0.01  # When to stop iterating

    def __init__(self, base_predictor: Optional[Callable] = None):
        """
        Initialize with an optional base predictor function.

        The base predictor should take market data and return a Prediction.
        If not provided, we use a simple momentum-based predictor.
        """
        self.base_predictor = base_predictor or self._default_predictor
        self.prediction_history: deque = deque(maxlen=1000)
        self.meta_prediction_history: deque = deque(maxlen=1000)
        self.accuracy_records: List[Dict[str, Any]] = []
        self.strange_loop_count = 0
        self.recursion_mode = RecursionMode.BOUNDED

    def _generate_id(self) -> str:
        """Generate unique prediction ID"""
        return hashlib.sha256(
            f"{datetime.now().isoformat()}_{random.random()}".encode()
        ).hexdigest()[:12]

    def _default_predictor(self, market_data: Dict[str, Any]) -> Prediction:
        """
        Default momentum-based predictor.

        This is a simple predictor that forms the base of the meta-prediction tower.
        """
        price = market_data.get("price", 0)
        prev_price = market_data.get("prev_price", price)
        volume = market_data.get("volume", 0)

        # Sanitize inputs
        import math
        if price is None or (isinstance(price, float) and (math.isnan(price) or math.isinf(price))):
            price = 0
        if prev_price is None or prev_price == 0 or (isinstance(prev_price, float) and (math.isnan(prev_price) or math.isinf(prev_price))):
            prev_price = price if price != 0 else 1  # Avoid division by zero

        # Simple momentum logic
        price_change = (price - prev_price) / prev_price if prev_price != 0 else 0

        if price_change > 0.02:
            action = "buy"
            confidence = min(0.9, 0.5 + price_change * 5)
            reasoning = "Strong upward momentum detected"
        elif price_change < -0.02:
            action = "sell"
            confidence = min(0.9, 0.5 + abs(price_change) * 5)
            reasoning = "Strong downward momentum detected"
        else:
            action = "hold"
            confidence = 0.5
            reasoning = "No clear momentum signal"

        return Prediction(
            id=self._generate_id(),
            timestamp=datetime.now(),
            input_data=market_data,
            predicted_action=action,
            confidence=confidence,
            reasoning=reasoning,
            meta_level=0
        )

    def make_base_prediction(self, market_data: Dict[str, Any]) -> Prediction:
        """Make a base-level prediction"""
        prediction = self.base_predictor(market_data)
        self.prediction_history.append(prediction)
        return prediction

    def make_meta_prediction(self, target: Prediction) -> MetaPrediction:
        """
        Make a prediction ABOUT a prediction.

        This analyzes:
        1. Historical accuracy of similar predictions
        2. Confidence calibration (does high confidence = high accuracy?)
        3. Market conditions that affect prediction reliability
        """
        # Analyze historical accuracy for similar predictions
        similar_preds = [
            p for p in self.accuracy_records
            if p["action"] == target.predicted_action
        ]

        if similar_preds:
            historical_accuracy = sum(
                p["was_correct"] for p in similar_preds
            ) / len(similar_preds)

            # Calculate confidence calibration
            avg_confidence = sum(p["confidence"] for p in similar_preds) / len(similar_preds)
            calibration = historical_accuracy / avg_confidence if avg_confidence > 0 else 1.0
        else:
            historical_accuracy = 0.5  # Prior assumption
            calibration = 1.0

        # Detect strange loop: is this prediction about a meta-prediction?
        strange_loop = target.meta_level > 0

        meta_pred = MetaPrediction(
            id=self._generate_id(),
            timestamp=datetime.now(),
            target_prediction_id=target.id,
            predicted_accuracy=historical_accuracy,
            predicted_confidence_calibration=calibration,
            meta_level=target.meta_level + 1,
            strange_loop_detected=strange_loop
        )

        if strange_loop:
            self.strange_loop_count += 1

        self.meta_prediction_history.append(meta_pred)
        return meta_pred

    def modify_prediction_from_meta(
        self,
        base_pred: Prediction,
        meta_pred: MetaPrediction
    ) -> Prediction:
        """
        Modify a base prediction based on its meta-prediction.

        This is where reflexivity happens:
        - If meta-pred says base will be inaccurate → reduce confidence
        - If meta-pred detects overconfidence → calibrate down
        - If meta-pred detects underconfidence → calibrate up

        The modification creates information that wasn't in the base prediction,
        which means future meta-predictions must account for this modification.
        """
        # Calculate modification factor
        accuracy_factor = meta_pred.predicted_accuracy
        calibration_factor = meta_pred.predicted_confidence_calibration

        # Modify confidence based on meta-prediction
        new_confidence = base_pred.confidence * accuracy_factor * calibration_factor
        new_confidence = max(0.1, min(0.95, new_confidence))  # Bound confidence

        # Potentially change action if confidence drops too low
        new_action = base_pred.predicted_action
        new_reasoning = base_pred.reasoning

        if new_confidence < 0.3 and base_pred.predicted_action != "hold":
            # Meta-prediction suggests we're not confident enough to act
            new_action = "hold"
            new_reasoning = f"Meta-analysis reduced confidence: {base_pred.reasoning}"

        # Create modified prediction (inherits meta-level from meta-prediction)
        return Prediction(
            id=self._generate_id(),
            timestamp=datetime.now(),
            input_data=base_pred.input_data,
            predicted_action=new_action,
            confidence=new_confidence,
            reasoning=new_reasoning,
            meta_level=meta_pred.meta_level
        )

    def recursive_meta_predict(
        self,
        market_data: Dict[str, Any],
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Perform recursive meta-prediction until convergence or max depth.

        This is the core strange loop:
        1. Make base prediction
        2. Meta-predict the base
        3. Modify base based on meta
        4. Meta-predict the modification
        5. Repeat until convergence or max depth

        Returns the full tower of predictions and the final converged prediction.
        """
        max_depth = max_depth or self.MAX_RECURSION_DEPTH

        # Start the tower
        tower = []
        base = self.make_base_prediction(market_data)
        tower.append({"level": 0, "prediction": base.to_dict(), "type": "base"})

        current_pred = base
        prev_confidence = base.confidence

        for depth in range(1, max_depth + 1):
            # Make meta-prediction about current prediction
            meta = self.make_meta_prediction(current_pred)
            tower.append({
                "level": depth,
                "meta_prediction": meta.to_dict(),
                "type": "meta"
            })

            # Modify prediction based on meta
            modified = self.modify_prediction_from_meta(current_pred, meta)
            tower.append({
                "level": depth,
                "prediction": modified.to_dict(),
                "type": "modified"
            })

            # Check for convergence
            confidence_change = abs(modified.confidence - prev_confidence)
            if confidence_change < self.CONVERGENCE_THRESHOLD:
                break

            prev_confidence = modified.confidence
            current_pred = modified

            # Check for strange loop divergence
            if meta.strange_loop_detected and depth > 2:
                # We're in a strange loop - behavior becomes unpredictable
                tower.append({
                    "level": depth,
                    "warning": "Strange loop detected - prediction stability uncertain",
                    "type": "warning"
                })

        # Record the final prediction
        final = current_pred
        self.prediction_history.append(final)

        return {
            "tower": tower,
            "final_prediction": final.to_dict(),
            "depth_reached": len([t for t in tower if t["type"] == "meta"]),
            "converged": len(tower) < max_depth * 2,
            "strange_loops_total": self.strange_loop_count
        }

    def record_outcome(self, prediction_id: str, was_correct: bool):
        """Record whether a prediction was correct"""
        # Find the prediction
        for pred in self.prediction_history:
            if pred.id == prediction_id:
                self.accuracy_records.append({
                    "id": prediction_id,
                    "action": pred.predicted_action,
                    "confidence": pred.confidence,
                    "meta_level": pred.meta_level,
                    "was_correct": was_correct,
                    "timestamp": datetime.now().isoformat()
                })
                break

    def get_accuracy_by_meta_level(self) -> Dict[int, float]:
        """
        Analyze accuracy at each meta-level.

        Key question: Does meta-prediction improve accuracy?

        Gödel suggests there's a limit - at some meta-level, additional
        analysis stops helping and may even hurt.
        """
        by_level: Dict[int, List[bool]] = {}

        for record in self.accuracy_records:
            level = record["meta_level"]
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(record["was_correct"])

        return {
            level: sum(records) / len(records) if records else 0
            for level, records in by_level.items()
        }

    def detect_reflexivity_impact(self) -> Dict[str, Any]:
        """
        Measure how much meta-prediction affects predictions.

        High reflexivity impact means the system is significantly
        changing its behavior based on self-analysis.
        """
        if len(self.prediction_history) < 10:
            return {"status": "insufficient_data", "prediction_count": len(self.prediction_history)}

        # Compare base predictions (level 0) with final predictions
        base_preds = [p for p in self.prediction_history if p.meta_level == 0]
        meta_preds = [p for p in self.prediction_history if p.meta_level > 0]

        if not base_preds or not meta_preds:
            return {"status": "insufficient_data"}

        # Calculate action change rate
        # (How often does meta-prediction change the action?)
        # Note: This is approximate since we don't track base→final pairs perfectly
        base_actions = [p.predicted_action for p in base_preds[-20:]]
        meta_actions = [p.predicted_action for p in meta_preds[-20:]]

        base_dist = {a: base_actions.count(a)/len(base_actions) for a in set(base_actions)}
        meta_dist = {a: meta_actions.count(a)/len(meta_actions) for a in set(meta_actions)}

        # Calculate distribution shift
        all_actions = set(base_dist.keys()) | set(meta_dist.keys())
        distribution_shift = sum(
            abs(base_dist.get(a, 0) - meta_dist.get(a, 0))
            for a in all_actions
        ) / 2  # Normalize to [0, 1]

        # Calculate confidence change
        base_conf = statistics.mean(p.confidence for p in base_preds[-20:])
        meta_conf = statistics.mean(p.confidence for p in meta_preds[-20:])
        confidence_shift = meta_conf - base_conf

        return {
            "status": "analyzed",
            "distribution_shift": round(distribution_shift, 4),
            "confidence_shift": round(confidence_shift, 4),
            "reflexivity_score": round(distribution_shift + abs(confidence_shift), 4),
            "interpretation": self._interpret_reflexivity(distribution_shift, confidence_shift)
        }

    def _interpret_reflexivity(self, dist_shift: float, conf_shift: float) -> str:
        """Interpret the reflexivity measurements"""
        if dist_shift < 0.1 and abs(conf_shift) < 0.1:
            return "Low reflexivity: Meta-prediction has minimal impact"
        elif dist_shift > 0.3:
            return "High reflexivity: Meta-prediction significantly changes actions"
        elif conf_shift < -0.2:
            return "Confidence dampening: Meta-prediction makes system more cautious"
        elif conf_shift > 0.2:
            return "Confidence amplification: Meta-prediction increases confidence"
        else:
            return "Moderate reflexivity: Meta-prediction has balanced impact"


class StrangeLoopGenerator:
    """
    Generate and analyze strange loops in prediction systems.

    A strange loop occurs when:
    - Level N predicts Level N-1
    - Level N-1 incorporates that prediction
    - Which changes what Level N would predict
    - Creating circular causation

    This is the computational analog of Gödel's self-referential sentence:
    "This prediction predicts that this prediction is unreliable."
    """

    def __init__(self):
        self.loops_generated = 0
        self.loop_history: List[Dict[str, Any]] = []

    def create_self_referential_prediction(
        self,
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a prediction that references itself.

        This is the trading equivalent of "This sentence is false."
        """
        loop_id = f"loop_{self.loops_generated}"
        self.loops_generated += 1

        # The strange loop: prediction about the prediction we're making
        loop = {
            "id": loop_id,
            "type": "self_referential_prediction",
            "timestamp": datetime.now().isoformat(),
            "market_data": market_data,
            "statement": "This prediction predicts its own accuracy",
            "layers": []
        }

        # Layer 0: What would we predict?
        base_action = "buy" if market_data.get("price", 0) > market_data.get("prev_price", 0) else "sell"
        loop["layers"].append({
            "level": 0,
            "content": f"Base prediction: {base_action}",
            "type": "base"
        })

        # Layer 1: What's the accuracy of that prediction?
        estimated_accuracy = 0.6  # Assume moderate accuracy
        loop["layers"].append({
            "level": 1,
            "content": f"Estimated accuracy: {estimated_accuracy:.0%}",
            "type": "meta"
        })

        # Layer 2: But knowing the accuracy changes our confidence
        adjusted_confidence = 0.5 * (1 + estimated_accuracy)
        loop["layers"].append({
            "level": 2,
            "content": f"Adjusted confidence: {adjusted_confidence:.2f}",
            "type": "adjustment"
        })

        # Layer 3: But that adjustment changes the accuracy estimate
        # (Because we're now more/less likely to act, affecting outcomes)
        new_accuracy = estimated_accuracy * (0.5 + 0.5 * adjusted_confidence)
        loop["layers"].append({
            "level": 3,
            "content": f"Re-estimated accuracy: {new_accuracy:.2%}",
            "type": "re-meta"
        })

        # The paradox emerges: the loop doesn't converge cleanly
        loop["paradox"] = {
            "detected": abs(new_accuracy - estimated_accuracy) > 0.1,
            "message": "Self-reference creates instability in accuracy estimates",
            "godel_parallel": "Like Gödel's sentence, we cannot consistently assign "
                            "truth (accuracy) to a self-referential statement"
        }

        self.loop_history.append(loop)
        return loop

    def analyze_loop_stability(self, iterations: int = 10) -> Dict[str, Any]:
        """
        Analyze whether strange loops stabilize or diverge.

        Some strange loops reach a fixed point.
        Others oscillate.
        Others diverge.

        This mirrors the behavior of recursive functions and the
        connection to the halting problem.
        """
        results = []

        # Create a simple feedback loop
        accuracy = 0.5
        confidence = 0.5

        for i in range(iterations):
            # Meta-prediction: confidence based on accuracy
            new_confidence = 0.3 + 0.7 * accuracy

            # Reflexivity: accuracy based on confidence
            # (High confidence → more aggressive → sometimes worse accuracy)
            new_accuracy = 0.4 + 0.4 * confidence - 0.1 * confidence ** 2

            results.append({
                "iteration": i,
                "accuracy": round(accuracy, 4),
                "confidence": round(confidence, 4),
                "change": round(abs(new_accuracy - accuracy) + abs(new_confidence - confidence), 4)
            })

            accuracy = new_accuracy
            confidence = new_confidence

        # Determine stability
        final_change = results[-1]["change"]
        stability = "stable" if final_change < 0.01 else "oscillating" if final_change < 0.1 else "diverging"

        return {
            "iterations": iterations,
            "trajectory": results,
            "final_accuracy": round(accuracy, 4),
            "final_confidence": round(confidence, 4),
            "stability": stability,
            "insight": self._stability_insight(stability)
        }

    def _stability_insight(self, stability: str) -> str:
        """Provide insight about loop stability"""
        insights = {
            "stable": "The strange loop reached a fixed point - a consistent self-model emerged",
            "oscillating": "The strange loop oscillates - self-knowledge fluctuates perpetually",
            "diverging": "The strange loop diverges - self-reference leads to instability"
        }
        return insights.get(stability, "Unknown stability pattern")


if __name__ == "__main__":
    print("=" * 60)
    print("META-PREDICTOR: Predictions About Predictions")
    print("=" * 60)

    # Create meta-predictor
    mp = MetaPredictor()

    # Simulate market data sequence
    market_sequence = [
        {"price": 45000, "prev_price": 44500, "volume": 1000000},
        {"price": 45200, "prev_price": 45000, "volume": 1200000},
        {"price": 44800, "prev_price": 45200, "volume": 800000},
        {"price": 44600, "prev_price": 44800, "volume": 900000},
        {"price": 45100, "prev_price": 44600, "volume": 1500000},
    ]

    print("\n1. RECURSIVE META-PREDICTION TOWER:")
    for i, market_data in enumerate(market_sequence[:2]):
        print(f"\n   Market state {i+1}: price=${market_data['price']}")
        result = mp.recursive_meta_predict(market_data, max_depth=4)

        print(f"   Final action: {result['final_prediction']['action']}")
        print(f"   Final confidence: {result['final_prediction']['confidence']:.2%}")
        print(f"   Tower depth: {result['depth_reached']}")
        print(f"   Converged: {result['converged']}")

        # Show the tower
        for layer in result['tower'][:6]:  # First 6 layers
            if layer['type'] == 'base':
                print(f"      L{layer['level']} [BASE] {layer['prediction']['action']} "
                      f"({layer['prediction']['confidence']:.2%})")
            elif layer['type'] == 'meta':
                print(f"      L{layer['level']} [META] predicted_accuracy="
                      f"{layer['meta_prediction']['predicted_accuracy']:.2%}")
            elif layer['type'] == 'modified':
                print(f"      L{layer['level']} [MOD]  {layer['prediction']['action']} "
                      f"({layer['prediction']['confidence']:.2%})")

    # Record some outcomes
    print("\n2. RECORDING OUTCOMES...")
    for pred in list(mp.prediction_history)[:5]:
        was_correct = random.random() > 0.4  # 60% accuracy simulation
        mp.record_outcome(pred.id, was_correct)
    print(f"   Recorded {len(mp.accuracy_records)} outcomes")

    print("\n3. ACCURACY BY META-LEVEL:")
    accuracy_by_level = mp.get_accuracy_by_meta_level()
    for level, acc in sorted(accuracy_by_level.items()):
        print(f"   Level {level}: {acc:.2%}")

    print("\n4. REFLEXIVITY IMPACT ANALYSIS:")
    # Generate more data
    for market_data in market_sequence * 5:
        mp.recursive_meta_predict(market_data, max_depth=3)
        for pred in list(mp.prediction_history)[-3:]:
            mp.record_outcome(pred.id, random.random() > 0.4)

    reflexivity = mp.detect_reflexivity_impact()
    print(f"   Distribution shift: {reflexivity.get('distribution_shift', 'N/A')}")
    print(f"   Confidence shift: {reflexivity.get('confidence_shift', 'N/A')}")
    print(f"   Reflexivity score: {reflexivity.get('reflexivity_score', 'N/A')}")
    print(f"   Interpretation: {reflexivity.get('interpretation', 'N/A')}")

    print("\n5. STRANGE LOOP GENERATION:")
    slg = StrangeLoopGenerator()
    loop = slg.create_self_referential_prediction(market_sequence[0])
    print(f"   Loop ID: {loop['id']}")
    print(f"   Statement: {loop['statement']}")
    for layer in loop['layers']:
        print(f"      Layer {layer['level']}: {layer['content']}")
    print(f"   Paradox detected: {loop['paradox']['detected']}")
    print(f"   Gödel parallel: {loop['paradox']['godel_parallel'][:60]}...")

    print("\n6. LOOP STABILITY ANALYSIS:")
    stability = slg.analyze_loop_stability(iterations=20)
    print(f"   Final accuracy: {stability['final_accuracy']:.2%}")
    print(f"   Final confidence: {stability['final_confidence']:.2%}")
    print(f"   Stability: {stability['stability']}")
    print(f"   Insight: {stability['insight']}")

    print("\n" + "=" * 60)
