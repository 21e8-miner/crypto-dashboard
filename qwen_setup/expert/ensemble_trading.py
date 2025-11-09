#!/usr/bin/env python3
"""
Ensemble Trading with Multiple LLM Queries
Improves weak model accuracy via consensus
"""

import json
import sys
from pathlib import Path
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from client import QwenClient
    # Try to connect to real server
    test_client = QwenClient()
    if not test_client.health_check():
        print("⚠️  No Qwen server detected. Using mock client for testing.")
        from mock_client import MockQwenClient as QwenClient
except Exception:
    print("⚠️  No Qwen server detected. Using mock client for testing.")
    from mock_client import MockQwenClient as QwenClient


class EnsembleTrader:
    def __init__(self, base_client, num_models=5):
        self.base_client = base_client
        self.num_models = num_models

        # Different "personalities" for diversity
        self.personalities = [
            "aggressive day trader",
            "conservative swing trader",
            "quantitative analyst",
            "momentum trader",
            "contrarian investor"
        ]

    def ensemble_predict(self, symbol, data):
        """Get predictions from multiple perspectives"""
        predictions = []

        for i in range(self.num_models):
            personality = self.personalities[i % len(self.personalities)]

            prompt = f"""You are a {personality}. Analyze {symbol}:
Data: {data}
Output ONLY: {{"action": "buy/sell/hold", "confidence": 1-10}}"""

            response = self.base_client.complete(prompt, max_tokens=100)

            try:
                pred = json.loads(response)
                predictions.append({
                    "action": pred["action"],
                    "confidence": pred.get("confidence", 5),
                    "personality": personality
                })
            except:
                continue

        # Consensus voting
        actions = [p["action"] for p in predictions]
        confidence_scores = [p["confidence"] for p in predictions]

        if not actions:
            return {
                "consensus_action": "hold",
                "consensus_votes": 0,
                "total_models": 0,
                "avg_confidence": 0,
                "individual_predictions": [],
                "diversity_score": 0
            }

        consensus = Counter(actions).most_common(1)[0]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)

        return {
            "consensus_action": consensus[0],
            "consensus_votes": consensus[1],
            "total_models": len(predictions),
            "avg_confidence": avg_confidence,
            "individual_predictions": predictions,
            "diversity_score": len(set(actions))  # Lower is better (more agreement)
        }


# Test
if __name__ == "__main__":
    client = QwenClient()
    ensemble = EnsembleTrader(client, num_models=5)

    # Test data
    test_data = "c:45000 v:2.5B c:46000 v:3.1B c:47000 v:2.8B"

    print("🎯 Ensemble Trading Test")
    print("=" * 60)
    result = ensemble.ensemble_predict("BTCUSDT", test_data)

    print(f"\n📊 Consensus: {result['consensus_action'].upper()}")
    print(f"Votes: {result['consensus_votes']}/{result['total_models']}")
    print(f"Avg Confidence: {result['avg_confidence']:.1f}/10")
    print(f"Diversity: {result['diversity_score']} (lower = more agreement)")

    print("\n🗳️ Individual Predictions:")
    for pred in result['individual_predictions']:
        print(f"  {pred['personality']}: {pred['action']} (confidence: {pred['confidence']})")
