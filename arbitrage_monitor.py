import requests
import time
import pandas as pd
from datetime import datetime, timezone

# API endpoints
EXCHANGES = {
    # ✅ Binance Testnet (no regional restrictions)
    "binance": "https://testnet.binance.vision/api/v3/ticker/bookTicker?symbol=BTCUSDT",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=XBTUSDT"  # Kraken uses XBT for BTC
}

THRESHOLD = 0.001  # % spread threshold (set low so we always log something)

def fetch_prices():
    prices = {}
    try:
        # Binance Testnet
        b = requests.get(EXCHANGES["binance"]).json()
        if "bidPrice" in b and "askPrice" in b:
            prices["binance_bid"] = float(b["bidPrice"])
            prices["binance_ask"] = float(b["askPrice"])
        else:
            print("⚠️ Binance response did not contain bid/ask:", b)

        # Kraken
        k = requests.get(EXCHANGES["kraken"]).json()
        if "result" in k and len(k["result"]) > 0:
            k_data = list(k["result"].values())[0]
            prices["kraken_bid"] = float(k_data["b"][0])
            prices["kraken_ask"] = float(k_data["a"][0])
        else:
            print("⚠️ Kraken response did not contain prices:", k)

    except Exception as e:
        print(f"Error fetching prices: {e}")
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

def log_results(results, prices):
    # Always show current prices
    print(f"[{datetime.now(timezone.utc)}] Binance: bid={prices.get('binance_bid')} ask={prices.get('binance_ask')} | "
          f"Kraken: bid={prices.get('kraken_bid')} ask={prices.get('kraken_ask')}")

    if not results:
        print("⚠️ No arbitrage opportunities found this run.")
        return

    df = pd.DataFrame([{
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

    # ✅ Overwrite CSV each run
    df.to_csv("arbitrage_log.csv", index=False)
    print("💰 Arbitrage opportunity found:")
    print(df)

def main():
    print("Starting Crypto Arbitrage Monitor...")

    all_results = []
    for i in range(5):  # run only 5 iterations for CI/CD demo
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
        time.sleep(5)  # shorter delay for CI/CD

    # ✅ Save all results at once (overwrite file)
    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv("arbitrage_log.csv", index=False)
        print("💰 Final Arbitrage Results:")
        print(df)
    else:
        print("⚠️ No arbitrage opportunities found across all runs.")

    print("✅ Finished monitor. Exiting.")

if __name__ == "__main__":
    main()
