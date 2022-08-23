#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class STC():
    
    def __init__(self, algorithm, length, fast, slow, AAA):

        self.Length = length
        self.Length_fast = fast
        self.Length_slow = slow

        self.AAA = AAA

        self.stc = deque(maxlen=2)
        self.stc_value = None
        self.is_ready = False

        self.fastMA = ExponentialMovingAverage(self.Length_fast)
        self.slowMA = ExponentialMovingAverage(self.Length_slow)
        
        self.d_fs = deque(maxlen=self.Length)
        self.d_fs_value = None
        
        self.CCCCC = deque(maxlen=2)
        self.CCCCC.append(0.0)
        self.CCCCC.append(0.0)
        self.DDD = deque(maxlen=self.Length)
        self.DDD.append(None)
        self.DDD.append(None)
        self.DDDDDD = deque(maxlen=2)
        self.DDDDDD.append(0.0)
        self.DDDDDD.append(0.0)
        self.EEEEE = deque(maxlen=2)
        self.EEEEE.append(None)
        self.EEEEE.append(None)
        self.color = None

        self.Bullish = False
        self.Bearish = False


        

    def Update(self, bartime, value):
        
        self.fastMA.Update(IndicatorDataPoint(bartime, value))
        self.slowMA.Update(IndicatorDataPoint(bartime, value))
        if self.slowMA.IsReady:
            self.d_fs_value = self.fastMA.Current.Value - self.slowMA.Current.Value
            self.d_fs.append(self.d_fs_value)
            if len(self.d_fs) == self.Length:
                CCC = min(self.d_fs)
                CCCC = max(self.d_fs)
                if CCCC > 0:
                    self.CCCCC.append((self.d_fs_value - CCC) / CCCC * 100)
                else:
                    self.CCCCC.append(self.CCCCC[-1])
                if self.DDD[-1] == None:
                    self.DDD.append(self.CCCCC[0])
                else:
                    self.DDD.append(self.DDD[-1] + self.AAA * (self.CCCCC[-1] - self.DDD[-1]))
                if len(self.DDD) == self.Length:
                    DDDD = min(self.DDD[-1])
                    DDDDD = max(self.DDD[-1]) - DDDD
                    if DDDDD > 0:
                        self.DDDDDD.append(self.DDD - DDDD) / DDDDD * 100
                    else:
                        self.DDDDDD.append(self.DDDDDD[-1])
                    if self.EEEEE[-1] == None:
                        self.EEEEE.append(self.DDDDDD[-1])
                    else:
                        self.EEEEE.append(self.DDDDDD[-1] + self.AAA * (self.DDDDDD[-1] - self.EEEEE[-1]))
                    self.stc_value = self.EEEEE[-1]
                    self.stc.append(self.stc_value)
                    if len(self.stc) == 2:
                        self.is_ready = True
        
        if self.is_ready == True:
            if self.stc[1] >= self.stc[0]:
                self.color = "GREEN"
            else:
                self.color = "RED"    

               
