#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque
import Optimization_Model as om

class TDI():
    
    def __init__(self, algorithm):

       

        self.Band_Length = om.band_length
        self.Fast_MA_On_RSI = om.fast_ma_on_rsi
        self.Slow_MA_On_RSI = om.slow_ma_on_rsi
        self.algorithm = algorithm
        self.ma = deque(maxlen=self.Band_Length)
        self.ma_value = None
        self.Offs = None
        self.Up = None
        self.Dn = None
        self.Mid = None
        self.Fast_MA = deque(maxlen=self.Fast_MA_On_RSI)
        self.Slow_MA = deque(maxlen=self.Slow_MA_On_RSI)
        self.Fast_Value = None
        self.Slow_Value = None

        self.HLine_Low = 30
        self.HLine_Mid = 50
        self.HLine_High = 70

        self.Bullish = False
        self.Bearish = False


        

    def Bull_Or_Bear(self, rsi):
        
        self.ma.appendleft(rsi)
     
        if len(self.ma) == self.Band_Length:
            self.ma_value = sum(self.ma) / len(self.ma)
            self.Offs = stats.stdev(self.ma) * 1.6185

            
            self.Up = self.ma_value + self.Offs
            self.Dn = self.ma_value - self.Offs
            self.Mid = (self.Up + self.Dn) / 2

            self.Fast_MA.appendleft(rsi)
            self.Slow_MA.appendleft(rsi)                                                                                 

            if len(self.Fast_MA) == self.Fast_MA_On_RSI and len(self.Slow_MA) == self.Slow_MA_On_RSI:
                self.Fast_Value = sum(self.Fast_MA) / len(self.Fast_MA)
                self.Slow_Value = sum(self.Slow_MA) / len(self.Slow_MA)

                if self.Fast_Value > self.Slow_Value and self.Fast_Value > self.Mid:
                    self.Bullish = True
                    self.Bearish = False
                elif self.Slow_Value > self.Fast_Value and self.Slow_Value < self.Mid:
                    self.Bullish = False
                    self.Bearish = True
                else:
                    self.Bearish = False
                    self.Bullish = False



