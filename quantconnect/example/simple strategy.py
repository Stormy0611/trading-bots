'''
Universe: SPY and IEF
Timeframe: Daily (the only reason why it is on minute is because we need the OnOrderEvent)
Position size: 50%
Buy rules: After the market closes, buy on Market-On-Open order if the 3-day cumulative RSI(2) < 15.
    Use a stoploss with 2*ATR(1) below the open price (which is the same as fill price)
Sell rules: After the market closes, sell if RSI(2) < 70 using MOO order.

Needing almost 80 lines of code for this simple strategy seems a bit too much. Can the code be made more efficient/smaller?
Also: is there an easy way to 'attach' a stop order to a market order such that when the position gets closed,
    the stop order is automatically cancelled?
'''
class RSI_Strategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1) 
        self.SetEndDate(2020, 1, 1)
        self.SetCash(100000)
        self.percentPerStock = 0.5 #Position size is 50%
        
        self.spy = self.AddEquity("SPY", Resolution.Minute).Symbol
        self.ief = self.AddEquity("IEF", Resolution.Minute).Symbol
        
        self.amountSPY = 0
        self.amountIEF = 0
        
        self.stopTicketSPY = 0
        self.stopTicketIEF = 0
        
        #Indicators
        self.rsi_SPY = self.RSI("SPY", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.RW_rsi_SPY = RollingWindow[float](3)
        
        self.rsi_IEF = self.RSI("IEF", 2, MovingAverageType.Wilders, Resolution.Daily)
        self.RW_rsi_IEF = RollingWindow[float](3)

    def OnData(self, data):
        if not data.ContainsKey(self.spy) or not data.ContainsKey(self.ief) or not self.Time.hour == 16 or not self.Time.minute == 0:
            return
        
        if self.rsi_SPY.IsReady and self.rsi_IEF.IsReady:
            self.RW_rsi_SPY.Add(self.rsi_SPY.Current.Value)
            self.RW_rsi_IEF.Add(self.rsi_IEF.Current.Value)
            
        if self.RW_rsi_SPY.IsReady and self.RW_rsi_IEF.IsReady:
            cumRSI_SPY = sum(list(self.RW_rsi_SPY))
            cumRSI_IEF = sum(list(self.RW_rsi_IEF))
            
            dollarAmount = self.percentPerStock*self.Portfolio.TotalPortfolioValue 
            
            #Buy rules
            if cumRSI_SPY < 15 and not self.Securities[self.spy].Invested:
                self.amountSPY = int(dollarAmount/data[self.spy].Close)
                self.MarketOnOpenOrder(self.spy, self.amountSPY)
                
            if cumRSI_IEF < 15 and not self.Securities[self.ief].Invested:
                self.amountIEF = int(dollarAmount/data[self.ief].Close)
                self.MarketOnOpenOrder(self.ief, self.amountIEF)
        
        #Sell rules
        if self.Securities[self.spy].Invested and self.rsi_SPY.Current.Value > 70:
            self.Liquidate(self.spy)
            #Cancel SL order
            self.stopTicketSPY.Cancel()
            
        if self.Securities[self.ief].Invested and self.rsi_IEF.Current.Value > 70:
            self.Liquidate(self.ief)
            #Cancel SL order
            self.stopTicketIEF.Cancel()
        
    #Attach a stop order to the market order. The reason why this cannot be done in the OnData code is 
    #that we cannot know the fill price before the order gets filled.
    def OnOrderEvent(self, orderEvent):
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        #If a market on open order gets filled
        if orderEvent.Status == OrderStatus.Filled and orderEvent.FillQuantity > 0: 
            fillPrice = orderEvent.FillPrice
            
            #Calculate 1 day ATR
            history = self.History(orderEvent.Symbol, 2, Resolution.Daily)
            previousClose = history['close'].iloc[0]
            high = history['high'].iloc[1]
            low = history['low'].iloc[1]
            atr = max(abs(high - low), abs(low - previousClose), abs(high - previousClose))
            
            #Set SL order
            if orderEvent.Symbol == self.spy:
                self.stopTicketSPY = self.StopMarketOrder(self.spy, -self.amountSPY, fillPrice - 2*atr)
            if orderEvent.Symbol == self.ief:
                self.stopTicketIEF = self.StopMarketOrder(self.ief, -self.amountIEF, fillPrice - 2*atr)