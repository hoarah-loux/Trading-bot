import asyncio
import websockets
import json
import requests
from datetime import datetime
from candle import Candle

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


async def scrape_live_candles(symbol, interval, candles):
    url = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"

    async with websockets.connect(url) as ws:
        print(f"Connected to Binance WebSocket for {symbol} @ {interval}")
        try:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                k = data['k']
                if k['x']:  # only closed candles
                    candle = Candle(k)
                    candles.append(candle)
                    print(f"Live candle closed @ {candle.close_time} close: {candle.close}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed.")


if __name__ == "__main__":
    # Setup your historic date range:
    start_str = "2023-06-01 00:00:00"
    end_str = "2023-06-30 23:59:59"

    start_ms = date_to_milliseconds(start_str)
    end_ms = date_to_milliseconds(end_str)

    interval_ms = 4 * 60 * 60 * 1000  # 4 hours
    adjusted_end_ms = end_ms - interval_ms

    # Pass all required parameters explicitly:
    candles = scrape_historical_candles("BTCUSDT", "4h", start_ms, adjusted_end_ms)
    print(f"Fetched {len(candles)} historical candles.")

    asyncio.run(scrape_live_candles("btcusdt", "4h", candles))
