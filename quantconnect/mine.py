# region imports
from AlgorithmImports import *
# endregion


class CryingApricotBison(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetEndDate(2022, 6, 30)
        # self.SetAccountCurrency("BTC")
        self.SetCash(100000)  # Set Strategy Cash
        # self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Cash)
        self.SetSecurityInitializer(self.CustomSecurityInitializer)
        # self.SetSecurityInitializer(lambda security: security.SetFeeModel(ConstantFeeModel(0, "USD")))

        self.AddForex("EURUSD", Resolution.Second)  # Add EURUSD 1 second bars

        # self.__symbol = "AAPL"
        self.__symbol = self.AddEquity("AAPL", Resolution.Minute).Symbol
        self.sma_short = self.SMA(self.__symbol, 10)
        self.sma_long = self.SMA(self.__symbol, 20)

    def CustomSecurityInitializer(self, security: Security) -> None:
        # Disable trading fees
        security.SetFeeModel(ConstantFeeModel(0, "USD"))

    def OnData(self, data: Slice):
        self.PlotIndicator("<chartName>", self.sma_short, self.sma_long)

    def OnEndOfAlgorithm(self):
        self.Debug("Algorithm done")
