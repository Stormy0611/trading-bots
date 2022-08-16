# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from AlgorithmImports import *
from QuantConnect.Indicators import *
from QuantConnect import *
from collections import deque

### <summary>
### Basic template algorithm simply initializes the date range and cash. This is a skeleton
### framework you can use for designing an algorithm.
### </summary>
### <meta name="tag" content="using data" />
### <meta name="tag" content="using quantconnect" />
### <meta name="tag" content="trading and orders" />
# class BasicTemplateAlgorithm(QCAlgorithm):
#     '''Basic template algorithm simply initializes the date range and cash'''

#     def Initialize(self):
#         '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

#         self.SetStartDate(2013,10, 7)  #Set Start Date
#         self.SetEndDate(2013,10,11)    #Set End Date
#         self.SetCash(100000)           #Set Strategy Cash
#         # Find more symbols here: http://quantconnect.com/data
#         self.AddEquity("SPY", Resolution.Minute)
#         self.Debug("numpy test >>> print numpy.pi: " + str(np.pi))
        # region imports

# endregion


class CryingApricotBison(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetEndDate(2022, 6, 30)

        # self.SetAccountCurrency("BTC")

        self.SetCash("BTC", 100000)  # Set Strategy Cash

        # self.SetCash("BTC", 1)

        # self.SetBrokerageModel(BrokerageName.GDAX, AccountType.Cash)
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
        # self.vwma50.Updated += self.CustomUpdated
        self.RegisterIndicator(self.symbol, self.vwma50, Resolution.Minute)
        self.PlotIndicator("VWMA 50", self.vwma50)

        self.vwma100 = VolumeWeightMovingAverage("VWMA 100", self.symbol, 100)
        # self.vwma100.Updated += self.CustomUpdated
        self.RegisterIndicator(self.symbol, self.vwma100, Resolution.Minute)
        self.PlotIndicator("VWMA 100", self.vwma100)

        self.vwma200 = VolumeWeightMovingAverage("VWMA 200", self.symbol, 200)
        # self.vwma200.Updated += self.CustomUpdated
        self.RegisterIndicator(self.symbol, self.vwma200, Resolution.Minute)
        self.PlotIndicator("VWMA 200", self.vwma200)

        # self.customWindow = RollingWindow[IndicatorDataPoint](5)

        # self.vwap = self.VWAP(self.symbol)
        # self.PlotIndicator("VWAP", self.vwap)

    # def CustomSecurityInitializer(self, security: Security) -> None:
    #     # Disable trading fees
    #     security.SetFeeModel(ConstantFeeModel(0, "USD"))

    # def OnWarmUpFinished(self) -> None:
    #     self.Log("Algorithm Ready")

    # def CustomUpdated(self, sender, updated):
    #     self.customWindow.Add(updated)

    # def OnData(self, data: Slice):
    #     self.Debug(data.Bars[self.symbol].Close)
    #     self.PlotIndicator("VWMA 50", self.vwma50)
    #     self.PlotIndicator("VWMA 100", self.vwma100)
    #     self.PlotIndicator("VWMA 200", self.vwma200)

    def OnEndOfAlgorithm(self):
        self.Debug("Algorithm done")


# class VolumeWeightMovingAverage(PythonIndicator):
class VolumeWeightMovingAverage:
    def __init__(self, name, symbol, period):
        self.Name = name
        self.Symbol = symbol
        self.WarmUpPeriod = period
        self.Time = datetime.min
        self.IsReady = False
        self.Value = 0
        self.queue_vol = deque(maxlen=period)
        self.queue_clo = deque(maxlen=period)
        # self.tradebar_indicator = TradeBarIndicator(name)

    def __repr__(self):
        return "{0} -> IsReady: {1}. Time: {2}. Value: {3}".format(self.Name, self.IsReady, self.Time, self.Value)

    def Update(self, input):
        # self.queue.appendleft(input.Close)
        # QCAlgorithm.Debug(self.tradebar_indicator.Bars[self.Symbol].Close)
        self.volume
        self.queue_clo.appendleft(input.Close)
        self.queue_vol.appendleft(input.Volume)
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


    # def OnData(self, data):
    #     '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
    #     Arguments:
    #         data: Slice object keyed by symbol containing the stock data
    #     '''
    #     if not self.Portfolio.Invested:
    #         self.SetHoldings("SPY", 1)
