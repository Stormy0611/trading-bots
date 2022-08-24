#region imports
from gc import is_tracked
from AlgorithmImports import *
#endregion
import config
import statistics as stats
from collections import deque



class TSI():
    
    def __init__(self, algorithm, short, long, signal):

        self.Length_short = short
        self.Length_long = long
        self.Length_signal = signal

        self.tsi = deque(maxlen=2)
        self.tsi_ema = ExponentialMovingAverage(self.Length_signal)
        self.tsi_value = None
        self.tsi_ema_value = None
        self.is_ready = False

        self.fist_smooth_ema = ExponentialMovingAverage(self.Length_long)
        self.double_fist_smooth_ema = ExponentialMovingAverage(self.Length_short)
        self.close = deque(maxlen=2)
      

        self.Bullish = False
        self.Bearish = False


    def Double_Smooth(self, src, bartime):
        self.fist_smooth_ema.Update(IndicatorDataPoint(bartime, src))
        if self.fist_smooth_ema.IsReady:
            self.double_fist_smooth_ema.Update(IndicatorDataPoint(bartime, self.fist_smooth_ema.Current.Value))
        if self.double_fist_smooth_ema.IsReady:
            return self.double_fist_smooth_ema.Current.values
        else:
            return 0
        

    def Update(self, bartime, value):
        
        self.close.append(value)
        if len(self.close) == 2:
            pc = self.close[1] - self.close[0]
            double_smoothed_pc = self.Double_Smooth(pc, bartime)
            double_smoothed_abs_pc = self.Double_Smooth(abs(pc), bartime)
            if double_smoothed_abs_pc * double_smoothed_pc:
                self.tsi_value = 100 * (double_smoothed_pc / double_smoothed_abs_pc)
                self.tsi.append(self.tsi_value)
                self.tsi_ema.Update(IndicatorDataPoint(bartime, self.tsi_value))
                if self.tsi_ema.IsReady:
                    self.tsi_ema_value = self.tsi_ema.Current.Value
                    self.is_ready = True
        
    def Bull_Or_Bear(self, bar):
        if self.is_ready:
            if self.tsi_value > self.tsi_ema_value:
                self.Bullish = True
                self.Bearish = False
            elif self.tsi_value < self.tsi_ema_value:
                self.Bearish = True
                self.Bullish = False
            else:
                self.Bullish = False
                self.Bearish = False
        

                
