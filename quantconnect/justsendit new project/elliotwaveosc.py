#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class EWO_LB():
    
    def __init__(self, algorithm):

        # self.volume_osc = deque(maxlen=2)
        self.ewo_value = None
        self.is_ready = False
        # self.short = deque(maxlen=self.Length_short)
        # self.short = deque(maxlen=self.Length_short)
        self.ema_short = ExponentialMovingAverage(5)
        self.ema_long = ExponentialMovingAverage(35)

      

        self.Bullish = False
        self.Bearish = False

    def Update(self, bartime, value):   # value = close
        self.ema_short.Update(IndicatorDataPoint(bartime, value))
        self.ema_long.Update(IndicatorDataPoint(bartime, value))
        if self.ema_long.IsReady:
            self.ewo_value = self.ema_short.Current.Value - self.ema_long.Current.Value
            self.is_ready = True
            # self.volume_osc.append(self.volume_osc_value)
        # if len(self.volume_osc) == 2:
        #     self.is_ready = True
        

    def Bull_Or_Bear(self, bar):

        if self.is_ready:
            if self.ewo_value > 0:
                self.Bullish = True
                self.Bearish = False
            elif self.ewo_value <= 0:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
