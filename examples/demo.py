from util import strategy 
reload(strategy)
#strategy.eval(stockname='TSLA', field='open', months=12, initialCash=20000, min_stocks=30, charts=True)

# try current strategy on different stock
for stock in ["TSLA", "GS", "SCTY", "AMZN", "CSCO"]:
  strategy.eval(stock, field='open', months=12, initialCash=20000, min_stocks=30, charts=True)


