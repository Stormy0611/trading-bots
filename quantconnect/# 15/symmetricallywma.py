#region imports
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class SWMA():
    
    def __init__(self, algorithm):

        self.swma = deque(maxlen=4)
        self.swma_value = None

      

        self.Bullish = False
        self.Bearish = False

    def get_value(self, src):
        self.swma.append(src)
        if len(self.swma) == 4:
            self.swma_value = (self.swma[0] + self.swma[3] + 2 * (self.swma[2] + self.swma[1])) / 6
            return self.swma_value
        else:
            return None
        
