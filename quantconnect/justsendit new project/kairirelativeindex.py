#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class KRI():
    
    def __init__(self, algorithm, length):

        self.Length = length

        # self.kri = deque(maxlen=self.Length)
        self.kri_value = None
        self.is_ready = False

        self.sma = SimpleMovingAverage(self.Length)

        self.Bullish = False
        self.Bearish = False


    def Update(self, bartime, value): # value = close
    
        self.sma.Update(IndicatorDataPoint(bartime, value))
        if self.sma.IsReady:
            self.kri_value = 100 * (value - self.sma.Current.Value) / self.sma.Current.Value
            self.is_ready = True
        

    def Bull_Or_Bear(self, bar):
        # self.kri.appendleft(bar.Volume)

        # if len(self.kri) == self.Length:
        #     self.is_ready = True
        #     self.kri_value = sum(self.kri) / len(self.kri)
        if self.is_ready:
            if self.kri_value >= 0:
                self.Bullish = True
                self.Bearish = False
            elif self.kri_value < 0:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False
