#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class SWMA():
    
    def __init__(self, algorithm):

        self.swma = deque(maxlen=4)
        self.value = None
        self.is_ready = False

        self.Bullish = False
        self.Bearish = False

    def Update_Value(self, src):
        self.swma.append(src)
        if len(self.swma) == 4:
            self.value = (self.swma[0] + self.swma[3] + 2 * (self.swma[2] + self.swma[1])) / 6
            self.is_ready = True
        
