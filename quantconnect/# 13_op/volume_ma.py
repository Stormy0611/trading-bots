#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque
import Optimization_Model as om


class VOL_MA():
    
    def __init__(self, algorithm):

        self.Length = om.volume_ma_length

        self.volume_ma = deque(maxlen=self.Length)
        self.volume_ma_value = None

      

        self.Bullish = False
        self.Bearish = False


        

    def Bull_Or_Bear(self, volume, color):
        self.volume_ma.appendleft(volume)

        if len(self.volume_ma) == self.Length:
            self.volume_ma_value = sum(self.volume_ma) / len(self.volume_ma)

            if volume > self.volume_ma_value and color > 0:
                self.Bearish = False
                self.Bullish = True
            elif volume > self.volume_ma_value and color < 0:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
