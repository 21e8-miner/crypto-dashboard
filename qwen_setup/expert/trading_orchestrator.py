#!/usr/bin/env python3
"""
Zero-Cost Trading Orchestrator
Manages entire pipeline: data → analysis → decision → execution
All local, all free, all private

Enhanced with optional agent integration:
- EnsembleTrader: Multi-perspective consensus voting
- GodelMachine: Meta-cognitive incompleteness detection
"""

import json
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scraper_config import ZeroCostScraper
from prompt_compression import TradingPromptCompressor
from client import QwenClient

# Optional agent imports
try:
    from ensemble_trading import EnsembleTrader
    ENSEMBLE_AVAILABLE = True
except ImportError:
    ENSEMBLE_AVAILABLE = False

try:
    from godel_machine import GodelMachine
    GODEL_AVAILABLE = True
except ImportError:
    GODEL_AVAILABLE = False


class TradingOrchestrator:
    """
    Zero-Cost Trading Orchestrator with optional agent integration.

    Modes:
    - basic: Original LLM-only mode
    - ensemble: Add consensus voting (improves accuracy)
    - godel: Add meta-cognitive analysis (detects unknowable states)
    - full: All agents integrated
    """

    VERSION = "2.0.0"

    def __init__(self, config_path="./trading_config.json", mode="basic"):
        self.mode = mode

        # Load config if exists, otherwise use defaults
        if Path(config_path).exists():
            self.config = json.loads(Path(config_path).read_text())
        else:
            self.config = {
                "paper_trading": True,
                "symbols": ["BTCUSDT", "ETHUSDT"],
                "interval": "1h",
                "max_position_size": 1000,
                "stop_loss_pct": 2.0,
                "mode": mode
            }

        self.scraper = ZeroCostScraper()
        self.compressor = TradingPromptCompressor()
        self.llm = QwenClient()

        # Initialize optional agents based on mode
        self.ensemble: Optional[EnsembleTrader] = None
        self.godel: Optional[GodelMachine] = None

        if mode in ["ensemble", "full"] and ENSEMBLE_AVAILABLE:
            self.ensemble = EnsembleTrader(self.llm, num_models=5)
            print(f"[AGENT] EnsembleTrader initialized")

        if mode in ["godel", "full"] and GODEL_AVAILABLE:
            self.godel = GodelMachine(
                name="OrchestratorGodel",
                enable_self_improvement=True
            )
            print(f"[AGENT] GodelMachine initialized")

        # Trading state
        self.state = {
            "positions": {},
            "trades_history": [],
            "last_analysis": None
        }

        # Performance tracking
        self.perf = {
            "queries_per_minute": 0,
            "avg_latency_ms": 0,
            "tokens_generated": 0,
            "total_queries": 0,
            "abstentions": 0,
            "ensemble_agreements": 0
        }

        print(f"[ORCHESTRATOR] Mode: {mode.upper()} | Agents: {self._get_agents()}")

    def _get_agents(self) -> str:
        """Get list of active agents"""
        agents = ["LLM"]
        if self.ensemble:
            agents.append("Ensemble")
        if self.godel:
            agents.append("Godel")
        return " + ".join(agents)

    def pipeline(self, symbol, interval="1h"):
        """Single analysis pipeline iteration with optional agent integration"""
        start = time.time()

        print(f"\n{'='*60}")
        print(f"🔄 Pipeline Execution: {symbol} @ {datetime.now()}")
        print(f"   Mode: {self.mode.upper()} | Agents: {self._get_agents()}")
        print(f"{'='*60}")

        # 1. Data acquisition (zero-cost)
        print("📡 Step 1: Data Acquisition...")
        raw_data = self.scraper.get_crypto_ohlcv(symbol, interval)

        if not raw_data:
            print("❌ Failed to fetch data")
            return None

        print(f"✅ Retrieved {len(raw_data)} candles")

        # 2. Data compression (context optimization)
        print("🗜️  Step 2: Data Compression...")
        compressed = self.compressor.compress_ohlcv(raw_data)
        indicators = self.compressor.extract_key_indicators(raw_data)

        print(f"✅ Compressed to {len(compressed)} data points")
        print(f"   Current Price: ${indicators.get('current_price', 0):,.2f}")
        print(f"   24h Change: {indicators.get('price_change_pct', 0):+.2f}%")

        # 3. Prompt engineering (maximize 1.5B model utility)
        print("📝 Step 3: Prompt Engineering...")
        prompt = self.build_trading_prompt(symbol, compressed, indicators)

        # 4. LLM inference (local, free)
        print("🤖 Step 4: LLM Inference...")
        analysis = self.llm.complete(prompt, max_tokens=400)

        print(f"✅ Generated analysis ({len(analysis)} chars)")

        # 5. Decision parsing (structured output)
        print("🎯 Step 5: Decision Parsing...")
        decision = self.parse_llm_output(analysis)

        print(f"✅ Basic Decision: {decision['action'].upper()}")
        print(f"   Confidence: {decision.get('confidence', 0)}/10")

        # 5a. Ensemble consensus (if enabled)
        if self.ensemble:
            print("🗳️  Step 5a: Ensemble Consensus...")
            data_str = " ".join([f"c:{c['c']:.0f} v:{c['v']:.0f}" for c in compressed[-5:]])
            ensemble_result = self.ensemble.ensemble_predict(symbol, data_str)

            print(f"   Ensemble: {ensemble_result['consensus_action'].upper()} "
                  f"({ensemble_result['consensus_votes']}/{ensemble_result['total_models']} votes)")

            # Override decision if strong consensus
            if ensemble_result['consensus_votes'] >= 4:
                decision['action'] = ensemble_result['consensus_action']
                decision['confidence'] = ensemble_result['avg_confidence']
                decision['ensemble_votes'] = ensemble_result['consensus_votes']

                if ensemble_result['diversity_score'] == 1:
                    self.perf['ensemble_agreements'] += 1

        # 5b. Godel meta-cognitive analysis (if enabled)
        if self.godel:
            print("🔮 Step 5b: Godel Meta-Cognitive Analysis...")
            price = indicators.get('current_price', 0)

            market_data = {
                "price": price,
                "prev_price": indicators.get('prev_price', price),
                "volume": indicators.get('volume', 0),
                "rsi": indicators.get('rsi', 50),
                "macd": indicators.get('macd', 0),
                "momentum": indicators.get('momentum', 0),
                "trend": 1 if price > indicators.get('sma_20', price) else -1
            }

            godel_decision = self.godel.process_market_state(market_data)

            print(f"   Godel: {godel_decision.action.upper()} "
                  f"(meta-confidence: {godel_decision.meta_confidence:.0%})")

            if godel_decision.incompleteness_detected:
                print(f"   ⚠️  INCOMPLETENESS: {godel_decision.incompleteness_type.name}")

            # Handle abstention
            if godel_decision.action == "abstain":
                decision['action'] = "hold"
                decision['confidence'] = 0
                decision['reason'] = f"ABSTAIN: {godel_decision.reasoning[:100]}"
                decision['incompleteness'] = True
                self.perf['abstentions'] += 1
            else:
                # Weight confidence by meta-confidence
                decision['meta_confidence'] = godel_decision.meta_confidence
                decision['godel_number'] = godel_decision.godel_number

        print(f"✅ Final Decision: {decision['action'].upper()}")
        print(f"   Reason: {decision.get('reason', 'N/A')[:100]}")

        # 6. Execution (if enabled)
        if self.config.get("paper_trading", True):
            print("💼 Step 6: Paper Trade Execution...")
            self.execute_paper_trade(decision, symbol, indicators.get('current_price', 0))

        # Performance logging
        latency = (time.time() - start) * 1000
        self.perf['total_queries'] += 1
        self.perf['avg_latency_ms'] = (
            (self.perf['avg_latency_ms'] * (self.perf['total_queries'] - 1) + latency) /
            self.perf['total_queries']
        )

        print(f"\n⏱️  Pipeline Latency: {latency:.0f}ms")
        print(f"📊 Avg Latency: {self.perf['avg_latency_ms']:.0f}ms")

        return decision

    def build_trading_prompt(self, symbol, compressed_data, indicators):
        """Expert-level prompt engineering for weak model"""

        # Few-shot examples embedded in prompt (improves 1.5B performance)
        few_shot = """Examples:
Q: BTC c:45000 v:1.2B c:45200 v:1.3B c:45100 v:1.1B
A: {"action": "hold", "reason": "consolidation", "confidence": 3}

Q: BTC c:40000 v:2.5B c:41000 v:3.1B c:42000 v:2.8B
A: {"action": "buy", "reason": "volume breakout", "confidence": 7}

Q: BTC c:50000 v:0.8B c:49500 v:0.9B c:49000 v:1.2B
A: {"action": "sell", "reason": "high volume selloff", "confidence": 6}
"""

        # Current market data (last 5 candles)
        current = " ".join([f"c:{c['c']:.0f} v:{c['v']:.0f}" for c in compressed_data[-5:]])

        # Add indicators
        sma_10 = indicators.get('sma_10', 0)
        sma_20 = indicators.get('sma_20', 0)
        price = indicators.get('current_price', 0)

        trend = "bullish" if price > sma_20 else "bearish"

        # Role forcing + structured output requirement
        prompt = f"""You are a trading bot. Analyze:
Symbol: {symbol}
Trend: {trend} (price vs SMA20)
Recent: {current}

{few_shot}

Q: {symbol} {current}
A:"""

        return prompt

    def parse_llm_output(self, raw_output):
        """Parse structured output from LLM"""
        try:
            # Try to extract JSON if model produced it
            if "{" in raw_output:
                json_str = raw_output[raw_output.find("{"):raw_output.rfind("}")+1]
                return json.loads(json_str)
        except:
            pass

        # Fallback: pattern matching
        output = raw_output.lower()
        if "buy" in output:
            return {"action": "buy", "reason": raw_output[:200], "confidence": 5}
        elif "sell" in output:
            return {"action": "sell", "reason": raw_output[:200], "confidence": 5}

        return {"action": "hold", "reason": "unclear signal", "confidence": 2}

    def execute_paper_trade(self, decision, symbol, price):
        """Simulate trade execution"""
        if decision['action'] == 'hold':
            print("   ⏸️  Holding position")
            return

        trade = {
            "symbol": symbol,
            "action": decision['action'],
            "timestamp": datetime.now().isoformat(),
            "confidence": decision.get('confidence', 0),
            "price": price,
            "reason": decision.get('reason', 'N/A')[:100]
        }

        self.state['trades_history'].append(trade)

        # Log to file
        log_file = Path("trades_log.jsonl")
        with log_file.open("a") as f:
            f.write(json.dumps(trade) + "\n")

        print(f"   📝 PAPER TRADE: {trade['action'].upper()} {symbol} at ${trade['price']:,.2f}")

    def run_continuous(self, interval_seconds=300):
        """Run continuous analysis loop"""
        print("🚀 Starting Continuous Trading Orchestrator")
        print(f"Symbols: {self.config.get('symbols', [])}")
        print(f"Interval: {interval_seconds}s")
        print(f"Paper Trading: {self.config.get('paper_trading', True)}")
        print(f"\nPress Ctrl+C to stop\n")

        iteration = 0
        while True:
            try:
                iteration += 1
                print(f"\n{'#'*60}")
                print(f"Iteration #{iteration} @ {datetime.now()}")
                print(f"{'#'*60}")

                for symbol in self.config.get('symbols', ['BTCUSDT']):
                    decision = self.pipeline(symbol, self.config.get('interval', '1h'))
                    time.sleep(2)  # Small delay between symbols

                print(f"\n⏳ Sleeping {interval_seconds}s until next iteration...")
                time.sleep(interval_seconds)

            except KeyboardInterrupt:
                print("\n\n⛔ Stopped by user")
                self.print_summary()
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                time.sleep(60)

    def print_summary(self):
        """Print trading summary"""
        print(f"\n{'='*60}")
        print("📊 TRADING SUMMARY")
        print(f"{'='*60}")
        print(f"Total Queries: {self.perf['total_queries']}")
        print(f"Avg Latency: {self.perf['avg_latency_ms']:.0f}ms")
        print(f"Total Trades: {len(self.state['trades_history'])}")

        # Analyze trades
        if self.state['trades_history']:
            buys = sum(1 for t in self.state['trades_history'] if t['action'] == 'buy')
            sells = sum(1 for t in self.state['trades_history'] if t['action'] == 'sell')

            print(f"\nBuys: {buys}")
            print(f"Sells: {sells}")

            print(f"\nTrades log saved to: trades_log.jsonl")


# Usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Zero-Cost Trading Orchestrator")
    parser.add_argument("--symbol", default="BTCUSDT", help="Trading symbol")
    parser.add_argument("--interval", default="1h", help="Candle interval")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--sleep", type=int, default=300, help="Sleep between iterations (seconds)")
    parser.add_argument("--mode", default="basic",
                        choices=["basic", "ensemble", "godel", "full"],
                        help="Trading mode: basic, ensemble, godel, or full")

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"TRADING ORCHESTRATOR v2.0")
    print(f"Mode: {args.mode.upper()}")
    print(f"{'='*60}\n")

    orchestrator = TradingOrchestrator(mode=args.mode)

    if args.continuous:
        orchestrator.run_continuous(interval_seconds=args.sleep)
    else:
        # Single run
        decision = orchestrator.pipeline(args.symbol, args.interval)
        print(f"\n🎯 Final Decision: {json.dumps(decision, indent=2)}")
