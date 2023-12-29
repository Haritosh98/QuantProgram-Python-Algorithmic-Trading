import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


Apple = yf.download("AAPL", start="2020-01-01", end="2021-01-01")

tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "FB"]
stocks = yf.download(tickers, start="2020-01-01", end="2021-01-01") 

stocks.info()