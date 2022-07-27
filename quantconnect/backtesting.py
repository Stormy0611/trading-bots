
from AlgorithmImports import *
import datetime

### <summary>
### Simple indicator demonstration algorithm of MACD
### </summary>
### <meta name="tag" content="indicators" />
### <meta name="tag" content="indicator classes" />
### <meta name="tag" content="plotting indicators" />

"""
    class QCAlgorithm:
        Securities   # Array of Security objects.
        Portfolio    # Array of SecurityHolding objects
        Transactions # Transactions helper
        Schedule     # Scheduling helper
        Notify       # Email, SMS helper
        Universe     # Universe helper

        # Set up Requested Data, Cash, Time Period.
        def Initialize(self) -> None:

        # Other Event Handlers
        def OnData(self, slice: Slice) -> None:
        def OnEndOfDay(self, symbol: Symbol) -> None:
        def OnEndOfAlgorithm(self) -> None:

        # Indicator Helpers
        def SMA(self, symbol: Symbol, period: int) -> SimpleMovingAverage:
"""
class MACDTrendAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2021, 1, 1)  # Set Start Date
        # self.SetEndDate(2015, 1, 1)      #Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        # Find more symbols here: http://quantconnect.com/data
        self.AddEquity("SPY", Resolution.Daily)

        # define our daily macd(12,26) with a 9 day signal
        self.__macd = self.MACD(
            "SPY", 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
        self.__previous = datetime.min
        self.PlotIndicator("MACD", True, self.__macd, self.__macd.Signal)
        self.PlotIndicator("SPY", self.__macd.Fast, self.__macd.Slow)

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # wait for our macd to fully initialize
        if not self.__macd.IsReady:
            return

        # only once per day
        if self.__previous.date() == self.Time.date():
            return

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.0025

        holdings = self.Portfolio["SPY"].Quantity

        signalDeltaPercent = (self.__macd.Current.Value -
                              self.__macd.Signal.Current.Value)/self.__macd.Fast.Current.Value

        # if our macd is greater than our signal, then let's go long
        if holdings <= 0 and signalDeltaPercent > tolerance:  # 0.01%
            # longterm says buy as well
            self.SetHoldings("SPY", 1.0)

        # of our macd is less than our signal, then let's go short
        elif holdings >= 0 and signalDeltaPercent < -tolerance:
            self.Liquidate("SPY")

        self.__previous = self.Time
