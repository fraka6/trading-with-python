#!pip install mlboost
from util import strategy 
reload(strategy)

charts = False
verbose = True
months=12

stock ="BBD.B"
stock ="AAPL"
#stock="GAZP" #don't work
#stock='TA' #oil
#stock='BP' # oil
#stock='XOM'# don't work

stocks = ["TSLA", "GS", "SCTY", "AMZN", "CSCO", 
          'UTX','JCI',"GOOGL",'AAPL','BP']
if False:
  x=strategy.eval(stock, field='open', months=months, 
                  initialCash=10000, min_stocks=50, 
                  charts=charts, verbose=verbose)
  print stock, x.ix[-1:,'cash':]
else:
  # try current strategy on different stock
  strategy.eval_best(stocks, field='open', months=months, 
                  initialCash=10000, min_stocks=50, 
                  charts=charts, verbose=verbose)
  