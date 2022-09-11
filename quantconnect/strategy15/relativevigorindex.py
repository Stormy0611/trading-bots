#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque
from symmetricallywma import SWMA


class RVGI():
    
    def __init__(self, algorithm, length):

        self.Length = length

        self.rvgi_n = deque(maxlen=self.Length)
        self.rvgi_q = deque(maxlen=self.Length)
        self.value = None
        self.is_ready = False
        
        self.swma_co = SWMA(algorithm)
        self.swma_hl = SWMA(algorithm)
        self.swma_rvgi = SWMA(algorithm)
        self.sig_value = None
        
        self.Bullish = False
        self.Bearish = False
        

    def Update_Value(self, bar):
        
        self.swma_co.Update_Value(bar.Close - bar.Open)
        self.swma_hl.Update_Value(bar.High - bar.Low)
        if self.swma_co.is_ready and self.swma_hl.is_ready:
            self.rvgi_q.appendleft(self.swma_co.value)
            self.rvgi_n.appendleft(self.swma_hl.value)
        
        if len(self.rvgi_n) == self.Length:
            self.value = sum(self.rvgi_q) / sum(self.rvgi_n)
            self.swma_rvgi.Update_Value(self.value)
            if self.swma_rvgi.is_ready:
                self.sig_value = self.swma_rvgi.value
                self.is_ready = True
        
    def Bull_Or_Bear(self, bar = None):
        if self.is_ready:
            if self.value > self.sig_value:
                self.Bullish = True
                self.Bearish = False
            elif self.value < self.sig_value:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False
        
                
