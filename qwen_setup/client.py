#!/usr/bin/env python3
"""
Qwen Client Library

Easy-to-use client for interacting with self-hosted Qwen API.
Compatible with both OpenAI-style and custom endpoints.
"""

import argparse
import json
import sys
from typing import List, Dict, Optional, Any

try:
    import requests
except ImportError:
    print("Error: requests not installed. Install with:")
    print("  pip install requests")
    sys.exit(1)


class QwenClient:
    """Client for interacting with Qwen LLM API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the Qwen client.

        Args:
            base_url: Base URL of the Qwen API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def complete(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Get a completion from the model.

        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)

        Returns:
            Generated text
        """
        # Try OpenAI-compatible endpoint first
        try:
            response = self.session.post(
                f"{self.base_url}/v1/completions",
                json={
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0].get("text", "")

        except requests.exceptions.RequestException:
            pass

        # Try simple /generate endpoint
        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json={
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if "text" in data:
                    return data["text"]
                elif "response" in data:
                    return data["response"]
                elif "generated_text" in data:
                    return data["generated_text"]

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Qwen API at {self.base_url}: {e}")

        raise Exception(f"Unexpected API response format from {self.base_url}")

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated response
        """
        try:
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            # Fallback: convert messages to simple prompt
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            return self.complete(prompt, max_tokens, temperature)

        raise Exception("Failed to get chat completion")

    def health_check(self) -> bool:
        """
        Check if the API server is running.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def list_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of model names
        """
        try:
            response = self.session.get(f"{self.base_url}/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "models" in data:
                    return data["models"]
        except requests.exceptions.RequestException:
            pass

        return []

    def analyze_code(self, code: str, question: str = "What does this code do?") -> str:
        """
        Analyze code with the LLM.

        Args:
            code: Code to analyze
            question: Question about the code

        Returns:
            Analysis response
        """
        prompt = f"""Analyze this code:

```
{code}
```

{question}"""

        return self.complete(prompt, max_tokens=600)

    def debug_code(self, code: str, error: str = "") -> str:
        """
        Get debugging help from the LLM.

        Args:
            code: Code with issue
            error: Error message (if any)

        Returns:
            Debugging suggestions
        """
        prompt = f"""Debug this code:

```
{code}
```
"""
        if error:
            prompt += f"\nError: {error}"

        prompt += "\n\nWhat's wrong and how to fix it?"

        return self.complete(prompt, max_tokens=600)

    def explain_concept(self, concept: str, level: str = "beginner") -> str:
        """
        Get explanation of a concept.

        Args:
            concept: Concept to explain
            level: Difficulty level (beginner, intermediate, expert)

        Returns:
            Explanation
        """
        prompt = f"Explain {concept} for a {level} level audience."
        return self.complete(prompt, max_tokens=500)


def main():
    """Command-line interface for the Qwen client"""
    parser = argparse.ArgumentParser(description="Qwen LLM Client")
    parser.add_argument("--base-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--prompt", help="Single prompt to send")
    parser.add_argument("--interactive", action="store_true", help="Interactive chat mode")
    parser.add_argument("--analyze-code", help="Code to analyze")
    parser.add_argument("--debug-code", help="Code to debug")
    parser.add_argument("--error", help="Error message for debugging")
    parser.add_argument("--max-tokens", type=int, default=500, help="Max tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")

    args = parser.parse_args()

    client = QwenClient(base_url=args.base_url)

    # Check health
    if not client.health_check():
        print(f"⚠️  Warning: Could not connect to Qwen API at {args.base_url}")
        print("Make sure the server is running.")
        print()

    if args.prompt:
        # Single prompt mode
        print("🤖 Qwen Response:")
        print("-" * 60)
        response = client.complete(args.prompt, max_tokens=args.max_tokens, temperature=args.temperature)
        print(response)
        print()

    elif args.analyze_code:
        # Code analysis mode
        print("🔍 Code Analysis:")
        print("-" * 60)
        response = client.analyze_code(args.analyze_code)
        print(response)
        print()

    elif args.debug_code:
        # Debug mode
        print("🐛 Debug Suggestions:")
        print("-" * 60)
        response = client.debug_code(args.debug_code, args.error or "")
        print(response)
        print()

    elif args.interactive:
        # Interactive chat mode
        print("💬 Interactive Chat Mode")
        print("Type 'exit' or 'quit' to end the conversation")
        print("-" * 60)

        messages = []

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                messages.append({"role": "user", "content": user_input})

                print("\nQwen: ", end="", flush=True)
                response = client.chat(messages, max_tokens=args.max_tokens, temperature=args.temperature)
                print(response)

                messages.append({"role": "assistant", "content": response})

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")

    else:
        # No arguments - show help
        parser.print_help()


if __name__ == "__main__":
    main()
