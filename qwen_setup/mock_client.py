#!/usr/bin/env python3
"""
Mock Qwen Client for Testing

Simulates LLM responses for testing when no server is available.
Used for benchmarking and development without running actual model.
"""

import json
import random
import time
from typing import List, Dict


class MockQwenClient:
    """Mock client that simulates LLM responses for testing"""

    def __init__(self, base_url: str = "http://localhost:8000", latency_ms: int = 8000):
        """
        Initialize mock client.

        Args:
            base_url: Ignored (for compatibility)
            latency_ms: Simulated latency in milliseconds (default: 8000ms = 8s)
        """
        self.base_url = base_url
        self.latency_ms = latency_ms

    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Simulate a completion.

        Args:
            prompt: The prompt (analyzed for keywords)
            max_tokens: Ignored
            temperature: Affects randomness of response

        Returns:
            Simulated response based on prompt analysis
        """
        # Simulate network latency
        time.sleep(self.latency_ms / 1000.0)

        # Parse prompt for trading signals
        prompt_lower = prompt.lower()

        # Check for price/volume patterns
        is_uptrend = any(x in prompt_lower for x in ['c:41000 v:2.5b', 'c:42000 v:3b', 'c:43000'])
        is_downtrend = any(x in prompt_lower for x in ['c:49500 v:0.9b', 'c:49000', 'weak momentum'])
        is_consolidation = any(x in prompt_lower for x in ['c:44000', 'c:44100', 'c:44050'])

        # Determine action with some randomness
        if is_uptrend:
            actions = ['buy'] * 7 + ['hold'] * 2 + ['sell'] * 1  # 70% buy
            confidence = random.randint(6, 9)
        elif is_downtrend:
            actions = ['sell'] * 7 + ['hold'] * 2 + ['buy'] * 1  # 70% sell
            confidence = random.randint(5, 8)
        elif is_consolidation:
            actions = ['hold'] * 7 + ['buy'] * 2 + ['sell'] * 1  # 70% hold
            confidence = random.randint(3, 6)
        else:
            # Random guess
            actions = ['buy', 'sell', 'hold']
            confidence = random.randint(3, 7)

        # Add temperature-based randomness
        if temperature > 0.5:
            # Higher temperature = more random
            action = random.choice(actions)
        else:
            # Lower temperature = more deterministic
            action = actions[0] if actions else 'hold'

        # Generate response in expected format
        response = {
            "action": action,
            "confidence": confidence
        }

        return json.dumps(response)

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Simulate chat completion.

        Args:
            messages: Conversation messages
            max_tokens: Ignored
            temperature: Sampling temperature

        Returns:
            Simulated chat response
        """
        # Use last message as prompt
        last_message = messages[-1]["content"] if messages else ""
        return self.complete(last_message, max_tokens, temperature)

    def health_check(self) -> bool:
        """Always returns True for mock"""
        return True

    def list_models(self) -> List[str]:
        """Returns mock model list"""
        return ["Mock-Qwen2-1.5B-Instruct"]

    def analyze_code(self, code: str, question: str = "What does this code do?") -> str:
        """Mock code analysis"""
        time.sleep(self.latency_ms / 1000.0)
        return "This code implements a trading function. It appears to use technical indicators for analysis."

    def debug_code(self, code: str, error: str = "") -> str:
        """Mock code debugging"""
        time.sleep(self.latency_ms / 1000.0)
        return "The code looks correct. The error might be related to missing dependencies or incorrect input format."

    def explain_concept(self, concept: str, level: str = "beginner") -> str:
        """Mock concept explanation"""
        time.sleep(self.latency_ms / 1000.0)
        return f"{concept} is a concept in trading. It involves analyzing market data to make informed decisions."


if __name__ == "__main__":
    # Test the mock client
    print("Testing Mock Qwen Client")
    print("=" * 60)

    client = MockQwenClient(latency_ms=100)  # Fast for testing

    # Test uptrend
    prompt1 = "Analyze: c:40000 v:2B c:41000 v:2.5B c:42000 v:3B\nAction?"
    print(f"\nPrompt: {prompt1}")
    print(f"Response: {client.complete(prompt1)}")

    # Test downtrend
    prompt2 = "Analyze: c:50000 v:0.8B c:49500 v:0.9B c:49000 v:1.2B\nAction?"
    print(f"\nPrompt: {prompt2}")
    print(f"Response: {client.complete(prompt2)}")

    # Test consolidation
    prompt3 = "Analyze: c:44000 v:1B c:44100 v:1.1B c:44050 v:1B\nAction?"
    print(f"\nPrompt: {prompt3}")
    print(f"Response: {client.complete(prompt3)}")

    print("\n✅ Mock client working correctly")
