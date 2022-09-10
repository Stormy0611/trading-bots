#region imports
from AlgorithmImports import *
#endregion
# import config
import statistics as stats
from collections import deque
import json
import setting


class VOL_MA():
    
    def __init__(self, algorithm):
        # file = open("setting.py", "r")
        # lines = file.readlines()
        # config = {}
        # for line in lines:
        #     list = line.split("=")
        #     try:
        #         config[list[0]] = int(list[1])
        #     except:
        #         config[list[0]] = float(list[1])
        # file.close()
        self.Length = setting.VOLUME_MA_LENGTH

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

                
