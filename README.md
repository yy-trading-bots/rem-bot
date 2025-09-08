<div align="center">
  <img src="assets/rembot.png" alt="RemBot Project Cover">
</div>

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Coverage 96.80%](https://img.shields.io/badge/coverage-96.80%25-brightgreen.svg)](#)
[![CI](https://github.com/yy-trading-bots/rem-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/yy-trading-bots/rem-bot/actions/workflows/ci.yml)
[![license](https://img.shields.io/github/license/yy-trading-bots/rem-bot)](https://github.com/yy-trading-bots/rem-bot/blob/master/LICENSE)

# RemBot

> An automated crypto trading bot for **Binance** that combines **R**SI, **E**MA, and **M**ACD — the **REM** trio — to generate confluence-based LONG/SHORT signals.

---

## 📖 Description

RemBot is a Python trading bot that connects to the Binance API and opens LONG or SHORT positions when REM (RSI, EMA, MACD) conditions are met. It uses clear abstractions with object‑oriented design and pragmatic design patterns to keep the codebase clean and maintainable without sacrificing functionality. The project also serves as a concise reference implementation for developers building their own trading bots.

---

## 🎯 Strategy

> **REM = RSI + EMA + MACD**

A typical configuration uses:

- **Trend filter (EMA)** – e.g., price relative to `EMA_100` to determine bullish/bearish bias.
- **Momentum (MACD)** – e.g., MACD line vs. signal line and the zero line.
- **Momentum (RSI)** – e.g., a short-period RSI threshold around 50 to confirm momentum direction.

**Illustrative decision flow (pseudocode):**

```py
while True:
    if price > EMA_100 and MACD_line crosses_above signal and RSI > 50:
        enter_long()
    elif price < EMA_100 and MACD_line crosses_below signal and RSI < 50:
        enter_short()

    manage_position(tp_ratio=TP_RATIO, sl_ratio=SL_RATIO, leverage=LEVERAGE)
```

> You can tune lookback windows, thresholds, and scheduling via configuration.

---

For a video explanation of the strategy, you may see the video below. (The video does not belong to this repository or organisation)

<div align="center">
  <a href="https://www.youtube.com/watch?v=Gs-_tleyz3Q&ab_channel=TRADEEMPIRE"><img src="assets/strategy.jpg" alt="Strategy Reference" width="600"> </a>
</div>

## ⚙️ Configuration

First, rename `settings.example.toml` to **`settings.toml`** and edit the fields to match your preferences.

| Key              | Section      |    Type |           Default | Description                                                                                   | Example               |
| ---------------- | ------------ | ------: | ----------------: | --------------------------------------------------------------------------------------------- | --------------------- |
| `PUBLIC_KEY`     | `[API]`      |  string |              `""` | Your Binance API key. Grant only the permissions you actually need. **Do not commit to VCS.** | `"AKIA..."`           |
| `SECRET_KEY`     | `[API]`      |  string |              `""` | Your Binance API secret. Keep it secret and out of the repo.                                  | `"wJalrXUtnFEMI..."`  |
| `SYMBOL`         | `[POSITION]` |  string |       `"ETHUSDT"` | Trading symbol (e.g., USDT-M futures or spot pair).                                           | `"BTCUSDT"`           |
| `COIN_PRECISION` | `[POSITION]` | integer |               `2` | Quantity precision for orders. Must align with the exchange **lot size** rules.               | `3`                   |
| `TP_RATIO`       | `[POSITION]` |   float |          `0.0050` | Take-profit distance **relative to entry**. `0.0050` = **0.5%**.                              | `0.0100`              |
| `SL_RATIO`       | `[POSITION]` |   float |          `0.0050` | Stop-loss distance **relative to entry**. `0.0050` = **0.5%**.                                | `0.0075`              |
| `LEVERAGE`       | `[POSITION]` | integer |               `1` | Leverage to apply (for futures). Use responsibly.                                             | `5`                   |
| `TEST_MODE`      | `[RUNTIME]`  |    bool |            `true` | Paper/Test mode. When `true`, no live orders are sent (or a testnet is used).                 | `false`               |
| `DEBUG_MODE`     | `[RUNTIME]`  |    bool |           `false` | Verbose logging and extra assertions.                                                         | `true`                |
| `INTERVAL`       | `[RUNTIME]`  |  string |           `"15m"` | Indicator/candle interval (e.g., `1m`, `5m`, `15m`, `1h`, ...).                               | `"1h"`                |
| `SLEEP_DURATION` | `[RUNTIME]`  |   float |            `30.0` | Delay (seconds) between loops to respect API limits.                                          | `10.0`                |
| `CSV_PATH`       | `[OUTPUT]`   |  string | `"./results.csv"` | Path where trade/position logs are written.                                                   | `"./logs/trades.csv"` |

**Where to get API keys:** Binance → **API Management**: [https://www.binance.com/en/my/settings/api-management](https://www.binance.com/en/my/settings/api-management)

> Tips
>
> - Keep `COIN_PRECISION` in sync with `exchangeInfo` (lot/tick size) to avoid rejected orders.

---

## ▶️ How to Run

> Ensure `settings.toml` is properly configured **before** running.

There are three ways to run the bot, and you may choose whichever best suits your needs.

### 1) Release

Download the latest release and run the executable.

### 2) Docker

```bash
# Build the image
docker build -t rembot .

# Run (Linux/macOS)
docker run --rm \
  -v "$(pwd)/src:/app/src" \
  rembot

# Run (Windows CMD)
docker run --rm \
  -v "%cd%\src:/app/src"
  rembot
```

> The volumes mount your local `src/` for output log files.

### 3) Python (virtualenv)

```bash
# Create a virtual environment
python -m venv .venv

# Activate
# Linux/macOS
source ./.venv/bin/activate
# Windows CMD
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python src/main.py   # direct module/script
```

---

## ⚠️ Warnings

> **Disclaimer:** Trading cryptocurrencies — especially with **leverage** — involves **significant risk**. This bot is **not financial advice** and is provided for educational/experimental purposes only. Review the code and the strategy thoroughly, start small, and only trade with funds you can afford to lose. **All P\&L is your responsibility.**
>
> Protect your API keys, never commit secrets, and be aware of operational risks such as rate limits, network issues, exchange maintenance, and **slippage**, all of which can materially affect performance.
