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
        self.rvgi_value = None
        self.is_ready = False
        
        self.swma_co = SWMA(algorithm)
        self.swma_hl = SWMA(algorithm)
        self.swma_rvgi = SWMA(algorithm)
        self.sig_value = None
        
        self.Bullish = False
        self.Bearish = False
        

    def Update_Value(self, bar):
        
        swma_co_value = self.swma_co.get_value(bar.Close - bar.Open)
        swma_hl_value = self.swma_hl.get_value(bar.High - bar.Low)
        if swma_co_value and swma_hl_value:
            self.rvgi_q.append(swma_co_value)
            self.rvgi_n.append(swma_hl_value)
        
        if len(self.rvgi_n) == self.Length:
            self.rvgi_value = sum(self.rvgi_q) / sum(self.rvgi_n)
            self.sig_value = self.swma_rvgi.get_value(self.rvgi_value)
            if self.sig_value:
                self.is_ready = True
        
    def Bull_Or_Bear(self, bar):
        if self.is_ready:
            if self.rvgi_value > self.sig_value:
                self.Bullish = True
                self.Bearish = False
            elif self.rvgi_value < self.sig_value:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False
        
                
