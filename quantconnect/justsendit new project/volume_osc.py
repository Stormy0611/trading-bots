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

        self.volume_osc = deque(maxlen=2)
        self.is_ready = False
        # self.short = deque(maxlen=self.Length_short)
        # self.short = deque(maxlen=self.Length_short)
        self.ema_short = ExponentialMovingAverage(self.Length_short)
        self.ema_long = ExponentialMovingAverage(self.Length_long)
        self.volume_osc_value = None

      

        self.Bullish = False
        self.Bearish = False


        

    def Bull_Or_Bear(self, volume, color, bar):
        self.ema_short.Update(IndicatorDataPoint(bar.EndTime, volume))
        self.ema_long.Update(IndicatorDataPoint(bar.EndTime, volume))
        if self.ema_long.IsReady:
            self.volume_osc.append(100 * (self.ema_short.Current.Value - self.ema_long.Current.Value) / self.ema_long.Current.Value)
        if len(self.volume_osc) == 2:
            self.is_ready = True
            self.volume_osc_value = self.volume_osc[-1]
        
        # self.volume_ma.appendleft(volume)

        # if len(self.volume_ma) == self.Length:
        #     self.volume_ma_value = sum(self.volume_ma) / len(self.volume_ma)

            if volume > self.volume_osc_value and color > 0:
                self.Bearish = False
                self.Bullish = True
            elif volume > self.volume_osc_value and color < 0:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
