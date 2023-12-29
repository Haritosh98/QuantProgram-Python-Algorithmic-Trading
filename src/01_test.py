import yfinance as yf
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
sns.set(style="darkgrid")

Apple = yf.download("AAPL", start="2020-01-01", end="2021-01-01")

tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "SPY"]
stocks = yf.download(tickers, start="2009-01-01", end="2023-11-01") 

# Save the data to a csv file
stocks.to_csv("../data/stocks_01.csv")

# read the data from a csv file and re-format it
stocks = pd.read_csv("../data/stocks_01.csv")
stocks
stocks = pd.read_csv("../data/stocks_01.csv", index_col=[0], header=[0, 1],parse_dates=[0])
stocks

# understand multi-index and single-index dataframes:
# convert multi-index to single index
stocks.columns
stocks.columns = stocks.columns.to_flat_index()
stocks.columns

# convert from single index to multi-index
stocks.columns = pd.MultiIndex.from_tuples(stocks.columns)
stocks

# select a single column and all rows
stocks.loc[:,"Close"]

# select a row and all columns
stocks.loc["2020-01-02",:]

# create a copy of the dataframe for the close prices
close = stocks.loc[:,"Close"].copy()
close

# plotting this:
close.plot(figsize=(12,8), fontsize=12)
plt.legend(fontsize=12) 
plt.show()

# normalize the starting data to 100

# normalize the data for apple for it to start from 1 dollar, then mulpitply by 100:
close["AAPL"]/close["AAPL"][0]*100

# this is the first row for all the columns(columns are the stocks)
close/close.iloc[0]*100
norm_close = close/close.iloc[0]*100

# plotting this. This graph lets us compare the stocks:
norm_close.plot(figsize=(12,8), fontsize=12)
plt.legend(fontsize=12) 
plt.show()