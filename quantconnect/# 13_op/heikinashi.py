from AlgorithmImports import *
from collections import deque
import config
import Optimization_Model as om

class Heikin_Ashi():


    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.TEMA_Period = om.tema_period
        self.EMA_Period = om.ema_period
        self.Candle_Size_Factor = om.candle_size_factor
        self.ema_close = ExponentialMovingAverage(self.EMA_Period) # SRC =
      
        self.EMA_Dictionary = {}
        self.Ha_Open = None
        self.Ha_Close = None
        self.Tha_Close = None
        self.THL_2 = None
        self.Ha_Close_Smooth = None
        self.HL2_Smooth = None
        self.Short_Candle= False
        self.Keep_n1 = False
        self.Keep_all_1 = False
        self.Keep_13 = False
        self.Utr = False
        self.Keep_n2 = False
        self.Keep_23 = False
        self.Keep_all_2 = False
        self.Dtr = False
        self.Upw = False
        self.Dnw = False
        self.Up_With_Offset = False
        self.Buy_Signal = False
        self.Sell_Signal = False
        self.Neutral_Signal = False
        self.Ha_Colt = None
        self.Color = ""
        self.Count = 0
        self.Ha_Close_Queue = deque(maxlen=2)
        self.Ha_Open_Queue = deque(maxlen=2)
        self.Low_Queue = deque(maxlen=2)
        self.High_Queue = deque(maxlen=2)
        self.Close_Queue = deque(maxlen=2)
        self.Keep_n1_Queue = deque(maxlen=2)
        self.Keep_all_1_Queue = deque(maxlen=2)
        self.Keep_n2_Queue = deque(maxlen=2)
        self.Keep_all_2_Queue = deque(maxlen=2)
        self.Utr_Queue = deque(maxlen=2)
        self.Dtr_Queue = deque(maxlen=2)
        
        self.EMA_Dictionary["Tha_Close"] = Calc_Tema(algorithm)
        self.EMA_Dictionary["THL_2"] = Calc_Tema(algorithm)
        self.EMA_Dictionary["THC_EMA"] = Calc_Tema(algorithm)
        self.EMA_Dictionary["THL_2_EMA"] = Calc_Tema(algorithm)

        self.Tha_Close = self.EMA_Dictionary["Tha_Close"]
        self.THL_2 = self.EMA_Dictionary["THL_2"]
        self.THC_EMA = self.EMA_Dictionary["THC_EMA"]
        self.THL_2_EMA = self.EMA_Dictionary["THL_2_EMA"]

    def Bull_Or_Bear(self, bartime, baropen, barhigh, barlow, barclose):
        self.ema_close.Update(IndicatorDataPoint(bartime, barclose))
        ohlc4 = (baropen + barhigh +barlow + barclose) /4
        hl2 = (barhigh + barlow) / 2
        if abs(barclose - baropen) < ((barhigh - barlow) * self.Candle_Size_Factor):
            self.Short_Candle = True
        else:
            self.Short_Candle = False
        if self.Ha_Open is None:
            self.Ha_Open = ohlc4
        self.Ha_Open = (self.Ha_Open + ohlc4) / 2

        self.Ha_Close = (self.Ha_Open + max(barhigh, self.Ha_Open) + min(barlow, self.Ha_Open) + ohlc4) / 4

        if barlow is not None:
            self.Low_Queue.appendleft(barlow)
        if barhigh is not None:
            self.High_Queue.appendleft(barhigh)
        if barclose is not None:
            self.Close_Queue.appendleft(barclose)

        if self.Ha_Close is not None:
            self.Ha_Close_Queue.appendleft(self.Ha_Close)
        if self.Ha_Open is not None:
            self.Ha_Open_Queue.appendleft(self.Ha_Open)

        self.Tha_Close.EMA_Update(self.Ha_Close, bartime)
        self.THL_2.EMA_Update(hl2, bartime)

        if self.THL_2.IsRdy:
            self.THL_2_EMA.EMA_Update(self.THL_2.Return_Value, bartime)
        
        self.Count = self.Count + 1
        # self.algorithm.Debug(self.Count)
        if self.Tha_Close.IsRdy:
            self.THC_EMA.EMA_Update(self.Tha_Close.Return_Value, bartime)


            if self.THC_EMA.IsRdy:
                self.Ha_Close_Smooth = 2 * self.Tha_Close.Return_Value - self.THC_EMA.Return_Value
            

        if self.THL_2_EMA.IsRdy:
            self.HL2_Smooth = 2 * self.THL_2.Return_Value - self.THL_2_EMA.Return_Value


        if self.HL2_Smooth is not None:
            if ((self.Ha_Close >= self.Ha_Open) and (self.Ha_Close_Queue[1] >= self.Ha_Open_Queue[1])) or (barclose >= self.Ha_Close) or (barhigh > self.High_Queue[1]) or (barlow > self.Low_Queue[1]) or (self.HL2_Smooth >= self.Ha_Close_Smooth):
                self.Keep_n1 = True
            else:
                self.Keep_n1 = False
        self.Keep_n1_Queue.appendleft(self.Keep_n1)

        if len(self.Keep_n1_Queue) == 2:
            # self.algorithm.Debug(f" {self.algorithm.Time} {self.Keep_n1} {self.Keep_n1_Queue[1]}")
            if self.Keep_n1 or (self.Keep_n1_Queue[1] and (barclose >= baropen) or (barclose >= self.Close_Queue[1])):
                self.Keep_all_1 = True
            else:
                self.Keep_all_1 = False
        
        self.Keep_all_1_Queue.appendleft(self.Keep_all_1)

        if self.Short_Candle is not None:
            if len(self.High_Queue) == 2 and len(self.Low_Queue) == 2:
                if self.Short_Candle and (barhigh >= self.Low_Queue[1]):
                    self.Keep_13 = True

        
        if len(self.Keep_all_1_Queue) == 2:
            # self.algorithm.Debug(f" {self.algorithm.Time} {self.Keep_all_1} {self.Keep_all_1_Queue[1]} {self.Keep_13}")
            if self.Keep_all_1 or (self.Keep_all_1_Queue[1] and self.Keep_13):
                self.Utr = True
            else:
                self.Utr = False
        
        self.Utr_Queue.appendleft(self.Utr)

        if self.HL2_Smooth is not None:
            if (self.Ha_Close < self.Ha_Open) and (self.Ha_Close_Queue[1] < self.Ha_Open_Queue[1]) or (self.HL2_Smooth < self.Ha_Close_Smooth):
                self.Keep_n2 = True
            else:
                self.Keep_n2 = False
        self.Keep_n2_Queue.appendleft(self.Keep_n2)

        if self.Short_Candle is not None:
            if len(self.High_Queue) == 2 and len(self.Low_Queue) == 2:
                if self.Short_Candle and (barlow <= self.High_Queue[1]):
                    self.Keep_23 = True
                else:
                    self.Keep_23 = False
            
       

        if len(self.Keep_n2_Queue) == 2:
            if self.Keep_n2 or (self.Keep_n2_Queue[1] and (barclose < baropen) or (barclose < self.Close_Queue[1])):
                self.Keep_all_2 = True
            else:
                self.Keep_all_2 = False
        
        self.Keep_all_2_Queue.appendleft(self.Keep_all_2)

        if len(self.Keep_all_2_Queue) == 2:
            if self.Keep_all_2 or (self.Keep_all_2_Queue[1] and self.Keep_23):
                self.Dtr = True
            else:
                self.Dtr = False

        self.Dtr_Queue.appendleft(self.Dtr)    
    

        if len(self.Dtr_Queue) == 2 and len(self.Utr_Queue) == 2:
            # self.algorithm.Debug(f" {self.Dtr} {self.Dtr_Queue[1]} {self.Utr}")
            if not self.Dtr and self.Dtr_Queue[1] == True and self.Utr == True:
                self.Upw = True
            else:
                self.Upw = False
            
            if not self.Utr and self.Utr_Queue[1] == True and self.Dtr == True:
                self.Dnw = True
            else:
                self.Dnw = False

        
        if self.Upw != self.Dnw:
            # self.algorithm.Debug(f" {self.Upw} {self.Dnw}")
            self.Up_With_Offset = self.Upw
        
        else:
            self.Up_With_Offset = self.Up_With_Offset
        
        # self.algorithm.Debug(str(self.Upw))
        if self.Upw:
            self.Buy_Signal = True
     
        elif self.Dnw == False and self.Up_With_Offset == True:
            self.Buy_Signal = True
        else:
            self.Buy_Signal = self.Up_With_Offset
        
        if self.ema_close.IsReady:
            if barclose < self.ema_close.Current.Value:
                self.Sell_Signal = True
            else:
                self.Sell_Signal = False

        
        if self.Buy_Signal or (self.Sell_Signal):
            self.Neutral_Signal = False
        
        else:
            self.Neutral_Signal = True
        
        if self.Buy_Signal:
            self.Ha_Colt = 1
        elif self.Neutral_Signal:
            self.Ha_Colt = 0
        else:
            self.Ha_Colt = -1

        if self.Ha_Colt is not None:
            if self.Ha_Colt > 0:
                self.Color = "GREEN"
            elif self.Ha_Colt < 0:
                self.Color = "RED"
            else:
                self.Color = "BLUE"


        # self.algorithm.Debug(f" {self.algorithm.Time} {self.ema}")
        # self.ema.Update(IndicatorDataPoint(bartime, barclose))




class Calc_Tema():


    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.TEMA_Period = config.TEMA_PERIOD
        self.EMA_Period = config.EMA_PERIOD
        self.Candle_Size_Factor = config.CANDLE_SIZE_FACTOR
        self.ema_1 = ExponentialMovingAverage(self.TEMA_Period) # SRC =
        self.ema_2 = ExponentialMovingAverage(self.TEMA_Period) # SRC = EMA1
        self.ema_3 = ExponentialMovingAverage(self.TEMA_Period) # SRC = EMA2
        self.Test_Queue = deque(maxlen=10)
        self.IsRdy = False
        self.Return_Value = None

    def EMA_Update(self, src, bartime):
        self.ema_1.Update(IndicatorDataPoint(bartime, src))

        self.Test_Queue.appendleft(src)

       

        if self.ema_1.IsReady:
            self.ema_2.Update(IndicatorDataPoint(bartime, self.ema_1.Current.Value))
          
        if self.ema_2.IsReady:
            # self.algorithm.Debug(self.algorithm.Time)
            self.ema_3.Update(IndicatorDataPoint(bartime, self.ema_2.Current.Value))
            
        if self.ema_3.IsReady:
            self.Return_Value = 3 * (self.ema_1.Current.Value - self.ema_2.Current.Value) + self.ema_3.Current.Value
            self.IsRdy = True
        else:
            self.IsRdy = False
            # self.IsRdy()

    # def IsRdy(self):
    #     self.algorithm.Debug("HERE")
    #     if not self.ema_3.IsReady or self.Return_Value is None:
    #         return False
    #     else:
    #         return True   

    
            
