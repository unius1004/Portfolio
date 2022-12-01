import bt
import pandas as pd

def Buy_n_Hold_BT(data, name="Buy and Hold"):
    s = bt.Strategy(name, [bt.algos.RunOnce(),
                           bt.algos.PrintInfo('{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'),
                           bt.algos.PrintDate(),                           
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.PrintTempData(),
                           bt.algos.Rebalance()])
    return bt.Backtest(s, data, initial_capital=100000000.0)


def Equal_Weight_BT(data, name="Equally Weighted"):
    s = bt.Strategy(name, [bt.algos.RunMonthly(run_on_first_date=False, run_on_end_of_period=True, run_on_last_date=False),
                           #bt.algos.PrintInfo('{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'),
                           #bt.algos.PrintDate(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           #bt.algos.PrintTempData(),
                           bt.algos.Rebalance()])
    return bt.Backtest(s, data, initial_capital=100000000.0)

def Target_Weight_BT(data, weights, name="Target Weight"):
    s = bt.Strategy(name, [bt.algos.RunMonthly(run_on_first_date=False, run_on_end_of_period=True, run_on_last_date=False),
                           #bt.algos.RunAfterDate(start),
                           #bt.algos.PrintInfo('{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'),
                           #bt.algos.PrintDate(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighTarget(weights),
                           #bt.algos.PrintTempData(),
                           bt.algos.Rebalance()])
    return bt.Backtest(s, data, initial_capital=100000000.0)


def Relative_Momentum_BT(data, n, m, name="Relative Momentum",
                         run_period=bt.algos.RunMonthly(run_on_first_date=False, run_on_end_of_period=True, run_on_last_date=False), lag=0):
    s = bt.Strategy(name, [run_period,
                           #bt.algos.RunAfterDate(start),
                           #bt.algos.PrintInfo('{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'),
                           #bt.algos.PrintDate(),
                           bt.algos.SelectAll(),
                           bt.algos.SelectMomentum(n=n,
                                                   lookback=pd.DateOffset(months=m),
                                                   lag=pd.DateOffset(days=lag)),
                           bt.algos.WeighEqually(),
                           #bt.algos.PrintTempData(),
                           bt.algos.Rebalance()])
    return bt.Backtest(s, data, initial_capital=100000000.0)
