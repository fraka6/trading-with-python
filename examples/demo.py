''' simulate a buy/sale strategy on a stock & evaluate its PnL (profit and Lost) '''
#!pip install mlboost
from util import strategy 
reload(strategy)

charts = True
verbose = True

months=12

#stock ="AAPL"
#stock='TA' #oil
#stock='BP' # oil

stock = 'TSLA'

summary = strategy.eval(stock, field='open', months=months, 
                  initialCash=10000, min_stocks=50, 
                  charts=charts, verbose=verbose);

print stock, summary.ix[-1:,'cash':]
