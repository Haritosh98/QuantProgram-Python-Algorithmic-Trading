import yfinance as yf
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
sns.set(style="darkgrid")

Apple = yf.download("AAPL", start="2020-01-01", end="2021-01-01")

tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "SPY", "IBM", "KO", "DIS", "INTC"]
stocks = yf.download(tickers, start="2006-01-01", end="2023-11-01") 

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

# focusing on apple
aapl = close["AAPL"].copy().to_frame()
aapl

# calculate the increase or decease from every day to the next
# using the shift function
aapl.shift(periods=1) # this shifts the data one day forward
aapl['lag1'] = aapl.shift(periods=1) # this adds a new column called lag 1 (which has the price from the day before). Now we can calculate the difference
aapl['diff'] = aapl['AAPL'] - aapl['lag1'] # this calculates the difference between the two columns
# now we can calculate the % change
aapl['% change'] = aapl['diff']/aapl['lag1'] * 100 # this calculates the % change
aapl

# we could have done this using the diff method:
# instead of this: aapl['lag1'] = aapl.shift(periods=1) \\ aapl['diff'] = aapl['AAPL'] - aapl['lag1']
aapl['diff_'] = aapl['AAPL'].diff(periods=1) # this calculates the difference between the two columns

# instead of this: aapl['% change'] = aapl['diff']/aapl['lag1'] * 100:
aapl['% change_'] = aapl['AAPL'].pct_change(periods=1) * 100 # this calculates the % change


# delete the columns we don't need
aapl.drop(columns=['lag1','diff','% change', 'diff_'], inplace=True)

# rename column:
aapl.rename(columns={'% change':'Daily % change'}, inplace=True)
aapl

aapl['AAPL'].resample('BM').last() # this gives us the last business day of every month
# we can calculate the monthly % change:
aapl['AAPL'].resample('BM').last().pct_change(periods=1) * 100


# now we can calculate the return (%change) on a daily basis:
aapl = close["AAPL"].copy().to_frame()
daily_returns = aapl.pct_change(periods=1).dropna() * 100
daily_returns.plot(kind = 'hist', figsize=(12,8), fontsize=12, bins=100)
plt.show()    
# the graph suggests that the daily returns are normally distributed
# we can also see that the mean is positive, which means that on average the stock goes up
# However, we can't base exit strategies on this, because the stock can go up 5% and then go down 10% the next day.

mean_returns_daily = daily_returns.mean()
mean_returns_daily

variance_daily = daily_returns.var()
variance_daily

# the risk metric is the standard deviation
std_daily = daily_returns.std()
std_daily

annual_mean_returns = mean_returns_daily * 252 # 252 is the number of trading days in a year
annual_mean_returns # this is the annual mean return for apple stock (in %) 

annual_variance = variance_daily * 252
annual_variance

annual_std = np.sqrt(annual_variance)
annual_std # this is the annual standard deviation for apple stock (in %)
# this is the same as this: std_daily * np.sqrt(252)


#_______________________________________________________________________________________________________________________

# now % change for all the stocks:
close # this is the close for all the stocks in the list (tickers)
all_stock_daily_returns = close.pct_change(periods=1).dropna() * 100 # this calculates the % change for all the stocks in the list (tickers) on a daily basis and drops the first row (which is NaN) and multiplies by 100 to get the % change 
all_stock_daily_returns.describe() # this gives us the mean, std, min, max, etc. for all the stocks in the list (tickers) on a daily basis  
# transpose this:
all_stock_daily_returns.describe().T # this gives us the mean, std, min, max, etc. for all the stocks in the list (tickers) on a daily basis (transposed)

summary_stocks_daily_returns = all_stock_daily_returns.describe().T.loc[:, ['mean', 'std']] # this gives us the mean and std for all the stocks in the list (tickers) on a daily basis (transposed)    
summary_stocks_daily_returns.rename(columns={'mean':'daily_mean', 'std':'daily_std'}, inplace=True) # rename the columns

# now for the annual returns
summary_stocks_daily_returns['annual_mean'] = summary_stocks_daily_returns['mean'] * 252 # this gives us the annual mean returns for all the stocks in the list (tickers) on a daily basis (transposed)
summary_stocks_daily_returns['annual_std'] = summary_stocks_daily_returns['std'] * np.sqrt(252) # this gives us the annual std for all the stocks in the list (tickers) on a daily basis (transposed)

summary_stocks_daily_returns.plot(kind = 'scatter', x = 'annual_std', y = 'annual_mean', figsize=(12,8), fontsize=12)
for i in summary_stocks_daily_returns.index:
    plt.annotate(i, xy=(summary_stocks_daily_returns.loc[i,'annual_std'] + 0.002, summary_stocks_daily_returns.loc[i,'annual_mean'] + 0.002), size=15)
plt.xlabel('Annual Risk (Standard Deviation %)', fontsize=15)
plt.ylabel('Annual Return (Mean %)', fontsize=15)
plt.title('Risk vs. Return', fontsize=15)
# returns on apple is high but so is the risk
# also choosing between microsoft and amazon is a tradeoff between risk and return
# choosing between disney and microsoft - choose microsoft because it has higher returns at almost the same risk
# choosing between goog and intc - choose goog because it has higher returns at almost the same risk


# this is basically what warren buffet does - he chooses stocks that have high returns and low risk