
import numpy as np
from trendy import segtrends
import pandas as pd
import tradingWithPython as twp
from filter import movingaverage

def orders_from_trends(x, segments=2, charts=True, window=7, momentum=False):
    ''' generate orders from segtrends '''
    x_maxima, maxima, x_minima, minima = segtrends(x, segments, charts, window)
    n = len(x)
    y = np.array(x)
    movy = movingaverage(y, window)

    # generate order strategy
    orders = np.zeros(n)
    last_buy = y[0]
    last_sale = y[0]

    for i in range(1,n):
        # get 2 latest support point y values prior to x
        pmin = list(minima[np.where(x_minima<=i)][-2:])
        pmax = list(maxima[np.where(x_maxima<=i)][-2:])
        # sell if support slop is negative
        min_sell = True if ((len(pmin)==2) and (pmin[1]-pmin[0])<0) else False 
        max_sell = True if ((len(pmax)==2) and (pmax[1]-pmax[0])<0) else False 

        # if support down, sell
        buy = -1 if (min_sell and max_sell) else 0
        # buy only if lower the moving average else sale
        buy = 1 if ((buy == 0) and (y[i]<movy[i])) else -1
        # sell only if ...
        buy= -1 if ((buy == -1) and y[i]>last_buy) else 1
      
        buy_price_dec = y[i]<last_buy
        sale_price_dec = y[i]<last_sale
        orders[i] = buy
        last_buy = y[i] if (buy==1) else last_buy
        last_sale = y[i] if (buy==-1) else last_sale
        
        import math
        if momentum:
            # add momentum for buy 
            if (buy==1) and (orders[i-1]>=1):
                #if buy_price_dec:
                orders[i]=round(math.log(2*orders[i-1])+1)
                #else:
                 #   orders[i]=max(1, round(orders[i-1]/2))
            # add momentum for sale
            elif (buy==-1) and (orders[i-1]<=-1):
                #if sale_price_dec:
                orders[i]*=round(math.log(abs(orders[i-1]*2))+1)
                #else:
                #    orders[i]=max(1, round(orders[i-1]/2))

    # OUTPUT
    return orders

def orders2strategy(orders, price, min_stocks=1):
    strategy = pd.Series(index=price.index) 
    orders=[el*min_stocks for el in orders]
    # create a stratgy from order
    for i, idx in enumerate(price.index):
        if orders[i]!=0:
            strategy[idx] = orders[i]
    return strategy

def eval(stockname='TSLA', field='open', months=12, 
             initialCash=20000, min_stocks=30, charts=True):
    import tradingWithPython.lib.yahooFinance as yahoo 
    from pylab import title, figure
    n = (5*4)*months
    price = yahoo.getHistoricData(stockname)[field][-n:] 
    if charts:
        title('automatic strategy')
    orders = orders_from_trends(price, segments=n/5, charts=charts, 
                                momentum=True); 
    strategy = orders2strategy(orders, price, min_stocks)
        
    # do the backtest
    bt = twp.Backtest(price, strategy, initialCash=initialCash, signalType='shares')
    if charts:
        bt.plotTrades()
        figure()
        bt.pnl.plot()
        title('pnl')
        
        bt.data.plot()
        title('all strategy data')

