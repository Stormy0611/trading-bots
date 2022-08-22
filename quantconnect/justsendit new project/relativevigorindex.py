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
        
        self.swma_co = SWMA()
        self.swma_hl = SWMA()
        self.swma_rvgi = SWMA()
        self.sig_value = None
        
        self.Bullish = False
        self.Bearish = False
        

    def Bull_Or_Bear(self, color, bar):
        
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
        
        
        
        if len(self.volume_osc) == 2:
            self.is_ready = True
        
            if self.volume_osc_value > 0:
                self.Bearish = False
                self.Bullish = True
            elif self.volume_osc_value < 0:
                self.Bullish = False
                self.Bearish = True
            else:
                self.Bullish = False
                self.Bearish = False

                
