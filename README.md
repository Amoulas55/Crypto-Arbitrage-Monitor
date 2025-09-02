# 📊 Crypto Arbitrage Monitor

A lightweight Python project that connects to Binance and Kraken APIs to monitor BTC/USDT prices in real time and detect arbitrage opportunities. The project is fully containerized with Docker for easy deployment and reproducibility.

---

## 🚀 Features

* Fetches live bid/ask prices from Binance and Kraken.
* Detects arbitrage spreads above a configurable threshold.
* Simulates profit per BTC (without executing trades).
* Logs results with timestamp into a CSV file.
* Runs locally, inside Docker, or automatically via GitHub Actions. ✅

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

## ⚙️ CI/CD with GitHub Actions (Scheduled Runs)

This project includes a **GitHub Actions workflow** that runs the monitor automatically on a schedule.

* The workflow installs dependencies, runs the script, and uploads the results as an artifact.
* By default, it runs at **23:20 UTC every day**, but you can adjust the `cron` schedule in `.github/workflows/run.yml`.
* Artifacts (CSV logs) can be downloaded from the **Actions tab** in your repository.

Example snippet from `.github/workflows/run.yml`:

```yaml
name: Run Arbitrage Monitor

on:
  schedule:
    - cron: "20 23 * * *"   # Runs daily at 23:20 UTC
  workflow_dispatch:         # Allow manual runs

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python arbitrage_monitor.py
      - uses: actions/upload-artifact@v4
        with:
          name: arbitrage-results
          path: arbitrage_log.csv
```

---

## 📂 Project Structure

```
crypto-arbitrage-monitor/
│── arbitrage_monitor.py   # Main script
│── requirements.txt       # Python dependencies
│── Dockerfile             # Container setup
│── arbitrage_log.csv      # Logged opportunities (sample)
│── .github/workflows/     # CI/CD workflows
│   └── run.yml
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

* Deploy to cloud for 24/7 monitoring.
* Add Streamlit dashboard for live visualization.
* Backtesting with historical data.

---

## 📜 License

MIT License
