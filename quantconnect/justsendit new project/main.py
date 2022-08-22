from AlgorithmImports import *
from collections import deque
import config
from datetime import *
import statistics as stats 
import time


from prettygoodosc import PGO_LB
from relativevigorindex import RVGI
from schafftrendcycle import STC
from truestrenthindex import TSI
from volume_ma import VOL_MA
from volume_osc import VOL_OSC
from volumeweightmovingaverage import VWMA


class LogicalSkyBlueDog(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 29)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.Crypto = self.AddCrypto("ADAUSD", Resolution.Hour, Market.GDAX).Symbol
        
        self.VOL_MA_LENGTH = config.VOL_MA
        self.VWMA1_LENGTH = config.VWMA_FASTEST
        self.VWMA2_LENGTH = config.VWMA_FAST
        self.VWMA3_LENGTH = config.VWMA_SLOW
        self.VWMA4_LENGTH = config.VWMA_SLOWEST
        self.VOL_OSC_SHORT_LENGTH = config.VOL_OSC_SHORT
        self.VOL_OSC_LONG_LENGTH = config.VOL_OSC_LONG
        self.PGO_LB_LENGTH = config.PGO_LB_LENGTH
        self.TSI_SHORT_LENGTH = config.TSI_SHORT
        self.TSI_LONG_LENGTH = config.TSI_LONG
        self.TSI_SIGNAL_LENGTH = config.TSI_SIGNAL
        self.RVGI_LENGTH = config.RVGI_LENGTH
        self.STC_LENGTH = config.STC_LENGTH
        self.STC_FAST_LENGTH = config.STC_FAST
        self.STC_SLOW_LENGTH = config.STC_SLOW
        self.STC_AAA = config.STC_AAA
        
        self.Indicators = {}
        self.Indicators['VOL_MA'] = VOL_MA(length=self.VOL_MA_LENGTH)
        self.Indicators['VWMA1'] = VWMA(length=self.VWMA1_LENGTH)
        self.Indicators['VWMA2'] = VWMA(length=self.VWMA2_LENGTH)
        self.Indicators['VWMA3'] = VWMA(length=self.VWMA3_LENGTH)
        self.Indicators['VWMA4'] = VWMA(length=self.VWMA4_LENGTH)
        self.Indicators['VOL_OSC'] = VOL_OSC(short=self.VOL_OSC_SHORT_LENGTH, 
                                             long=self.VOL_OSC_LONG_LENGTH)
        self.Indicators['PGO_LB'] = PGO_LB(length=self.PGO_LB_LENGTH)
        self.Indicators['TSI'] = TSI(short=self.TSI_SHORT_LENGTH,
                                     long=self.TSI_LONG_LENGTH,
                                     signal=self.TSI_SIGNAL_LENGTH)
        self.Indicators['RVGI'] = RVGI(length=self.RVGI_LENGTH)
        self.Indicators['STC'] = STC(length=self.STC_LENGTH,
                                     fast=self.STC_FAST_LENGTH,
                                     slow=self.STC_SLOW_LENGTH,
                                     AAA=self.STC_AAA)
        
        
        
        # self.lambda_func = lambda x: (x.High + x.Low) / 2.0

        # self.Daily_Consolidator = self.Consolidate(self.Crypto, timedelta(hours=1), self.IndicatorUpdate)

        
        # self.Warm_Up_Consolidator = TradeBarConsolidator(timedelta(hours=1))
        # self.SubscriptionManager.AddConsolidator(self.Crypto, self.Warm_Up_Consolidator)
        # self.Warm_Up_Consolidator.DataConsolidated += self.MA_ATR_RSI_WARMUP

     

        # history = map(lambda x: x[self.Crypto],self.History(1100 , Resolution.Hour))
        # for row in history:
        #     self.Warm_Up_Consolidator.Update(row)


        # # if not self.ma_atr_rsi.IsReady:
        # #     self.MA_ATR_RSI_WARMUP()
        
        # Set TrainingMethod to be executed immediately
        self.Train(self.TrainingMethod)

        # Set TrainingMethod to be executed at 8:00 am every Sunday
        self.Train(self.DateRules.Every(DayOfWeek.Sunday), self.TimeRules.At(8 , 0), self.TrainingMethod)



    # def MA_ATR_RSI_WARMUP(self, sender, bar):
        
      
          
    #     TDI_Indie = self.Indicators["TDI"]
    #     if self.rsi_tdi.IsReady:
    #         TDI_Indie.Bull_Or_Bear(self.rsi_tdi.Current.Value)
    

        
    #     donchian_indie = self.Indicators["DONCHIAN"]
    #     donchian_indie.Donchian_Channel(bar.High, bar.Low, bar.Close)
    #     donchian_indie.Donchian_Alt(bar.High, bar.Low, bar.Close)


        
    #     volatility_osc = self.Indicators["VOLATILITY"]
    #     volatility_osc.Bull_Or_Bear(bar.Close, bar.Open)
    #     # donchian.Donchian_Ribbon.__init__(self)
        

        
    #     VOLUME_Indie = self.Indicators["VOLUME"]
    #     color = bar.Close - bar.Open
    #     VOLUME_Indie.Bull_Or_Bear(bar.Volume, color)


        
    #     heikin_ashi = self.Indicators["HEIKINASHI"]
    #     heikin_ashi.Bull_Or_Bear(bar.EndTime, bar.Open, bar.High, bar.Low, bar.Close)
        
    #     ultra_fast_parrot = self.Indicators["ULTRAPARROT"]
    #     ultra_fast_parrot.Calculate_Parrot(bar.Close, bar.EndTime)

    #     if self.rsi_tdi.IsReady:
    #         TDI_Indie.Bull_Or_Bear(self.rsi_tdi.Current.Value)
    #     # self.Debug(donchian_indie.Color)
    #     # self.Debug(str(volatility_osc.Bullish))    

    #     self.rsi_2.Update(IndicatorDataPoint(bar.EndTime , bar.Close))
    #     self.rsi_warm.Update(IndicatorDataPoint(bar.EndTime, bar.Close))
        
    #     if self.rsi_sma_warm.IsReady:
    #         self.rsi_sma_queue.appendleft(self.rsi_sma_warm.Current.Value)
        
    #     ####### 2

        
        
    #     if self.rsi_ema.IsReady:
    #         self.rsi_2_queue.appendleft(self.rsi_ema.Current.Value)

    #     if len(self.rsi_2_queue) == 3:
    #         self.Atr_Rsi_2 = abs(self.rsi_2_queue[1] - self.rsi_ema.Current.Value)
        
    #     if self.Atr_Rsi_2 is not None:
    #         self.Ema_Atr_Rsi_2.Update(IndicatorDataPoint(bar.EndTime, self.Atr_Rsi_2))
        
    #     if self.Ema_Atr_Rsi_2.IsReady:
    #         self.Dar_2_Ema.Update(IndicatorDataPoint(bar.EndTime, self.Ema_Atr_Rsi_2.Current.Value))

    #     if self.Dar_2_Ema.IsReady:
    #         self.Dar_2 = self.Dar_2_Ema.Current.Value * self.QQE2
        
    #     if self.rsi_ema.IsReady and self.Dar_2 is not None:
    #         self.New_Long_Band_2 = self.rsi_ema.Current.Value + self.Dar_2
    #         self.New_Short_Band_2 = self.rsi_ema.Current.Value - self.Dar_2
        
    #     if len(self.rsi_2_queue) == 3 and len(self.Long_Band_Queue_2) == 3 and self.New_Long_Band_2 is not None:
    #         if self.rsi_2_queue[1] > self.Long_Band_Queue_2[1] and self.rsi_ema.Current.Value > self.Long_Band_Queue_2[1]:
    #             self.Long_Band_2 = max(self.Long_Band_Queue_2[1], self.New_Long_Band_2)
    #         else:
    #             self.Long_Band_2 = self.New_Long_Band_2
        
    #     self.Long_Band_Queue_2.appendleft(self.Long_Band_2)
        
    #     if len(self.rsi_2_queue) == 3 and len(self.Short_Band_Queue_2) == 3 and self.New_Short_Band_2 is not None:
    #         if self.rsi_2_queue[1] < self.Short_Band_Queue_2[1] and self.rsi_ema.Current.Value < self.Short_Band_Queue_2[1]:
    #             self.Short_Band_2 = min(self.Short_Band_Queue_2[1], self.New_Short_Band_2)
    #         else:
    #             self.Short_Band_2 = self.New_Short_Band_2
        
    #     self.Short_Band_Queue_2.appendleft(self.Short_Band_2)

        



    #     if len(self.Long_Band_Queue_2) == 3 and len(self.rsi_2_queue) == 2:
    #         if self.Long_Band_Queue_2[1] > self.rsi_ema.Current.Value and self.Long_Band_Queue_2[2] < self.rsi_2_queue[1]:
    #             self.cross_2 = True
    #         elif self.Long_Band_Queue_2[1] < self.rsi_ema.Current.Value  and self.Long_Band_Queue_2[2] > self.rsi_2_queue[1]:
    #             self.cross_2 = True
    #         else:
    #             self.cross_2 = False
        
    #     check_2 = False
    #     if len(self.Short_Band_Queue_2) == 3 and len(self.rsi_2_queue) == 2:
    #         if self.Short_Band_Queue_2[1] > self.rsi_ema.Current.Value  and self.Short_Band_Queue_2[2] < self.rsi_2_queue[1]:
    #             check_2 = True
    #         elif self.Short_Band_Queue_2[1] < self.rsi_ema.Current.Value  and self.Short_Band_Queue_2[2] > self.rsi_2_queue[1]:
    #             check_2 = True
    #         else:
    #             check_2 = False
            
    #         if check_2:
    #             self.Trend_2 = 1
    #         if not check_2:
    #             if self.cross_2:
    #                 self.Trend_2 = -1
    #             else:
    #                 if len(self.Trend_Queue_2) >= 1:
    #                     self.Trend_2 = self.Trend_Queue_2[1]
    #                 else:
    #                     self.Trend_2 = 1
        
    #     self.Trend_Queue_2.appendleft(self.Trend_2)


    #     if self.Trend_2 == 1:
    #         self.Fast_Atr_Rsi_Tl_2 = self.Long_Band_2
    #     else:
    #         self.Fast_Atr_Rsi_Tl_2 = self.Short_Band_2

    #     if self.Fast_Atr_Rsi_Tl_2 is not None:
    #         self.Basis_Queue.appendleft(self.Fast_Atr_Rsi_Tl_2-50)

    #     if self.rsi_ema.IsReady:
    #         if self.rsi_ema.Current.Value >= 50:
    #             self.QQE_z_Long_2 = self.QQE_z_Long_2 + 1
    #             self.QQE_z_Short_2 = 0
    #         else:
    #             self.QQE_z_Short_2 = self.QQE_z_Short_2 +1
    #             self.QQE_z_Long_2 = 0

    #     #### 2

    #     if len(self.rsi_sma_queue) == 3:
    #         self.atr_rsi = abs(self.rsi_sma_queue[1] - self.rsi_sma.Current.Value)

    #     if self.rsi_ema.IsReady and len(self.rsi_2_queue) == 3:
    #         self.Atr_Rsi_2 = abs(self.rsi_2_queue[1] - self.rsi_ema.Current.Value)

    #     if self.atr_rsi is not None:
    #         self.ma_atr_rsi.Update(IndicatorDataPoint(bar.EndTime, self.atr_rsi))
        
    #     if self.ma_atr_rsi.IsReady:
    #         self.dar_ema.Update(IndicatorDataPoint(bar.EndTime, self.ma_atr_rsi.Current.Value))
        
    #     if self.dar_ema.IsReady:
    #         self.dar = self.dar_ema.Current.Value * self.QQE
        
    #     if self.dar is not None and self.rsi_sma_warm.IsReady:
    #         self.New_Long_Band = self.rsi_sma_warm.Current.Value - self.dar
    #         self.New_Short_Band = self.rsi_sma_warm.Current.Value + self.dar
        
    #     if len(self.rsi_sma_queue) == 3 and len(self.Long_Band_Queue) == 3 and self.New_Long_Band is not None:

    #         if self.rsi_sma_queue[1] > self.Long_Band_Queue[1] and self.rsi_sma_queue[0] > self.Long_Band_Queue[1]:
    #             self.Long_Band = max(self.Long_Band_Queue[1], self.New_Long_Band)
    #         else:
    #             self.Long_Band = self.New_Long_Band
        
    #     self.Long_Band_Queue.appendleft(self.Long_Band)


    #     if len(self.rsi_sma_queue) == 3 and len(self.Short_Band_Queue) == 23 and self.New_Short_Band is not None:

    #         if self.rsi_sma_queue[1] < self.Short_Band_Queue[1] and self.rsi_sma_queue[0] < self.Short_Band_Queue[1]:
    #             self.Short_Band = min(self.Short_Band_Queue[1, self.New_Short_Band])
    #         else:
    #             self.Short_Band = self.New_Short_Band
        
    #     self.Short_Band_Queue.appendleft(self.Short_Band)
        
    #     if len(self.Long_Band_Queue) == 3 and len(self.rsi_sma_queue) == 2:
    #         if self.Long_Band_Queue[1] > self.rsi_sma.Current.Value and self.Long_Band_Queue[2] < self.rsi_sma_queue[1]:
    #             self.cross_1 = True
    #         elif self.Long_Band_Queue[1] < self.rsi_sma.Current.Value  and self.Long_Band_Queue[2] > self.rsi_sma_queue[1]:
    #             self.cross_1 = True
    #         else:
    #             self.cross_1 = False
        
    #     check = False
    #     if len(self.Short_Band_Queue) == 3 and len(self.rsi_sma_queue) == 2:
    #         if self.Short_Band_Queue[1] > self.rsi_sma.Current.Value  and self.Short_Band_Queue[2] < self.rsi_sma_queue[1]:
    #             check = True
    #         elif self.Short_Band_Queue[1] < self.rsi_sma.Current.Value  and self.Short_Band_Queue[2] > self.rsi_sma_queue[1]:
    #             check = True
    #         else:
    #             check = False
            
    #         if check:
    #             self.Trend = 1
    #         if not check:
    #             if self.cross_1:
    #                 self.Trend = -1
    #             else:
    #                 if len(self.Trend_Queue) >= 1:
    #                     self.Trend = self.Trend_Queue[1]
    #                 else:
    #                     self.Trend = 1
        
    #     self.Trend_Queue.appendleft(self.Trend)


    #     if self.Trend == 1:
    #         self.Fast_Atr_Rsi_Tl = self.Long_Band
    #     else:
    #         self.Fast_Atr_Rsi_Tl = self.Short_Band

    #     if self.Fast_Atr_Rsi_Tl is not None:
    #         self.Basis_Queue.appendleft(self.Fast_Atr_Rsi_Tl-50)
        
    #     if len(self.Basis_Queue) == self.Length:
    #         self.Basis = sum(self.Basis_Queue) / self.Length
        
    #     if self.Fast_Atr_Rsi_Tl is not None:
    #         if len(self.Basis_Queue) == self.Length:
    #             self.Dev = self.Mult * stats.stdev(self.Basis_Queue)
        
    #     if self.Dev is not None:
    #         if self.Basis is not None:
    #             self.Upper = self.Basis + self.Dev
    #             self.Lower = self.Basis - self.Dev
        
    #     if self.Upper is not None and self.Lower is not None:
    #         if (self.rsi_sma_warm.Current.Value - 50) > self.Upper:
    #             self.Color_Bar = "GREEN"
    #         elif (self.rsi_sma_warm.Current.Value - 50) < self.Lower:
    #             self.Color_Bar = "RED"
    #         else:
    #             self.Color_Bar = "GRAY"
        

    #     if self.rsi_sma_warm.IsReady:
    #         if self.rsi_sma_warm.Current.Value >= 50:
    #             self.QQE_z_Long = self.QQE_z_Long + 1
    #             self.QQE_z_Short = 0
    #         else:
    #             self.QQE_z_Short = self.QQE_z_Short +1
    #             self.QQE_z_Long = 0
        

    #     if self.rsi_ema.IsReady:
    #         if self.rsi_ema.Current.Value - 50 > self.ThreshHold2:
    #             self.hcolor2 = "SILVER"
    #         elif self.rsi_ema.Current.Value - 50 < 0 - self.ThreshHold2:
    #             self.hcolor2 = "SILVER"
    #         else:
    #             self.hcolor2= None
        
    #     if self.Fast_Atr_Rsi_Tl_2 is not None:
    #         self.QQE_Line = self.Fast_Atr_Rsi_Tl_2 - 50
        
    #     if self.rsi_ema.IsReady:
    #         self.Histo2 = self.rsi_ema.Current.Value - 50

    #         if self.rsi_ema.Current.Value - 50 > self.ThreshHold2:
    #             self.GreenBar1 = True
    #         else:
    #             self.GreenBar1 = False

    #         if self.rsi_ema.Current.Value - 50 < 0 - self.ThreshHold2:
    #             self.RedBar1 = True
    #         else:
    #             self.RedBar1 = False


    #     if self.rsi_sma_warm.IsReady and self.Upper is not None:
    #         if self.rsi_sma_warm.Current.Value - 50 > self.Upper:
    #             self.GreenBar2 = True
    #         else:
    #             self.GreenBar2 = False

    #     if self.rsi_sma_warm.IsReady and self.Lower is not None:
    #         if self.rsi_sma_warm.Current.Value - 50 < self.Lower:
    #             self.RedBar2 = True
    #         else:
    #             self.RedBar2 = False
        

    #     if self.GreenBar1 and self.GreenBar2:
    #         self.QQE_UP = self.rsi_ema.Current.Value - 50
    #     else:
    #         self.QQE_UP = None
        
    #     if self.RedBar1 and self.RedBar2:
    #         self.QQE_DOWN = self.rsi_ema.Current.Value - 50
    #     else:
    #         self.QQE_DOWN = None

    #     self.Warming_Up = False
                


    # def IndicatorUpdate(self, bar):
    #     if not self.Warming_Up:
    #         if self.rsi_tdi.IsReady:
 

    #         TDI_indie = self.Indicators["TDI"]
    #         if self.rsi_tdi.IsReady:
    #             TDI_indie.Bull_Or_Bear(self.rsi_tdi.Current.Value)
    #         if self.Macd.IsReady:
    #             self.Macd.Update(IndicatorDataPoint(bar.EndTime, bar.Close))
    #         donchian_indie = self.Indicators["DONCHIAN"]
        
    #         donchian_indie.Donchian_Channel(bar.High, bar.Low, bar.Close)
    #         donchian_indie.Donchian_Alt(bar.High, bar.Low, bar.Close)
    #         volatility_osc = self.Indicators["VOLATILITY"]
    #         #t0 = time.perf_counter()
    #         volatility_osc.Bull_Or_Bear(bar.Close, bar.Open)
    #         #t1 = time.perf_counter()
    #         #execution_time = t1 - t0
            
    #         #self.Debug(execution_time)

    #         VOLUME_Indie = self.Indicators["VOLUME"]
    #         color = bar.Close - bar.Open
    #         VOLUME_Indie.Bull_Or_Bear(bar.Volume, color)



    #         heikin_ashi = self.Indicators["HEIKINASHI"]
    #         heikin_ashi.Bull_Or_Bear(bar.EndTime, bar.Open, bar.High, bar.Low, bar.Close)


    #         ultra_fast_parrot = self.Indicators["ULTRAPARROT"]
    #         ultra_fast_parrot.Calculate_Parrot(bar.Close, bar.EndTime)
    #         # t1 = time.perf_counter()
    #         # execution_time = t1 - t0
    #         # if execution_time >= 1:
    #         #     self.Debug(execution_time)
    #         # self.Debug(f" {self.Time} {str(volatility_osc.Bullish)}")

    #         # if TDI_indie.Bullish:
    #         #     self.Debug(f" {self.Time} {str(TDI_indie.Bullish)}")

    #         if self.sma_slow.IsReady:
    #             self.sma_slow.Update(IndicatorDataPoint(bar.EndTime, ((bar.Low + bar.High)/2)))

    #         if self.sma_fast.IsReady:
    #             self.sma_fast.Update(IndicatorDataPoint(bar.EndTime, ((bar.Low + bar.High)/2)))
            
    #         if self.sma_fastest.IsReady:
    #             self.sma_fastest.Update(IndicatorDataPoint(bar.EndTime, ((bar.Low + bar.High)/2)))

    #         if self.SMMA_Slow is not None:
    #             src_slow = ((bar.Low + bar.High)/2)
    #             self.SMMA_Slow = (self.SMMA_Slow * (self.SMMA_Slow_Length - 1) + src_slow) / self.SMMA_Slow_Length
    #         if self.SMMA_Fast is not None:
    #             src_fast = ((bar.Low + bar.High)/2)
    #             self.SMMA_Fast = (self.SMMA_Fast * (self.SMMA_Fast_Length - 1) + src_fast) / self.SMMA_Fast_Length
    #         if self.SMMA_Fastest is not None:
    #             src_fastest = ((bar.Low + bar.High)/2)
    #             self.SMMA_Fastest = (self.SMMA_Fastest * (self.SMMA_Fastest_Length - 1) + src_fastest) / self.SMMA_Fastest_Length

    #         ###### 2

    #         if self.rsi_2.IsReady:
    #             self.rsi_2.Update(IndicatorDataPoint(bar.EndTime , bar.Close))


        
                
    #         if self.rsi_ema.IsReady:
    #             self.rsi_2_queue.appendleft(self.rsi_ema.Current.Value)

    #         if len(self.rsi_2_queue) == 3:
    #             self.Atr_Rsi_2 = abs(self.rsi_2_queue[1] - self.rsi_ema.Current.Value)
            
    #         if self.Atr_Rsi_2 is not None:
    #             self.Ema_Atr_Rsi_2.Update(IndicatorDataPoint(bar.EndTime, self.Atr_Rsi_2))
            
    #         if self.Ema_Atr_Rsi_2.IsReady:
    #             self.Dar_2_Ema.Update(IndicatorDataPoint(bar.EndTime, self.Ema_Atr_Rsi_2.Current.Value))

    #         if self.Dar_2_Ema.IsReady:
    #             self.Dar_2 = self.Dar_2_Ema.Current.Value * self.QQE2
            
    #         if self.rsi_ema.IsReady and self.Dar_2 is not None:
    #             self.New_Long_Band_2 = self.rsi_ema.Current.Value + self.Dar_2
    #             self.New_Short_Band_2 = self.rsi_ema.Current.Value - self.Dar_2
            
    #         if len(self.rsi_2_queue) == 3 and len(self.Long_Band_Queue_2) == 3 and self.New_Long_Band_2 is not None:
    #             if self.rsi_2_queue[1] > self.Long_Band_Queue_2[1] and self.rsi_ema.Current.Value > self.Long_Band_Queue_2[1]:
    #                 self.Long_Band_2 = max(self.Long_Band_Queue_2[1], self.New_Long_Band_2)
    #             else:
    #                 self.Long_Band_2 = self.New_Long_Band_2
            
    #         self.Long_Band_Queue_2.appendleft(self.Long_Band_2)
            
    #         if len(self.rsi_2_queue) == 3 and len(self.Short_Band_Queue_2) == 3 and self.New_Short_Band_2 is not None:
    #             if self.rsi_2_queue[1] < self.Short_Band_Queue_2[1] and self.rsi_ema.Current.Value < self.Short_Band_Queue_2[1]:
    #                 self.Short_Band_2 = min(self.Short_Band_Queue_2[1], self.New_Short_Band_2)
    #             else:
    #                 self.Short_Band_2 = self.New_Short_Band_2
            
    #         self.Short_Band_Queue_2.appendleft(self.Short_Band_2)

            



    #         if len(self.Long_Band_Queue_2) == 3 and len(self.rsi_2_queue) == 2:
    #             if self.Long_Band_Queue_2[1] > self.rsi_ema.Current.Value and self.Long_Band_Queue_2[2] < self.rsi_2_queue[1]:
    #                 self.cross_2 = True
    #             elif self.Long_Band_Queue_2[1] < self.rsi_ema.Current.Value  and self.Long_Band_Queue_2[2] > self.rsi_2_queue[1]:
    #                 self.cross_2 = True
    #             else:
    #                 self.cross_2 = False
            
    #         check_2 = False
    #         if len(self.Short_Band_Queue_2) == 3 and len(self.rsi_2_queue) == 2:
    #             if self.Short_Band_Queue_2[1] > self.rsi_ema.Current.Value  and self.Short_Band_Queue_2[2] < self.rsi_2_queue[1]:
    #                 check_2 = True
    #             elif self.Short_Band_Queue_2[1] < self.rsi_ema.Current.Value  and self.Short_Band_Queue_2[2] > self.rsi_2_queue[1]:
    #                 check_2 = True
    #             else:
    #                 check_2 = False
                
    #             if check_2:
    #                 self.Trend_2 = 1
    #             if not check_2:
    #                 if self.cross_2:
    #                     self.Trend_2 = -1
    #                 else:
    #                     if len(self.Trend_Queue_2) >= 1:
    #                         self.Trend_2 = self.Trend_Queue_2[1]
    #                     else:
    #                         self.Trend_2 = 1
            
    #         self.Trend_Queue_2.appendleft(self.Trend_2)


    #         if self.Trend_2 == 1:
    #             self.Fast_Atr_Rsi_Tl_2 = self.Long_Band_2
    #         else:
    #             self.Fast_Atr_Rsi_Tl_2 = self.Short_Band_2

    #         if self.Fast_Atr_Rsi_Tl_2 is not None:
    #             self.Basis_Queue.appendleft(self.Fast_Atr_Rsi_Tl_2-50)

    #         if self.rsi_ema.IsReady:
    #             if self.rsi_ema.Current.Value >= 50:
    #                 self.QQE_z_Long_2 = self.QQE_z_Long_2 + 1
    #                 self.QQE_z_Short_2 = 0
    #             else:
    #                 self.QQE_z_Short_2 = self.QQE_z_Short_2 +1
    #                 self.QQE_z_Long_2 = 0

            
    #         ########### 2

    #         if self.psar.IsReady:
    #             self.psar.Update(bar)

    #         if self.rsi.IsReady:
    #             self.rsi.Update(IndicatorDataPoint(bar.EndTime, bar.Close))


    #         if self.rsi.IsReady and self.rsi_sma.IsReady:
    #             self.rsi_sma_queue.appendleft(self.rsi_sma.Current.Value)

    #             if len(self.rsi_sma_queue) == 3:
    #                 self.atr_rsi = abs(self.rsi_sma_queue[1] - self.rsi_sma.Current.Value)
            
    #         if self.atr_rsi is not None:
    #             self.ma_atr_rsi.Update(IndicatorDataPoint(self.Time, self.atr_rsi))

    #         if self.ma_atr_rsi.IsReady:
    #             self.dar_ema.Update(IndicatorDataPoint(self.Time, self.ma_atr_rsi.Current.Value))
                
    #         if self.dar_ema.IsReady:
    #             self.dar = self.dar_ema.Current.Value * self.QQE
            

    #             if self.dar is not None and self.rsi_sma.IsReady:
    #                 self.New_Long_Band = self.rsi_sma.Current.Value - self.dar
    #                 self.New_Short_Band = self.rsi_sma.Current.Value + self.dar
                
    #             if len(self.rsi_sma_queue) == 3 and len(self.Long_Band_Queue) == 3 and self.New_Long_Band is not None:

    #                 if self.rsi_sma_queue[1] > self.Long_Band_Queue[1] and self.rsi_sma_queue[0] > self.Long_Band_Queue[1]:
    #                     self.Long_Band = max(self.Long_Band_Queue[1], self.New_Long_Band)
    #                 else:
    #                     self.Long_Band = self.New_Long_Band
                
    #             self.Long_Band_Queue.appendleft(self.Long_Band)


    #             if len(self.rsi_sma_queue) == 3 and len(self.Short_Band_Queue) == 3 and self.New_Short_Band is not None:

    #                 if self.rsi_sma_queue[1] < self.Short_Band_Queue[1] and self.rsi_sma_queue[0] < self.Short_Band_Queue[1]:
    #                     self.Short_Band = min(self.Short_Band_Queue[1], self.New_Short_Band)
    #                 else:
    #                     self.Short_Band = self.New_Short_Band
                
    #             self.Short_Band_Queue.appendleft(self.Short_Band)



    #             if self.Long_Band_Queue[1] > self.rsi_sma.Current.Value and self.Long_Band_Queue[2] < self.rsi_sma_queue[1]:
    #                 self.cross_1 = True
    #             elif self.Long_Band_Queue[1] < self.rsi_sma.Current.Value and self.Long_Band_Queue[2] > self.rsi_sma_queue[1]:
    #                 self.cross_1 = True
    #             else:
    #                 self.cross_1 = False
                
    #             check = False

    #             if self.Short_Band_Queue[1] > self.rsi_sma.Current.Value and self.Short_Band_Queue[2] < self.rsi_sma_queue[1]:
    #                 check = True
    #             elif self.Short_Band_Queue[1] < self.rsi_sma.Current.Value and self.Short_Band_Queue[2] > self.rsi_sma_queue[1]:
    #                 check = True
    #             else:
    #                 check = False
                
    #             if check:
    #                 self.Trend = 1
    #             if not check:
    #                 if self.cross_1:
    #                     self.Trend = -1
    #                 else:
    #                     if len(self.Trend_Queue) >= 1:
    #                         self.Trend = self.Trend_Queue[1]
    #                     else:
    #                         self.Trend = 1
                
    #             self.Trend_Queue.appendleft(self.Trend)


    #             if self.Trend == 1:
    #                 self.Fast_Atr_Rsi_Tl = self.Long_Band
    #             else:
    #                 self.Fast_Atr_Rsi_Tl = self.Short_Band
                
    #             if self.Fast_Atr_Rsi_Tl is not None:
    #                 self.Basis_Queue.appendleft(self.Fast_Atr_Rsi_Tl-50)
                
    #             if len(self.Basis_Queue) == self.Length:
    #                 self.Basis = sum(self.Basis_Queue) / self.Length
                
    #             if self.Fast_Atr_Rsi_Tl is not None:
    #                 if len(self.Basis_Queue) == self.Length:
    #                     self.Dev = self.Mult * stats.stdev(self.Basis_Queue)
                
    #             if self.Dev is not None:
    #                 if self.Basis is not None:
    #                     self.Upper = self.Basis + self.Dev
    #                     self.Lower = self.Basis - self.Dev
                
    #             if self.Upper is not None and self.Lower is not None:
    #                 if (self.rsi_sma.Current.Value - 50) > self.Upper:
    #                     self.Color_Bar = "GREEN"
    #                 elif (self.rsi_sma.Current.Value - 50) < self.Lower:
    #                     self.Color_Bar = "RED"
    #                 else:
    #                     self.Color_Bar = "GRAY"
                
    #             if self.rsi_sma.IsReady:
    #                 if self.rsi_sma.Current.Value >= 50:
    #                     self.QQE_z_Long = self.QQE_z_Long + 1
    #                     self.QQE_z_Short = 0
    #                 else:
    #                     self.QQE_z_Short = self.QQE_z_Short +1
    #                     self.QQE_z_Long = 0


    #             if self.rsi_ema.IsReady:
    #                 if self.rsi_ema.Current.Value - 50 > self.ThreshHold2:
    #                     self.hcolor2 = "SILVER"
    #                 elif self.rsi_ema.Current.Value - 50 < 0 - self.ThreshHold2:
    #                     self.hcolor2 = "SILVER"
    #                 else:
    #                     self.hcolor2= None
                
    #             if self.Fast_Atr_Rsi_Tl_2 is not None:
    #                 self.QQE_Line = self.Fast_Atr_Rsi_Tl_2 - 50
                
    #             if self.rsi_ema.IsReady:
    #                 self.Histo2 = self.rsi_ema.Current.Value - 50

    #                 if self.rsi_ema.Current.Value - 50 > self.ThreshHold2:
    #                     self.GreenBar1 = True
    #                 else:
    #                     self.GreenBar1 = False

    #                 if self.rsi_ema.Current.Value - 50 < 0 - self.ThreshHold2:
    #                     self.RedBar1 = True
    #                 else:
    #                     self.RedBar1 = False


    #             if self.rsi_sma.IsReady and self.Upper is not None:
    #                 if self.rsi_sma.Current.Value - 50 > self.Upper:
    #                     self.GreenBar2 = True
    #                 else:
    #                     self.GreenBar2 = False

    #             if self.rsi_sma.IsReady and self.Lower is not None:
    #                 if self.rsi_sma.Current.Value - 50 < self.Lower:
    #                     self.RedBar2 = True
    #                 else:
    #                     self.RedBar2 = False
                

    #             if self.GreenBar1 and self.GreenBar2:
    #                 self.QQE_UP = self.rsi_ema.Current.Value - 50
    #             else:
    #                 self.QQE_UP = None
                
    #             if self.RedBar1 and self.RedBar2:
    #                 self.QQE_DOWN = self.rsi_ema.Current.Value - 50
    #             else:
    #                 self.QQE_DOWN = None

    def OnData(self, data: Slice):
        self.Debug(data.Bars[self.Crypto])
        # # self.Debug("HERE")
        # volatility_osc = self.Indicators["VOLATILITY"]
        # donchian_indie = self.Indicators["DONCHIAN"]
        # TDI_indie = self.Indicators["TDI"]
        # VOLUME_Indie = self.Indicators["VOLUME"]
        # heikin_ashi = self.Indicators["HEIKINASHI"]
        # ultra_fast_parrot = self.Indicators["ULTRAPARROT"]
         
        # # self.Debug(f" {self.Time} {ultra_fast_parrot.TSI_Hist_Color}")

        # if volatility_osc.Bullish and donchian_indie.Color == "GREEN" and self.QQE_UP is not None and TDI_indie.Bullish:
        #     if not self.Portfolio[self.Crypto].IsLong:
        #         self.SetHoldings(self.Crypto, 1)
     


        # if volatility_osc.Bearish and donchian_indie.Color == "RED" and self.QQE_DOWN is not None and TDI_indie.Bearish:
        #     if not self.Portfolio[self.Crypto].IsShort:
        #         self.SetHoldings(self.Crypto, -1)

       

        # if self.Portfolio[self.Crypto].Invested:
        #     if self.Portfolio[self.Crypto].UnrealizedProfitPercent > 0.01:
        #         self.SetHoldings(self.Crypto, 0)

        #     if self.Portfolio[self.Crypto].UnrealizedProfitPercent < -0.05:
        #         self.SetHoldings(self.Crypto, 0)
    
    
    def TrainingMethod(self):

        self.Log(f'Start training at {self.Time}')
        # Use the historical data to train the machine learning model
        history = self.History(["SPY"], 200, Resolution.Daily)

        # ML code:
        pass
    