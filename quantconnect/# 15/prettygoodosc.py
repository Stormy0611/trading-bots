#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class PGO_LB():
    
    def __init__(self, algorithm, length):

        self.Length = length
        self.algorithm = algorithm

        # self.pgo_osc = deque(maxlen=self.Length)
        self.is_ready = False
        # self.short = deque(maxlen=self.Length_short)
        # self.short = deque(maxlen=self.Length_short)
        self.sma = SimpleMovingAverage(self.Length)
        self.ema = ExponentialMovingAverage(self.Length)
        # self.Crypto = algorithm.AddCrypto("BTCUSD", Resolution.Hour, Market.GDAX).Symbol
        self.tr = TrueRange()
        self.value = None

      

        self.Bullish = False
        self.Bearish = False

    def Update_Value(self, bartime, value):     # value = close
        self.tr.Update(IndicatorDataPoint(bartime, value))
        if self.tr.IsReady:
            self.sma.Update(IndicatorDataPoint(bartime, value))
            self.ema.Update(IndicatorDataPoint(bartime, self.tr.Current.Value))
        if self.ema.IsReady:
            self.value = (value - self.sma.Current.Value) / self.ema.Current.Value
            self.is_ready = True
        

    def Bull_Or_Bear(self, bar = None):
        # self.tr.Update(IndicatorDataPoint(bar.EndTime))
        # if self.tr.IsReady:
        #     self.sma.Update(IndicatorDataPoint(bar.EndTime, bar.Close))
        #     self.ema.Update(IndicatorDataPoint(bar.EndTime, self.tr.Current.Value))
        # if self.ema.IsReady:
        #     self.value = (bar.Close - self.sma.Current.Value) / self.ema.Current.Value
        #     self.is_ready = True
        
        if self.is_ready:
            if self.value > 3:
                self.Bearish = False
                self.Bullish = True
            elif self.value < -3:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
