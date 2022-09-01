#region imports
from AlgorithmImports import *
#endregion
from collections import deque
import config
import Optimization_Model as om

class Donchian_Ribbon():
    
    def __init__(self, algorithm):

        self.Donchian_Channel_Period = om.donchain_period
        self.HH_LL_Period = 2
        self.Highest_High = deque(maxlen=self.HH_LL_Period)
        self.Lowest_Low = deque(maxlen=self.HH_LL_Period)
        self.List_Of_Highs = deque(maxlen=self.Donchian_Channel_Period)
        self.List_Of_Lows = deque(maxlen=self.Donchian_Channel_Period)
        self.Trend = 0

        self.algorithm = algorithm
        self.HH_LL_Period_Alt = 2
        self.Highest_High_Alt = deque(maxlen=self.HH_LL_Period_Alt)
        self.Lowest_Low_Alt = deque(maxlen=self.HH_LL_Period_Alt)
        self.List_Of_Highs_Alt = deque(maxlen=self.Donchian_Channel_Period)
        self.List_Of_Lows_Alt = deque(maxlen=self.Donchian_Channel_Period)
        self.Trend_Alt = 0
        self.Color = None
        self.Donchian_Channel_Ready = False
 

    def Donchian_Channel(self, high, low, close):

        self.List_Of_Highs.appendleft(high)
        self.List_Of_Lows.appendleft(low)
        
        if len(self.List_Of_Highs) == self.Donchian_Channel_Period and len(self.List_Of_Lows) == self.Donchian_Channel_Period:
            self.Highest_High.appendleft(max(self.List_Of_Highs))
            self.Lowest_Low.appendleft(min(self.List_Of_Lows))

            if len(self.Highest_High) == self.HH_LL_Period and len(self.Lowest_Low) == self.HH_LL_Period:
                self.Donchian_Channel_Ready = True
                if close > self.Highest_High[1]:
                    self.Trend = 1
                elif close < self.Lowest_Low[1]:
                    self.Trend = -1
                else:
                    self.Trend = self.Trend

                


    def Donchian_Alt(self, high, low, close):
      
        if self.Donchian_Channel_Ready:
            self.List_Of_Highs_Alt.appendleft(high)
            self.List_Of_Lows_Alt.appendleft(low)
          

            if len(self.List_Of_Highs_Alt) == self.Donchian_Channel_Period and len(self.List_Of_Lows_Alt) == self.Donchian_Channel_Period:
                self.Highest_High_Alt.appendleft(max(self.List_Of_Highs_Alt))
                self.Lowest_Low_Alt.appendleft(min(self.List_Of_Lows_Alt))

                

                if len(self.Highest_High_Alt) == self.HH_LL_Period_Alt and len(self.Lowest_Low_Alt) == self.HH_LL_Period_Alt:
                
                    if close > self.Highest_High_Alt[1]:
                        self.Trend_Alt = 1
                    elif close < self.Lowest_Low_Alt[1]:
                        self.Trend_Alt = -1
                    else:
                        self.Trend_Alt = self.Trend_Alt


                    if self.Trend == 1 and self.Trend_Alt == 1:
                        self.Color = "GREEN"
                    if self.Trend == -1 and self.Trend_Alt == -1:
                        self.Color = "RED"



