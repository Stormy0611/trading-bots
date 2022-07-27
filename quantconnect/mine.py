# region imports
from AlgorithmImports import *
from Lean.Indicators import *
# from QuantConnect.Indicators import *
from QuantConnect import *
from collections import deque
# endregion


class CryingApricotBison(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetEndDate(2022, 6, 30)

        # self.SetAccountCurrency("BTC")

        self.SetCash(100000)  # Set Strategy Cash

        self.SetCash("BTC", 1)

        self.SetBrokerageModel(BrokerageName.GDAX, AccountType.Cash)
        # self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Cash)

        # self.SetSecurityInitializer(self.CustomSecurityInitializer)
        # self.SetSecurityInitializer(lambda security: security.SetFeeModel(ConstantFeeModel(0, "USD")))

        self.symbol = self.AddCrypto("BTCUSD", Resolution.Minute).Symbol
        # self.AddForex("EURUSD", Resolution.Second) # Add EURUSD 1 second bars

        # Feed in 100 trading days worth of data before the start date
        # self.SetWarmUp(100, Resolution.Minute)

        # Create a QuantConnect indicator and a python custom indicator for comparison
        self.vwma50 = VolumeWeightMovingAverage("VWMA 50", self.symbol, 50)
        # The python custom class must inherit from PythonIndicator to enable Updated event handler
        self.vwma50.Updated += self.CustomUpdated
        self.RegisterIndicator(self.symbol, self.vwma50, Resolution.Minute)
        self.PlotIndicator("VWMA 50", self.vwma50)

        self.vwma100 = VolumeWeightMovingAverage("VWMA 100", self.symbol, 100)
        self.vwma100.Updated += self.CustomUpdated
        self.RegisterIndicator(self.symbol, self.vwma100, Resolution.Minute)
        self.PlotIndicator("VWMA 100", self.vwma100)

        self.vwma200 = VolumeWeightMovingAverage("VWMA 200", self.symbol, 200)
        self.vwma200.Updated += self.CustomUpdated
        self.RegisterIndicator(self.symbol, self.vwma200, Resolution.Minute)
        self.PlotIndicator("VWMA 200", self.vwma200)

        self.customWindow = RollingWindow[IndicatorDataPoint](5)

        self.vwap = self.VWAP(self.symbol)
        self.PlotIndicator("VWAP", self.vwap)

    # def CustomSecurityInitializer(self, security: Security) -> None:
    #     # Disable trading fees
    #     security.SetFeeModel(ConstantFeeModel(0, "USD"))

    # def OnWarmUpFinished(self) -> None:
    #     self.Log("Algorithm Ready")

    def CustomUpdated(self, sender, updated):
        self.customWindow.Add(updated)

    # def OnData(self, data: Slice):
    #     self.Debug(data.Bars[self.symbol].Close)
    #     self.PlotIndicator("VWMA 50", self.vwma50)
    #     self.PlotIndicator("VWMA 100", self.vwma100)
    #     self.PlotIndicator("VWMA 200", self.vwma200)

    def OnEndOfAlgorithm(self):
        self.Debug("Algorithm done")


class VolumeWeightMovingAverage(PythonIndicator):
    def __init__(self, name, symbol, period):
        self.Name = name
        self.Symbol = symbol
        self.WarmUpPeriod = period
        self.Time = datetime.min
        self.Value = 0
        self.queue_vol = deque(maxlen=period)
        self.queue_clo = deque(maxlen=period)

    def Update(self, input: BaseData):
        # self.queue.appendleft(input.Value)
        self.queue_clo.appendleft(self.Bars[self.Symbol].Close)
        self.queue_vol.appendleft(self.Bars[self.Symbol].Volume)
        count = len(self.queue_vol)
        self.Time = input.Time
        self.Value = 0
        for i in range(count):
            self.Value += self.queue_clo[i] * self.queue_vol
        self.Value /= sum(self.queue_vol)
        return count == self.queue_vol.maxlen


class HLC3(PythonIndicator):
    def __init__(self, name, symbol, period):
        self.Name = name
        self.Symbol = symbol
        self.WarmUpPeriod = period
        self.Time = datetime.min
        self.Value = 0
        self.queue = deque(maxlen=period)

    def Update(self, input: BaseData):
        # self.queue.appendleft(input.Value)
        self.Value = (self.Bars[self.Symbol].High +
                      self.Bars[self.Symbol].Low + self.Bars[self.Symbol].Close) / 3
        self.queue.appendleft(self.Value)
        count = len(self.queue)
        self.Time = input.Time
        return count == self.queue.maxlen
