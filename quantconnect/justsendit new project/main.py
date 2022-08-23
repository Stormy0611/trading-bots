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
from vwma import VWMA


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
        self.Indicators['VOL_MA'] = VOL_MA(self, length=self.VOL_MA_LENGTH)
        self.Indicators['VWMA1'] = VWMA(self, length=self.VWMA1_LENGTH)
        self.Indicators['VWMA2'] = VWMA(self, length=self.VWMA2_LENGTH)
        self.Indicators['VWMA3'] = VWMA(self, length=self.VWMA3_LENGTH)
        self.Indicators['VWMA4'] = VWMA(self, length=self.VWMA4_LENGTH)
        self.Indicators['VOL_OSC'] = VOL_OSC(self, 
                                            short=self.VOL_OSC_SHORT_LENGTH, 
                                             long=self.VOL_OSC_LONG_LENGTH)
        self.Indicators['PGO_LB'] = PGO_LB(self, length=self.PGO_LB_LENGTH)
        self.Indicators['TSI'] = TSI(self, 
                                    short=self.TSI_SHORT_LENGTH,
                                     long=self.TSI_LONG_LENGTH,
                                     signal=self.TSI_SIGNAL_LENGTH)
        self.Indicators['RVGI'] = RVGI(self, length=self.RVGI_LENGTH)
        self.Indicators['STC'] = STC(self, 
                                    length=self.STC_LENGTH,
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



    

    def OnData(self, data: Slice):
        
        # self.Debug(data.Bars[self.Crypto].EndTime)
        # self.Debug(data.Bars[self.Crypto].Close)
        # self.Debug(data.Bars[self.Crypto].Open)
        # self.Debug(data.Bars[self.Crypto].High)
        # self.Debug(data.Bars[self.Crypto].Low)
        # self.Debug(data.Bars[self.Crypto].Volume)
        
        vol_ma = self.Indicators['VOL_MA']
        vwma1 = self.Indicators['VWMA1']
        vwma2 = self.Indicators['VWMA2']
        vwma3 = self.Indicators['VWMA3']
        vwma4 = self.Indicators['VWMA4']
        vol_osc = self.Indicators['VOL_OSC']
        pgo_lb = self.Indicators['PGO_LB']
        tsi = self.Indicators['TSI']
        rvgi = self.Indicators['RVGI']
        stc = self.Indicators['STC']
        
        vol_ma.Update(data.Bars[self.Crypto].Volume)
        vwma1.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Volume,
                     data.Bars[self.Crypto].Close)
        vwma2.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Volume,
                     data.Bars[self.Crypto].Close)
        
        vwma3.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Volume,
                     data.Bars[self.Crypto].Close)
        vwma4.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Volume,
                     data.Bars[self.Crypto].Close)
        vol_osc.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Volume)
        pgo_lb.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Close)
        tsi.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Close)
        rvgi.Update(data.Bars[self.Crypto])
        stc.Update(data.Bars[self.Crypto].EndTime, 
                     data.Bars[self.Crypto].Close)
        
        
        
        
         
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
        history = self.History(["ADAUSD"], 200, Resolution.Daily)

        # ML code:
        pass
    