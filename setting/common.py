import FinanceDataReader as fdr
import numpy as np
import pandas as pd

def getHistory(tickers, names) :
    data = pd.DataFrame()
    for i in range(0, len(tickers)) :
        raw = fdr.DataReader(tickers[i])
        data[names[i]] = raw['Close']
    return data.dropna()

def getWeightByAbsoluteMomentum(assets, months=12) :
    momentum = assets / assets.shift(months) - 1
    print('momentum \n', momentum.head(30))

    weights = pd.DataFrame(np.zeros((len(assets),2)), columns=assets.columns)
    weights['Date'] = assets.index
    weights = weights.set_index('Date')

    for i in range(0, len(weights)):
        if momentum[assets.columns[0]].iloc[i] >= 0:
            weights[assets.columns[0]].iloc[i] = 1
        else:
            weights[assets.columns[1]].iloc[i] = 1
    return weights

def getWeightByAvgMomentumScore(assets):
    sumOfmomentum = 0
    sumOfscore = 0
    for i in range(1, 13):
        sumOfmomentum = assets / assets.shift(i) + sumOfmomentum
        sumOfscore = np.where(assets / assets.shift(i) > 1, 1,0) + sumOfscore
    
    sumOfmomentum[sumOfmomentum > 0] = sumOfscore/12
    return sumOfmomentum