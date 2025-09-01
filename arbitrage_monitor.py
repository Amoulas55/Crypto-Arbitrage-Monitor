import requests
import time
import pandas as pd
from datetime import datetime, timezone

# API endpoints
EXCHANGES = {
    "binance": "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSDT"  # Kraken uses XBT for BTC
}

THRESHOLD = 0.001  # % spread threshold (set low so we always log something)


def fetch_prices():
    prices = {}
    try:
        # Binance
        b = requests.get(EXCHANGES["binance"]).json()
        if "bidPrice" in b and "askPrice" in b:
            prices["binance_bid"] = float(b["bidPrice"])
            prices["binance_ask"] = float(b["askPrice"])
        else:
            print("⚠️ Binance response did not contain bid/ask:", b)
            return {}

        # Kraken
        k = requests.get(EXCHANGES["kraken"]).json()
        if "result" in k and len(k["result"]) > 0:
            k_data = list(k["result"].values())[0]
            prices["kraken_bid"] = float(k_data["b"][0])
            prices["kraken_ask"] = float(k_data["a"][0])
        else:
            print("⚠️ Kraken response did not contain prices:", k)
            return {}

    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}

    return prices


def check_spread(prices):
    results = []
    if not prices or "kraken_bid" not in prices or "binance_bid" not in prices:
        return results

    # Buy Binance → Sell Kraken
    spread1 = (prices["kraken_bid"] - prices["binance_ask"]) / prices["binance_ask"] * 100
    if spread1 > THRESHOLD:
        profit = prices["kraken_bid"] - prices["binance_ask"]
        results.append(("binance", "kraken", spread1, profit))

    # Buy Kraken → Sell Binance
    spread2 = (prices["binance_bid"] - prices["kraken_ask"]) / prices["kraken_ask"] * 100
    if spread2 > THRESHOLD:
        profit = prices["binance_bid"] - prices["kraken_ask"]
        results.append(("kraken", "binance", spread2, profit))

    return results


def main():
    print("Starting Crypto Arbitrage Monitor...")

    all_results = []
    for i in range(5):  # run 5 iterations for faster CI/CD runs
        prices = fetch_prices()
        if prices:
            results = check_spread(prices)
            if results:
                all_results.extend([{
                    "timestamp": datetime.now(timezone.utc),
                    "buy_exchange": r[0],
                    "sell_exchange": r[1],
                    "spread_%": round(r[2], 3),
                    "profit_per_BTC": round(r[3], 2),
                    "binance_bid": prices["binance_bid"],
                    "binance_ask": prices["binance_ask"],
                    "kraken_bid": prices["kraken_bid"],
                    "kraken_ask": prices["kraken_ask"]
                } for r in results])
        time.sleep(5)

    # ✅ Always save a CSV (even empty)
    df = pd.DataFrame(all_results)
    df.to_csv("arbitrage_log.csv", index=False)

    if df.empty:
        print("⚠️ No arbitrage opportunities found this run.")
    else:
        print("💰 Final Arbitrage Results:")
        print(df)

    print("✅ Finished monitor. Exiting.")


if __name__ == "__main__":
    main()
