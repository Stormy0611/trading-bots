#region imports
from AlgorithmImports import *
#endregion
from collections import deque
# import config
import statistics as stats
import json

class Volatility_Oscillator():
    
    def __init__(self, algorithm):
        file = open("setting.py", "r")
        lines = file.readlines()
        config = {}
        for line in lines:
            list = line.split("=")
            try:
                config[list[0]] = int(list[1])
            except:
                config[list[0]] = float(list[1])
        file.close()
        self.Length = config['VOLATILITY_PERIOD']
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
                self.Y = self.X * -1
        
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
