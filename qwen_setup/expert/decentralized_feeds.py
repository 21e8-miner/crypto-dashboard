#!/usr/bin/env python3
"""
Decentralized Data Feeds - Uncensorable, Zero-Cost
Uses P2P networks and blockchain oracles
"""

import json
from typing import Optional, Dict


try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    print("Warning: web3 not installed. Install with: pip install web3")


class DecentralizedData:
    def __init__(self, rpc_url="https://rpc.ankr.com/eth"):  # Free RPC
        if not WEB3_AVAILABLE:
            self.w3 = None
            print("Web3 not available - decentralized feeds disabled")
            return

        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Chainlink Price Feeds (free to read on-chain)
        # https://docs.chain.link/data-feeds/price-feeds/addresses
        self.chainlink_feeds = {
            "BTC/USD": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
            "ETH/USD": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
            "LINK/USD": "0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c",
            "USDC/USD": "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6"
        }

        # ABI for Chainlink aggregator
        self.chainlink_abi = json.loads('''[
            {
                "inputs": [],
                "name": "latestRoundData",
                "outputs": [
                    {"internalType": "uint80", "name": "roundId", "type": "uint80"},
                    {"internalType": "int256", "name": "answer", "type": "int256"},
                    {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
                    {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
                    {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "decimals",
                "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]''')

    def get_chainlink_price(self, pair: str) -> Optional[Dict]:
        """Read from Chainlink oracle - truly decentralized, zero-cost"""
        if not WEB3_AVAILABLE or self.w3 is None:
            return None

        if pair not in self.chainlink_feeds:
            return None

        try:
            feed_address = self.chainlink_feeds[pair]
            contract = self.w3.eth.contract(address=feed_address, abi=self.chainlink_abi)

            # Get latest price data
            round_id, answer, started_at, updated_at, answered_in_round = contract.functions.latestRoundData().call()

            # Get decimals for proper scaling
            decimals = contract.functions.decimals().call()

            # Calculate price
            price = answer / (10 ** decimals)

            return {
                "pair": pair,
                "price": price,
                "timestamp": updated_at,
                "round_id": round_id,
                "source": "chainlink",
                "network": "ethereum"
            }
        except Exception as e:
            print(f"Error fetching {pair}: {e}")
            return None

    def get_uniswap_price(self, token_address: str) -> Optional[Dict]:
        """
        Get price from Uniswap V2/V3 pools
        Requires more complex logic - placeholder for now
        """
        # TODO: Implement Uniswap price feed
        # Would read reserves from Uniswap pool contracts
        # Completely on-chain, zero-cost
        pass

    def get_multiple_feeds(self, pairs: list) -> Dict[str, Dict]:
        """Get prices for multiple pairs"""
        results = {}
        for pair in pairs:
            price_data = self.get_chainlink_price(pair)
            if price_data:
                results[pair] = price_data
        return results


# This is actually unstoppable - no central authority can block this data feed

if __name__ == "__main__":
    print("🔗 Decentralized Data Feeds Test")
    print("=" * 60)

    dex_data = DecentralizedData()

    if not WEB3_AVAILABLE:
        print("Install web3: pip install web3")
    else:
        # Test Chainlink feeds
        pairs = ["BTC/USD", "ETH/USD", "LINK/USD"]

        print("\n📊 Chainlink Price Feeds (On-Chain):")
        for pair in pairs:
            data = dex_data.get_chainlink_price(pair)
            if data:
                print(f"{pair}: ${data['price']:,.2f} (updated: {data['timestamp']})")
            else:
                print(f"{pair}: Failed to fetch")

        print("\n💡 Note: These prices are read directly from Ethereum mainnet")
        print("   - Zero cost (only RPC call)")
        print("   - Uncensorable")
        print("   - Verifiable on-chain")
