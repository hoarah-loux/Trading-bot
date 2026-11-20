# Trading Bot

A work-in-progress Python project for exploring cryptocurrency candle data and market-structure signals. The current scripts use Binance market data and focus on analysis; they do not place trades.

## What it does

- Represents OHLCV data as candle objects.
- Fetches historical candles from Binance and can listen for completed live candles over a WebSocket.
- Experiments with swing highs and lows, breaks of structure (BOS), volume-based BOS strength, order blocks, fair value gaps (FVG), and liquidity sweeps.
- Plots BTCUSDT candles with swing and BOS markers.

## Project files

- `candle.py` - candle data model and basic bullish/bearish classification.
- `scrape.py` - historical candle retrieval and a live Binance candle stream.
- `structures.py` - experimental market-structure detection functions.
- `strategy_priority.py` - fetches historical BTCUSDT candles, analyzes them, and plots a chart.
- `main.py` - placeholder for future application logic.

## Getting started

You need Python and an internet connection to retrieve market data. Install the packages used by the scripts:

```bash
python3 -m pip install requests websockets pandas mplfinance
```

Run the charting example:

```bash
python3 strategy_priority.py
```

It currently uses a hard-coded BTCUSDT date range and 4-hour interval. The data is fetched from Binance before the chart is displayed.

To try the scraper:

```bash
python3 scrape.py
```

This fetches a hard-coded historical range, then listens for completed 4-hour BTCUSDT candles. Stop it with `Ctrl+C`.

## Work in progress

This is an experimental project, not a finished or production-ready trading bot. Some analysis functions are incomplete, settings and date ranges are hard-coded, and there is no order execution or risk-management system. Treat the results as exploratory, not financial advice.
