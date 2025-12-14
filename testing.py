import requests
from datetime import datetime
import pandas as pd
import mplfinance as mpf
from typing import List

class Candle:
    def __init__(self, k=None):
        if k:
            self.open_time = k["t"]
            self.open = float(k["o"])
            self.high = float(k["h"])
            self.low = float(k["l"])
            self.close = float(k["c"])
            self.volume = float(k["v"])
            self.close_time = k["T"]
            self.is_closed = k["x"]
        else:
            self.open_time = None
            self.open = None
            self.high = None
            self.low = None
            self.close = None
            self.volume = None
            self.close_time = None
            self.is_closed = None

        # Swing and BOS markers
        self.is_swing_high = False
        self.is_swing_low = False
        self.is_closed_high = False
        self.is_closed_low = False
        self.is_bullish_bos = False
        self.is_bearish_bos = False

def date_to_milliseconds(date_str, date_format="%Y-%m-%d %H:%M:%S"):
    dt = datetime.strptime(date_str, date_format)
    return int(dt.timestamp() * 1000)

def scrape_historical_candles(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    limit = 1000
    candles = []

    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit,
        "startTime": start_time,
        "endTime": end_time
    }

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            break

        for k in data:
            k_dict = {
                "t": k[0],
                "o": k[1],
                "h": k[2],
                "l": k[3],
                "c": k[4],
                "v": k[5],
                "T": k[6],
                "x": True
            }
            candles.append(Candle(k_dict))

        if len(data) < limit:
            break

        params["startTime"] = data[-1][0] + 1

    return candles

def detect_zigzag_swings(candles: List[Candle], window=3):
    n = len(candles)
    for i in range(window, n - window):
        current_high = candles[i].high
        current_low = candles[i].low
        current_close = candles[i].close

        is_swing_high = True
        is_swing_low = True
        is_closed_high = True
        is_closed_low = True

        for j in range(i - window, i + window + 1):
            if j == i:
                continue
            if candles[j].high >= current_high:
                is_swing_high = False
            if candles[j].low <= current_low:
                is_swing_low = False
            if candles[j].close >= current_close:
                is_closed_high = False
            if candles[j].close <= current_close:
                is_closed_low = False

        candles[i].is_swing_high = is_swing_high
        candles[i].is_swing_low = is_swing_low
        candles[i].is_closed_high = is_closed_high
        candles[i].is_closed_low = is_closed_low

def bos(candles: List[Candle], threshold=0.001, volume_threshold=1000):
    last_swing_high = -1
    last_swing_low = -1
    bos_events = []

    for j in range(len(candles)):
        if candles[j].is_swing_high:
            last_swing_high = j
        if candles[j].is_swing_low:
            last_swing_low = j

        # Bullish BOS
        if last_swing_high >= 0 and candles[j].close > candles[last_swing_high].high * (1 + threshold):
            is_strong = candles[j].volume > volume_threshold
            candles[j].is_bullish_bos = True
            bos_event = {
                'type': 'bullish',
                'pivot_index': last_swing_high,
                'break_index': j,
                'break_price': candles[j].close,
                'pivot_price': candles[last_swing_high].high,
                'volume': candles[j].volume,
                'is_strong_bos': is_strong
            }
            bos_events.append(bos_event)
            last_swing_high = j

        # Bearish BOS
        if last_swing_low >= 0 and candles[j].close < candles[last_swing_low].low * (1 - threshold):
            is_strong = candles[j].volume > volume_threshold
            candles[j].is_bearish_bos = True
            bos_event = {
                'type': 'bearish',
                'pivot_index': last_swing_low,
                'break_index': j,
                'break_price': candles[j].close,
                'pivot_price': candles[last_swing_low].low,
                'volume': candles[j].volume,
                'is_strong_bos': is_strong
            }
            bos_events.append(bos_event)
            last_swing_low = j

    return bos_events

def candles_to_dataframe(candles: List[Candle]):
    data = {
        "Open": [c.open for c in candles],
        "High": [c.high for c in candles],
        "Low": [c.low for c in candles],
        "Close": [c.close for c in candles],
        "Volume": [c.volume for c in candles],
    }
    dates = [datetime.fromtimestamp(c.open_time / 1000) for c in candles]
    df = pd.DataFrame(data, index=pd.DatetimeIndex(dates))
    return df

def plot_candles_with_indicators(candles: List[Candle]):
    df = candles_to_dataframe(candles)

    swing_high_series = pd.Series(index=df.index, dtype='float64')
    swing_low_series = pd.Series(index=df.index, dtype='float64')
    closed_high_series = pd.Series(index=df.index, dtype='float64')
    closed_low_series = pd.Series(index=df.index, dtype='float64')
    bullish_bos_series = pd.Series(index=df.index, dtype='float64')
    bearish_bos_series = pd.Series(index=df.index, dtype='float64')

    for c in candles:
        dt = datetime.fromtimestamp(c.open_time / 1000)
        if c.is_swing_high and dt in swing_high_series.index:
            swing_high_series.at[dt] = c.high
        if c.is_swing_low and dt in swing_low_series.index:
            swing_low_series.at[dt] = c.low
        if c.is_closed_high and dt in closed_high_series.index:
            closed_high_series.at[dt] = c.close
        if c.is_closed_low and dt in closed_low_series.index:
            closed_low_series.at[dt] = c.close
        if c.is_bullish_bos and dt in bullish_bos_series.index:
            bullish_bos_series.at[dt] = c.close
        if c.is_bearish_bos and dt in bearish_bos_series.index:
            bearish_bos_series.at[dt] = c.close

    addplots = []
    if swing_high_series.dropna().any():
        addplots.append(mpf.make_addplot(swing_high_series, type='scatter', markersize=80, marker='^', color='red'))
    if swing_low_series.dropna().any():
        addplots.append(mpf.make_addplot(swing_low_series, type='scatter', markersize=80, marker='v', color='green'))
    if closed_high_series.dropna().any():
        addplots.append(mpf.make_addplot(closed_high_series, type='scatter', markersize=50, marker='o', color='orange'))
    if closed_low_series.dropna().any():
        addplots.append(mpf.make_addplot(closed_low_series, type='scatter', markersize=50, marker='o', color='blue'))
    if bullish_bos_series.dropna().any():
        addplots.append(mpf.make_addplot(bullish_bos_series, type='scatter', markersize=120, marker='X', color='purple'))
    if bearish_bos_series.dropna().any():
        addplots.append(mpf.make_addplot(bearish_bos_series, type='scatter', markersize=120, marker='X', color='brown'))

    mpf.plot(df, type='candle', style='charles', addplot=addplots, volume=True,
             title="BTCUSDT 4h with Swings and BOS", figsize=(12,8))

if __name__ == "__main__":
    start_str = "2023-06-01 00:00:00"
    end_str = "2023-06-30 23:59:59"

    start_ms = date_to_milliseconds(start_str)
    end_ms = date_to_milliseconds(end_str)

    candles = scrape_historical_candles("BTCUSDT", "4h", start_ms, end_ms)
    print(f"Fetched {len(candles)} candles.")

    detect_zigzag_swings(candles, window=3)

    bos_events = bos(candles, threshold=0.001, volume_threshold=1000)
    print(f"Detected {len(bos_events)} BOS events.")

    plot_candles_with_indicators(candles)
