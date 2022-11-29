import bt

def buy_n_hold(data, name='buy and keep'):
  s = bt.Strategy(name, [bt.algos.RunOnce(),
                         bt.algos.SelectAll(),
                         bt.algos.WeighEqually(),
                         bt.algos.Rebalance()])
  return bt.Backtest(s, data, initial_capital=100000000.0)
