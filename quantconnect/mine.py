# region imports
from AlgorithmImports import *
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

        self.symbol = self.AddCrypto("BTCUSD", Resolution.Minute)
        # self.AddForex("EURUSD", Resolution.Second) # Add EURUSD 1 second bars

        # Feed in 100 trading days worth of data before the start date
        # self.SetWarmUp(100, Resolution.Minute)

        self.sma_short = self.SMA(self.symbol, 10)
        self.sma_long = self.SMA(self.symbol, 20)

    # def CustomSecurityInitializer(self, security: Security) -> None:
    #     # Disable trading fees
    #     security.SetFeeModel(ConstantFeeModel(0, "USD"))

    # def OnWarmUpFinished(self) -> None:
    #     self.Log("Algorithm Ready")

    def OnData(self, data: Slice):
        self.PlotIndicator("<chartName>", self.sma_short, self.sma_long)

    def OnEndOfAlgorithm(self):
        self.Log("Algorithm done")
