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

        self.type = self.get_type()

        # Marking attributes for structure analysis
        self.bullish= False
        self.bearish = False
        self.is_high = False             # Local high (optional if needed)
        self.is_low = False              # Local low (optional if needed)
        self.is_swing_high = False       # Zigzag swing high
        self.is_swing_low = False        # Zigzag swing low
        self.is_closed_high = False      # Highest close in a local window
        self.is_closed_low = False       # Lowest close in a local window
        self.is_bullish_bos = False
        self.is_bearish_bos = False
        self.is_Bullish_FVG = False
        self.is_Bearish_FVG = False
        self.is_strong_bullish_bos = False
        self.is_strong_bearish_bos = False
        self.break_point = 0
        self.marked = False
        self.BOS_info = {}
        self.is_bullish_ob= False
        self.is_bullish_sweep = False
        self.is_bearish_ob= False

    def isbullish(self):
        return self.open < self.close if self.open is not None and self.close is not None else False

    def isbearish(self):
        return self.open > self.close if self.open is not None and self.close is not None else False

    def get_type(self):
        if self.open is None or self.close is None:
            return None
        if self.open < self.close:
            return "bullish"
        elif self.open > self.close:
            return "bearish"
        else:
            return "neutral"

        

    


    

    
