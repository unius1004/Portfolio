import yfinance as yf
import FinanceDataReader as fdr
import numpy as np
import pandas as pd

def getHistoryByFdr(tickers, names) :
    data = pd.DataFrame()
    for i in range(0, len(tickers)) :
        raw = fdr.DataReader(tickers[i])
        data[names[i]] = raw['Close']
    return data.dropna()

def getHistoryByYf(tickers, names) :
    data = yf.download(tickers)['Adj Close']
    if (len(tickers) > 1):
        data = data[tickers]
    else:
        data = data.to_frame()
        data = data.rename(columns={'Adj Close':names[0]})
    return data.dropna()

# 투자자산(asset[0])의 n(=months)개월 절대모멘텀을 비교하여 양수이면 100% 비중, 아니면 안전자산(asset[1]) 100% 비중
def getWeightByAbsoluteMomentum(assets, months=12) :
    momentum = assets / assets.shift(months) - 1
    print('momentum \n', momentum)

    weights = pd.DataFrame(np.zeros((len(assets),2)), columns=assets.columns)
    weights['Date'] = assets.index
    weights = weights.set_index('Date')

    for i in range(0, len(weights)):
        if momentum[assets.columns[0]].iloc[i] >= 0:
            weights[assets.columns[0]].iloc[i] = 1
        else:
            weights[assets.columns[1]].iloc[i] = 1
    return weights

# 12개월 평균모멘텀 스코어 산출
def getWeightByAvgMomentumScore(assets):
    sumOfmomentum = 0
    sumOfscore = 0
    for i in range(1, 13):
        sumOfmomentum = assets / assets.shift(i) + sumOfmomentum
        sumOfscore = np.where(assets / assets.shift(i) > 1, 1,0) + sumOfscore
    
    sumOfmomentum[sumOfmomentum > 0] = sumOfscore/12
    return sumOfmomentum

# 기준자산(dualticker[0])과 투자자산(ticker)의 순위(rank)내 자산의 n(=month)개월 모멘텀을 비교하여 기준자산보다 좋으면 ticker선택, 아니면 안전자산(dualticker[1])을 선택
def getDualMomentumAsset(assets, months, rank, tickers, dualtickers) :
    momentum = assets.pct_change(periods=months)
    #print('momentum head(20) \n', momentum.head(50))
    #print('momentum tail \n', momentum.tail())
    
    mom_rank = momentum[tickers].rank(ascending=False,axis=1)
    #print('mom_rank head(20) \n', mom_rank.head(50))
    #print('mom_rank tail \n', mom_rank.tail)

    selected = pd.DataFrame(columns = momentum.columns)
    for i in range(0, momentum.shape[0]):
        stat = pd.DataFrame(np.zeros((1,len(momentum.columns)) , dtype=int), columns = momentum.columns)
        #print('index:{}'.format(momentum.index[i]))
        for j in range(0, len(tickers)) :
            stat[tickers[j]] = False
        for k in range(0, len(dualtickers)) :
            stat[dualtickers[k]] = False

        for j in range(0, len(tickers)) :
            #print('mom_rank[{}]'.format(tickers[j]), mom_rank[tickers[j]].iloc[i])
            if mom_rank[tickers[j]].iloc[i] <= rank:
                #print('{} ret'.format(tickers[j]),momentum[tickers[j]].iloc[i], '{} ret'.format(dualTickers[0]), momentum[dualTickers[0]].iloc[i])
                if momentum[tickers[j]].iloc[i] > momentum[dualtickers[0]].iloc[i]:
                    stat[tickers[j]] = True
                else:
                    stat[dualtickers[1]] = True
        #print('stat :', stat)
        selected = pd.concat([selected, stat])
        
    #print('df_stat shape: ', selected.shape)
    selected.index = momentum.index
    #selected = selected.loc[start_day:]       
    return selected