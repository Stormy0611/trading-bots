#region imports
from AlgorithmImports import *
#endregion
from collections import deque
import config
import statistics as stats
import Optimization_Model as om
class Volatility_Oscillator():
    
    def __init__(self, algorithm):

        self.Length = om.volatility_period
        self.Spike = None
        self.Spike_Queue = deque(maxlen=self.Length)
        self.X = None
        self.Y =  None
        self.LBR = 5
        self.LBL = 5
        self.Range_Upper = 60
        self.Range_Lower = 55
        self.Bullish = False
        self.Bearish = False
        
        

    def Bull_Or_Bear(self, close, open):
        self.Spike = close - open

        if self.Spike is not None:
            self.Spike_Queue.appendleft(self.Spike)
            if len(self.Spike_Queue) == self.Length:
                self.X = stats.stdev(self.Spike_Queue)
                self.Y = self.X * - 1
        
        if self.X is not None and self.Y is not None:
            if self.Spike > self.X:
                self.Bullish  = True
                self.Bearish = False
            elif self.Spike < self.Y:
                self.Bearish = True
                self.Bullish = False
            else:
                self.Bullish = False
                self.Bearish = False
