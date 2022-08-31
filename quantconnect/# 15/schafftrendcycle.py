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
        self.value = None
        self.is_ready = False

        self.fastMA = ExponentialMovingAverage(self.Length_fast)
        self.slowMA = ExponentialMovingAverage(self.Length_slow)
        
        self.d_fs = deque(maxlen=self.Length)
        self.d_fs_value = None
        
        self.CCCCC = deque(maxlen=2)
        self.CCCCC.appendleft(0.0)
        self.CCCCC.appendleft(0.0)
        self.DDD = deque(maxlen=self.Length)
        self.DDD.appendleft(None)
        self.DDD.appendleft(None)
        self.DDDDDD = deque(maxlen=2)
        self.DDDDDD.appendleft(0.0)
        self.DDDDDD.appendleft(0.0)
        self.EEEEE = deque(maxlen=2)
        self.EEEEE.appendleft(None)
        self.EEEEE.appendleft(None)
        self.color = None

        self.Bullish = False
        self.Bearish = False


        

    def Update_Value(self, bartime, value):     # value = close
        
        self.fastMA.Update(IndicatorDataPoint(bartime, value))
        self.slowMA.Update(IndicatorDataPoint(bartime, value))
        if self.slowMA.IsReady:
            self.d_fs_value = self.fastMA.Current.Value - self.slowMA.Current.Value
            self.d_fs.appendleft(self.d_fs_value)
            if len(self.d_fs) == self.Length:
                CCC = min(self.d_fs)
                CCCC = max(self.d_fs)
                if CCCC > 0:
                    self.CCCCC.appendleft((self.d_fs_value - CCC) / CCCC * 100)
                else:
                    self.CCCCC.appendleft(self.CCCCC[0])
                if self.DDD[0] == None:
                    self.DDD.appendleft(self.CCCCC[1])
                else:
                    self.DDD.appendleft(self.DDD[0] + self.AAA * (self.CCCCC[0] - self.DDD[0]))
                if len(self.DDD) == self.Length:
                    DDDD = min(self.DDD)
                    DDDDD = max(self.DDD) - DDDD
                    if DDDDD > 0:
                        self.DDDDDD.appendleft(self.DDD[0] - DDDD) / DDDDD * 100
                    else:
                        self.DDDDDD.appendleft(self.DDDDDD[0])
                    if self.EEEEE[0] == None:
                        self.EEEEE.appendleft(self.DDDDDD[0])
                    else:
                        self.EEEEE.appendleft(self.DDDDDD[0] + self.AAA * (self.DDDDDD[0] - self.EEEEE[0]))
                    self.value = self.EEEEE[0]
                    self.stc.appendleft(self.value)
                    if len(self.stc) == 2:
                        self.is_ready = True
        
        if self.is_ready:
            if self.stc[0] >= self.stc[1]:
                self.color = "GREEN"
            else:
                self.color = "RED"    

    def Bull_Or_Bear(self, bar = None):
        if self.is_ready:
            if self.color == "GREEN":
                self.Bullish = True
                self.Bearish = False
            elif self.color == "RED":
                self.Bullish = False
                self.Bearish = False
            else:
                self.Bullish = False
                self.Bearish = False
