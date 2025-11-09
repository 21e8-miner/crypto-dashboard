#!/usr/bin/env python3
"""
Benchmark Qwen2-1.5B Trading Performance
Measure accuracy, latency, and token efficiency
"""

import json
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from client import QwenClient


class TradingBenchmark:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.results = []

        # Test scenarios with known outcomes
        self.test_cases = [
            {
                "description": "Clear uptrend with high volume",
                "data": "c:40000 v:2B c:41000 v:2.5B c:42000 v:3B c:43000 v:2.8B",
                "expected": "buy",
                "rationale": "Trend continuation"
            },
            {
                "description": "Overbought RSI divergence",
                "data": "c:45000 v:1B c:45500 v:0.8B c:45200 v:0.7B c:45100 v:0.6B",
                "expected": "sell",
                "rationale": "Weak momentum"
            },
            {
                "description": "Consolidation pattern",
                "data": "c:44000 v:1B c:44100 v:1.1B c:44050 v:1B c:44150 v:1.1B",
                "expected": "hold",
                "rationale": "No clear direction"
            },
            {
                "description": "Volume spike on breakout",
                "data": "c:43000 v:1B c:43100 v:1.2B c:44000 v:3.5B c:44500 v:2.8B",
                "expected": "buy",
                "rationale": "Breakout confirmed by volume"
            },
            {
                "description": "Failed rally into resistance",
                "data": "c:46000 v:2B c:47000 v:1.5B c:46500 v:1.2B c:46000 v:0.9B",
                "expected": "sell",
                "rationale": "Rejection at resistance"
            }
        ]

    def run_benchmark(self, iterations=10):
        """Run multiple test scenarios"""
        print("🏁 Benchmarking Qwen2-1.5B Trading Performance")
        print("=" * 60)

        total_latency = 0
        total_tokens = 0
        correct_predictions = 0
        total_tests = 0

        for i in range(iterations):
            print(f"\n{'='*60}")
            print(f"Iteration {i+1}/{iterations}")
            print(f"{'='*60}")

            for case in self.test_cases:
                # Build prompt
                prompt = f"""Analyze: {case['data']}

What action? buy/sell/hold
Output format: {{"action": "xxx", "confidence": 1-10}}"""

                # Measure performance
                start = time.time()
                response = self.llm.complete(prompt, max_tokens=100)
                latency = (time.time() - start) * 1000

                # Parse and evaluate
                try:
                    # Try to extract JSON
                    if "{" in response:
                        json_str = response[response.find("{"):response.rfind("}")+1]
                        result = json.loads(json_str)
                    else:
                        # Fallback parsing
                        result = {"action": "unknown", "confidence": 0}

                    predicted = result.get("action", "unknown")
                    confidence = result.get("confidence", 0)

                    if predicted == case["expected"]:
                        correct_predictions += 1
                        status = "✅"
                    else:
                        status = "❌"

                    print(f"{status} {case['description']}")
                    print(f"  Expected: {case['expected']}, Got: {predicted} (confidence: {confidence})")
                    print(f"  Latency: {latency:.0f}ms")

                    total_latency += latency
                    total_tokens += len(response.split())
                    total_tests += 1

                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {response[:100]}...")
                    total_tests += 1
                except Exception as e:
                    print(f"❌ Error: {e}")
                    total_tests += 1

        # Summary
        if total_tests > 0:
            accuracy = (correct_predictions / total_tests) * 100
            avg_latency = total_latency / total_tests
            avg_tokens = total_tokens / total_tests
            qpm = 60000 / avg_latency if avg_latency > 0 else 0

            print(f"\n{'='*60}")
            print(f"📊 BENCHMARK RESULTS:")
            print(f"{'='*60}")
            print(f"Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_tests})")
            print(f"Avg Latency: {avg_latency:.0f}ms")
            print(f"Avg Tokens: {avg_tokens:.0f}")
            print(f"Queries/minute: {qpm:.1f}")

            results = {
                "timestamp": datetime.now().isoformat(),
                "iterations": iterations,
                "total_tests": total_tests,
                "correct_predictions": correct_predictions,
                "accuracy": accuracy,
                "avg_latency_ms": avg_latency,
                "avg_tokens": avg_tokens,
                "qpm": qpm
            }

            return results
        else:
            return {"error": "No tests completed"}

    def stress_test(self, duration_seconds=60):
        """Stress test: How many queries can we handle?"""
        print(f"\n🔥 Stress Test: {duration_seconds}s")
        print("=" * 60)

        start_time = time.time()
        query_count = 0
        errors = 0

        simple_prompt = "Analyze: c:45000 v:1B c:45100 v:1.1B. Output: {action: buy/sell/hold}"

        while (time.time() - start_time) < duration_seconds:
            try:
                response = self.llm.complete(simple_prompt, max_tokens=50)
                query_count += 1

                if query_count % 5 == 0:
                    elapsed = time.time() - start_time
                    qpm = (query_count / elapsed) * 60
                    print(f"Queries: {query_count} | QP M: {qpm:.1f} | Elapsed: {elapsed:.1f}s")

            except Exception as e:
                errors += 1
                print(f"Error: {e}")

        total_time = time.time() - start_time
        qpm = (query_count / total_time) * 60

        print(f"\n📊 Stress Test Results:")
        print(f"Total Queries: {query_count}")
        print(f"Total Time: {total_time:.1f}s")
        print(f"Queries/minute: {qpm:.1f}")
        print(f"Errors: {errors}")

        return {
            "duration": total_time,
            "queries": query_count,
            "qpm": qpm,
            "errors": errors
        }


# Run benchmark
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Benchmark trading LLM")
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations")
    parser.add_argument("--stress", action="store_true", help="Run stress test")
    parser.add_argument("--duration", type=int, default=60, help="Stress test duration (seconds)")

    args = parser.parse_args()

    client = QwenClient()
    benchmark = TradingBenchmark(client)

    if args.stress:
        stress_results = benchmark.stress_test(duration_seconds=args.duration)
        Path("stress_test_results.json").write_text(json.dumps(stress_results, indent=2))
    else:
        results = benchmark.run_benchmark(iterations=args.iterations)

        # Save results
        Path("benchmark_results.json").write_text(json.dumps(results, indent=2))

        print(f"\n💾 Results saved to benchmark_results.json")
