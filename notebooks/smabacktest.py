import yfinance as yf
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sns.set(style="darkgrid")


class SMABacktester():
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end  
        self.results = None
        self.get_data()
        
    def get_data(self):
        df = yf.download(self.symbol, start = self.start, end = self.end)
        data = df['Close'].to_frame()
        data['returns'] = np.log(data['Close'].div(data['Close'].shift(1)))
        data['SMA_S'] = data['Close'].rolling(self.SMA_S).mean()
        data['SMA_L'] = data['Close'].rolling(self.SMA_L).mean()
        data.dropna(inplace = True)
        self.data2 = data
        return data
    
    def test_result(self):
        data = self.data2.copy().dropna()
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        data['strategy'] = data['returns'] * data['position'].shift(1)
        data.dropna(inplace = True)
        data['returns_buy_hold'] = data['returns'].cumsum().apply(np.exp)
        data['return_strategy'] = data['strategy'].cumsum().apply(np.exp)
        perf = data['return_strategy'].iloc[-1]
        outperf = perf - data['returns_buy_hold'].iloc[-1]
        self.results = data
        
        # absolute performance of the strategy (if 1 dollar is invested, what happens)
        ret = np.exp(data['strategy'].sum())
        std = data['strategy'].std() * np.sqrt(252)
    
        #return ret, std
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        if self.results is None:
            print("Run the test please")
        else:
            title = "{}| SMA_S = {} | SMA_L = {}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[['returns_buy_hold', 'return_strategy']].plot(title = title, figsize = (12,8))