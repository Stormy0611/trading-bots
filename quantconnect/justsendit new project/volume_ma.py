#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class VOL_MA():
    
    def __init__(self, algorithm, length):

        self.Length = length

        self.volume_ma = deque(maxlen=self.Length)
        self.volume_ma_value = None
        self.is_ready = False

      

        self.Bullish = False
        self.Bearish = False


    def Update(self, value):
        self.volume_ma.appendleft(value)

        if len(self.volume_ma) == self.Length:
            self.volume_ma_value = sum(self.volume_ma) / len(self.volume_ma)
            self.is_ready = True

        

    def Bull_Or_Bear(self, bar, color):
        # self.volume_ma.appendleft(bar.Volume)

        # if len(self.volume_ma) == self.Length:
        #     self.is_ready = True
        #     self.volume_ma_value = sum(self.volume_ma) / len(self.volume_ma)

            if bar.Volume > self.volume_ma_value:
                self.Bearish = False
                self.Bullish = True
            elif bar.Volume < self.volume_ma_value:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
