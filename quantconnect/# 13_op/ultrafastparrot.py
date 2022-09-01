from AlgorithmImports import *
from collections import deque
import config
import statistics as stats
import Optimization_Model as om
class UltraFastParrot():


    def __init__(self, algorithm):
        self.MA_0 = ArnaudLegouxMovingAverage(period=3, sigma=om.signal_sigma, offset=om.signal_offset)
        self.MA_1 = ArnaudLegouxMovingAverage(period=5, sigma=om.signal_sigma , offset=om.signal_offset)
        self.MA_2 = ArnaudLegouxMovingAverage(period=8, sigma=om.signal_sigma , offset=om.signal_offset)
        self.MA_3 = ArnaudLegouxMovingAverage(period=13, sigma=om.signal_sigma , offset=om.signal_offset)
        self.MA_4 = ArnaudLegouxMovingAverage(period=21, sigma=om.signal_sigma , offset=om.signal_offset)
        self.MA_5 = ArnaudLegouxMovingAverage(period=34, sigma=om.signal_sigma , offset=om.signal_offset)
        self.MA_6 = ArnaudLegouxMovingAverage(period=55, sigma=om.signal_sigma , offset=om.signal_offset)

        self.Previous_Close = deque(maxlen=2)
        self.PC = None

        self.Indicators = {}

        self.Double_Smoothed_PC = None
        self.Double_Smoothed_ABS_PC = None

        self.TSI_Line =  None
        self.TSI_Signal = None
        self.TSI_Hist = None
        self.Below_Signal = False
        self.Crossing_Over = False
        self.Crossing_Under = False
        self.Crossing_Over_0 = False
        self.Crossing_Under_0 = False

        self.TSI_Color = ""
        self.TSI_Hist_Color = ""

        self.TSI_Line_Queue = deque(maxlen=2)
        self.TSI_Signal_Queue = deque(maxlen=2)
        self.TSI_Hist_Queue = deque(maxlen=2)


        self.Indicators["DOUBLE PC"] = Double_Smooth(algorithm)
        self.Indicators["DOUBLE PC ABS"] = Double_Smooth(algorithm)

        self.Double_Smoothed_PC = self.Indicators["DOUBLE PC"]
        self.Double_Smoothed_ABS_PC = self.Indicators["DOUBLE PC ABS"]

    def Calculate_Parrot(self, close, bartime):
        self.Previous_Close.appendleft(close)

        if len(self.Previous_Close) == 2:
            self.PC = close - self.Previous_Close[1]

        
        if self.PC is not None:
            self.Double_Smoothed_PC.Double_Smooth_Update(self.PC, bartime)
            self.Double_Smoothed_ABS_PC.Double_Smooth_Update(abs(self.PC), bartime)


        if self.Double_Smoothed_PC.IsRdy and self.Double_Smoothed_ABS_PC.IsRdy:
            if self.Double_Smoothed_ABS_PC.Return_Value != 0:
                self.TSI_Line = 100 * (self.Double_Smoothed_PC.Return_Value / self.Double_Smoothed_ABS_PC.Return_Value)
        
        if self.TSI_Line is not None:
            self.MA_0.Update(IndicatorDataPoint(bartime, self.TSI_Line))
            self.MA_1.Update(IndicatorDataPoint(bartime, self.TSI_Line))
            self.MA_2.Update(IndicatorDataPoint(bartime, self.TSI_Line))
            self.MA_3.Update(IndicatorDataPoint(bartime, self.TSI_Line))
            self.MA_4.Update(IndicatorDataPoint(bartime, self.TSI_Line))
            self.MA_5.Update(IndicatorDataPoint(bartime, self.TSI_Line))
            self.MA_6.Update(IndicatorDataPoint(bartime, self.TSI_Line))

        if self.MA_6.IsReady:
            self.TSI_Signal = (self.MA_0.Current.Value + self.MA_1.Current.Value + self.MA_2.Current.Value + self.MA_3.Current.Value + self.MA_4.Current.Value + self.MA_5.Current.Value + self.MA_6.Current.Value) / 7


        
        if self.TSI_Signal is not None:
            self.TSI_Hist = self.TSI_Line - self.TSI_Signal

            self.TSI_Hist_Queue.appendleft(self.TSI_Hist)

            

        if self.TSI_Hist is not None:
            if self.TSI_Line <= self.TSI_Signal:
                self.Below_Signal = True
            else:
                self.Below_Signal = False
        
        if self.TSI_Line is not None and self.TSI_Signal is not None:
            self.TSI_Line_Queue.appendleft(self.TSI_Line)
            self.TSI_Signal_Queue.appendleft(self.TSI_Signal)
            if len(self.TSI_Line_Queue) == 2 and len(self.TSI_Signal_Queue) == 2:
                if self.TSI_Line > self.TSI_Signal and self.TSI_Line_Queue[1] < self.TSI_Signal_Queue[1]:
                    self.Crossing_Over = True
                else:
                    self.Crossing_Over = False
                
                if self.TSI_Line < self.TSI_Signal and self.TSI_Line_Queue[1] > self.TSI_Signal_Queue[1]:
                    self.Crossing_Under = True
                else:
                    self.Crossing_Under = False

                
                if self.TSI_Line > 0 and self.TSI_Line_Queue[1] < 0:
                    self.Crossing_Over_0 = True
                else:
                    self.Crossing_Over_0 = False

                if self.TSI_Line < 0 and self.TSI_Line_Queue[1] > 0:
                    self.Crossing_Under_0 = True
                else:
                    self.Crossing_Under_0 = False


                if self.Below_Signal:
                    self.TSI_Color = "RED"
                else:
                    self.TSI_Color = "GREEN"

                if self.Below_Signal and self.TSI_Hist >= self.TSI_Hist_Queue[1]:
                    self.TSI_Hist_Color = "MAROON"
                elif self.Below_Signal and self.TSI_Hist < self.TSI_Hist_Queue[1]:
                    self.TSI_Hist_Color = "RED"
                elif self.TSI_Hist < self.TSI_Hist_Queue[1]:
                    self.TSI_Hist_Color = "GREEN"
                else:
                    self.TSI_Hist_Color = "LIME"

        

class Double_Smooth():


    def __init__(self, algorithm):
        self.algorithm = algorithm
        
        self.Short = config.SHORT_ALMA_LENGTH
        self.Long = config.LONG_ALMA_LENGTH
        self.Offset = config.FAST_OFFSET
        self.OffsetT = config.TREND_OFFSET
        self.Sigma = config.FAST_SIGMA
        self.SigmaT = config.TREND_SIGMA
        self.First_Smooth = ArnaudLegouxMovingAverage(period=self.Long, sigma=self.SigmaT , offset=self.OffsetT)
        self.Last_Smooth = ArnaudLegouxMovingAverage(period=self.Short, sigma=self.Sigma , offset=self.Offset)
        self.Test_Queue = deque(maxlen=10)
        self.IsRdy = False
        self.Return_Value = None

    def Double_Smooth_Update(self, src, bartime):
        
        self.First_Smooth.Update(IndicatorDataPoint(bartime, src))


        if self.First_Smooth.IsReady:
            self.Last_Smooth.Update(IndicatorDataPoint(bartime, self.First_Smooth.Current.Value))
        

        if self.Last_Smooth.IsReady:
            self.Return_Value = self.Last_Smooth.Current.Value
            self.IsRdy = True
        else:
            self.IsRdy = False
