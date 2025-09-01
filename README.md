# 📊 Crypto Arbitrage Monitor

A lightweight Python project that connects to Binance and Kraken APIs to monitor BTC/USDT prices in real time and detect arbitrage opportunities. The project is fully containerized with Docker for easy deployment and reproducibility.

---

## 🚀 Features

* Fetches live bid/ask prices from Binance and Kraken.
* Detects arbitrage spreads above a configurable threshold.
* Simulates profit per BTC (without executing trades).
* Logs results with timestamp into a CSV file.
* Runs locally or inside Docker with one command.

---

## 🛠 How to Run

### Run Locally

```bash
pip install -r requirements.txt
python arbitrage_monitor.py
```

### Run with Docker

Build the image:

```bash
docker build -t arbitrage-monitor .
```

Run the container:

```bash
docker run --rm arbitrage-monitor
```

Save CSV to your local folder:

```bash
docker run --rm -v ${PWD}:/app arbitrage-monitor
```

---

## 📂 Project Structure

```
crypto-arbitrage-monitor/
│── arbitrage_monitor.py   # Main script
│── requirements.txt       # Python dependencies
│── Dockerfile             # Container setup
│── arbitrage_log.csv      # Logged opportunities (sample)
│── README.md              # Project documentation
```

---

## 🧑‍💻 Example Output

```
Starting Crypto Arbitrage Monitor...
[2025-09-01 11:56:13+00:00] Binance: bid=108835.27 ask=108835.28 | Kraken: bid=108804.9 ask=108805.0
💰 Arbitrage opportunity found:
timestamp                 buy_exchange  sell_exchange  spread_%  profit_per_BTC
2025-09-01 11:56:13+00:00 kraken        binance        0.028     30.37
```

---

## 🌍 Future Extensions

* CI/CD with GitHub Actions (scheduled runs).
* Deploy to cloud for 24/7 monitoring.
* Add Streamlit dashboard for live visualization.
* Backtesting with historical data.

---

## 📜 License

MIT License
