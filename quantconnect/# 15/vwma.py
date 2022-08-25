#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class VWMA():
    
    def __init__(self, algorithm, length):

        self.Length = length

        self.vwma = deque(maxlen=self.Length)
        self.value = None
        self.is_ready = False

        self.sma_v = SimpleMovingAverage(self.Length)
        self.sma_cv = SimpleMovingAverage(self.Length)

        self.Bullish = False
        self.Bearish = False

    def Update_Value(self, bartime, volume, value):
        self.sma_v.Update(IndicatorDataPoint(bartime, volume))
        self.sma_cv.Update(IndicatorDataPoint(bartime, volume * value))
        
        if self.sma_cv.IsReady:
            self.value = self.sma_cv.Current.Value / self.sma_v.Current.Value
            self.vwma.append(self.sma_cv.Current.Value / self.sma_v.Current.Value)
        
        if len(self.vwma) == self.Length:
            self.is_ready = True
            

    def Bull_Or_Bear(self, bar, color):
        pass
        # self.sma_v.Update(IndicatorDataPoint(bar.EndTime, bar.Volume))
        # self.sma_cv.Update(IndicatorDataPoint(bar.EndTime, bar.Volume * bar.Close))
        
        # if self.sma_cv.IsReady:
        #     self.value = self.sma_cv.Current.Value / self.sma_v.Current.Value
        #     self.vwma.append(self.sma_cv.Current.Value / self.sma_v.Current.Value)
        
        # if len(self.vwma) == self.Length:
        #     self.is_ready = True

            # if volume > self.volume_ma_value and color > 0:
            #     self.Bearish = False
            #     self.Bullish = True
            # elif volume > self.volume_ma_value and color < 0:
            #     self.Bullish = False
            #     self.Bearish = True
            # else:
            #     self.Bullish = False
            #     self.Bearish = False

                
