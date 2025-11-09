#!/usr/bin/env python3
"""
Compress market data to fit in limited context
Qwen2-1.5B has 8K token context - every token counts
"""

import re
import json
from typing import List, Dict, Any


class TradingPromptCompressor:
    def __init__(self, max_tokens=6000):  # Leave buffer for response
        self.max_tokens = max_tokens

    def compress_ohlcv(self, candles, max_candles=50):
        """Compress OHLCV data to essential info only"""
        if not candles:
            return []

        compressed = []
        for candle in candles[-max_candles:]:
            # Only keep: timestamp, close, volume, high/low spread
            try:
                compressed.append({
                    "t": candle[0],  # timestamp
                    "c": float(candle[4]),  # close
                    "v": float(candle[5]),  # volume
                    "r": float(candle[2]) - float(candle[3])  # high-low range
                })
            except (IndexError, ValueError):
                continue

        return compressed

    def compress_orderbook(self, orderbook, levels=5):
        """Compress orderbook to top N levels"""
        # Binance orderbook format: {"lastUpdateId": ..., "bids": [[price, qty], ...], "asks": [...]}
        try:
            return {
                "bids": orderbook.get("bids", [])[:levels],
                "asks": orderbook.get("asks", [])[:levels],
                "spread": float(orderbook.get("asks", [[0]])[0][0]) - float(orderbook.get("bids", [[0]])[0][0])
            }
        except (IndexError, ValueError):
            return {"bids": [], "asks": [], "spread": 0}

    def build_efficient_prompt(self, symbol, compressed_data, analysis_type):
        """Build minimal but effective prompt"""

        if analysis_type == "sentiment":
            return f"""Analyze: {symbol} | V:{compressed_data.get('volume', 0)} C:{compressed_data.get('close', 0):.2f} | News:{compressed_data.get('news', 'None')}"""

        elif analysis_type == "technical":
            if isinstance(compressed_data, list):
                ohlcv_str = " ".join([f"c:{c['c']:.0f} v:{c['v']:.0f}" for c in compressed_data[-10:]])
                return f"""TA {symbol} {ohlcv_str} What are key levels?"""
            else:
                return f"""TA {symbol} | No data available"""

        return "Invalid analysis type"

    def compress_multiasset(self, assets_data: Dict[str, List]) -> str:
        """Compress multi-asset portfolio data into minimal prompt"""
        compressed = []
        for symbol, candles in assets_data.items():
            if candles and len(candles) > 0:
                latest = candles[-1]
                try:
                    compressed.append(f"{symbol}:c{float(latest[4]):.0f}v{float(latest[5]):.0f}")
                except (IndexError, ValueError):
                    continue

        return " | ".join(compressed)

    def extract_key_indicators(self, ohlcv_data: List) -> Dict[str, Any]:
        """Extract key technical indicators in compressed form"""
        if not ohlcv_data or len(ohlcv_data) < 20:
            return {"error": "insufficient data"}

        closes = [float(c[4]) for c in ohlcv_data[-20:]]
        volumes = [float(c[5]) for c in ohlcv_data[-20:]]

        # Simple indicators that don't require external libs
        return {
            "sma_10": sum(closes[-10:]) / 10,
            "sma_20": sum(closes[-20:]) / 20,
            "avg_vol": sum(volumes) / len(volumes),
            "current_price": closes[-1],
            "price_change_pct": ((closes[-1] - closes[0]) / closes[0]) * 100,
            "vol_change_pct": ((volumes[-1] - sum(volumes[:-1])/len(volumes[:-1])) / (sum(volumes[:-1])/len(volumes[:-1]))) * 100 if len(volumes) > 1 else 0
        }


# This can fit 100+ candles in <500 tokens

if __name__ == "__main__":
    compressor = TradingPromptCompressor()

    # Test compression
    test_candles = [
        [1699000000000, "45000", "45200", "44900", "45100", "1200000000"],
        [1699003600000, "45100", "45300", "45000", "45200", "1350000000"],
        [1699007200000, "45200", "45400", "45100", "45300", "1180000000"]
    ]

    compressed = compressor.compress_ohlcv(test_candles)
    print("Compressed OHLCV:")
    print(json.dumps(compressed, indent=2))

    indicators = compressor.extract_key_indicators(test_candles * 10)  # Simulate 30 candles
    print("\nKey Indicators:")
    print(json.dumps(indicators, indent=2))

    prompt = compressor.build_efficient_prompt("BTCUSDT", compressed, "technical")
    print(f"\nEfficient Prompt ({len(prompt)} chars):")
    print(prompt)
