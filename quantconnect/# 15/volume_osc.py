#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class VOL_OSC():
    
    def __init__(self, algorithm, short, long):

        self.Length_short = short
        self.Length_long = long
        self.algorithm = algorithm
        
        # self.volume_osc = deque(maxlen=2)
        self.is_ready = False
        # self.short = deque(maxlen=self.Length_short)
        # self.short = deque(maxlen=self.Length_short)
        self.ema_short = ExponentialMovingAverage(self.Length_short)
        self.ema_long = ExponentialMovingAverage(self.Length_long)
        self.value = None

      

        self.Bullish = False
        self.Bearish = False

    def Update_Value(self, bartime, volume):
        self.ema_short.Update(IndicatorDataPoint(bartime, volume))
        self.ema_long.Update(IndicatorDataPoint(bartime, volume))
        if self.ema_long.IsReady:
            self.value = 100 * (self.ema_short.Current.Value - self.ema_long.Current.Value) / self.ema_long.Current.Value
            self.is_ready = True
            # self.volume_osc.append(self.value)
        # if len(self.volume_osc) == 2:
        #     self.is_ready = True
        

    def Bull_Or_Bear(self, bar):
        # self.volume_ma.appendleft(bar.Volume)

        # if len(self.volume_ma) == self.Length:
        #     self.is_ready = True
        #     self.volume_ma_value = sum(self.volume_ma) / len(self.volume_ma)

        if self.is_ready:    
            if bar.Close - bar.Open >= 0:
                barcolor = "GREEN"
            else:
                barcolor = "RED"

            if barcolor == "GREEN" and bar.Volume > self.volume_ma_value:
                self.Bullish = True
                self.Bearish = False
            elif barcolor == "RED" and bar.Volume < self.volume_ma_value:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
