from candle import Candle

def detect_zigzag_swings(candles: list[Candle], window=3):
    n = len(candles)
    for i in range(window, n - window):
        current_high = candles[i].high
        current_low = candles[i].low
        current_close = candles[i].close

        is_swing_high = True
        is_swing_low = True
        is_closed_high = True
        is_closed_low = True

        # Check neighbors before and after i
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


## this is mostly the final bos def, but we need to add a bool is_strong_bos to check for volume//
# if its already added we just need to find and appropriate threshold, maybe the mean of volume of candles across a given interval.
# add closed highs and lows
def bos(candles: list[Candle], threshold=0.001, volume_threshold=1000):
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
            candles[j].BOS_info = bos_event
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
            candles[j].BOS_info = bos_event
            bos_events.append(bos_event)
            last_swing_low = j

    return bos_events


def Order_block(candles: list[Candle]):
    for i in range(len(candles)):

        # Bullish Order Block
        if candles[i].is_bullish_bos:
            j = i
            while j >= 0 and not candles[j].is_swing_low:
                j -= 1
            if j >= 0:
                candles[j].is_bullish_ob = True

        # Bearish Order Block
        if candles[i].is_bearish_bos:
            j = i
            while j >= 0 and not candles[j].is_swing_high:
                j -= 1
            if j >= 0:
                candles[j].is_bearish_ob = True



## if candle at i-1 high is less than i +1 low with a threshold
def fvg(candles: list[Candle], threshold=12):
    for i in range(1, len(candles) - 1):
        prev = candles[i - 1]
        curr = candles[i]
        next = candles[i + 1]

        # Bullish FVG
        if prev.high < curr.low and curr.high < next.low:
            gap_size = min(curr.low - prev.high, next.low - curr.high)
            if gap_size >= threshold:
                candles[i].is_Bullish_FVG = True

        # Bearish FVG
        if prev.low > curr.high and curr.low > next.high:
            gap_size = min(prev.low - curr.high, curr.low - next.high)
            if gap_size >= threshold:
                candles[i].is_Bearish_FVG = True

    return False


def fakeouts(candles: list[Candle], threshold: int):

    for i in range(len(candles)):
        if candles[i].is_bullish_bos:
            pass        


def liquidity_sweep(candles: list, threshold: float):
    for i in range(len(candles)):
        # bull
        j = i - 1
        while j >= 0:
            
            if candles[j].is_bullish_ob and candles[i].low < candles[j].low - threshold:
                candles[i].is_bullish_sweep = True
                break
            j -= 1

        # bear
        j = i - 1
        while j >= 0:
            
            if candles[j].is_bearish_ob and candles[i].high > candles[j].high + threshold:
                candles[i].is_bearish_sweep = True
                break
            j -= 1


def trend(candles: list[Candle], threshold: int):
    return None



def zones(candles: list[Candle], len: int):
    pass






    


    





























def Order_block1(candles: list[Candle]):
    for i in range(len(candles)):
        if candles[i].is_bullish_bos:
            j = i
            while not candles[j].is_swing_low:
                # your code here
                j -= 1
            candles[j].is_bullish_ob = True



































##these are just two overloaded functions

def bos(candles: list[Candle], threshold=0.1, volume_threshold=1000, int=1):
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
            candles[j].is_bullish_bos = True
            candles[j].is_strong_bullish_bos = candles[j].volume > volume_threshold
            bos_event = {
                'type': 'bullish',
                'pivot_index': last_swing_high,
                'break_index': j,
                'break_price': candles[j].close,
                'pivot_price': candles[last_swing_high].high,
                'volume': candles[j].volume,
                'is_strong_bos': candles[j].is_strong_bullish_bos
            }
            bos_events.append(bos_event)
            last_swing_high = j

        # Bearish BOS
        if last_swing_low >= 0 and candles[j].close < candles[last_swing_low].low * (1 - threshold):
            candles[j].is_bearish_bos = True
            candles[j].is_strong_bearish_bos = candles[j].volume > volume_threshold
            bos_event = {
                'type': 'bearish',
                'pivot_index': last_swing_low,
                'break_index': j,
                'break_price': candles[j].close,
                'pivot_price': candles[last_swing_low].low,
                'volume': candles[j].volume,
                'is_strong_bos': candles[j].is_strong_bearish_bos
            }
            bos_events.append(bos_event)
            last_swing_low = j

    return bos_events


def bos(candles: list[Candle], threshold=0.1):
    i = -1
    for j in range(len(candles)):
        if candles[j].is_swing_high:
            i = j
            continue
        if i >= 0 and candles[j].close > candles[i].high * (1 + threshold):
            i = j
            candles[j].is_breaking_structure = True
