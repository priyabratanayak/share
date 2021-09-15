
# Import necesary libraries
import yfinance as yf
import pandas as pd
import numpy as np

# Download historical data for required stocks
tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='7mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp
    
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["return"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR
    
def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    vol = df["return"].std() * np.sqrt(252)
    return vol

def sharpe(DF, rf):
    "function to calculate Sharpe Ratio of a trading strategy"
    df = DF.copy()
    return (CAGR(df) - rf)/volatility(df)#volatility(df) gives the standard deviation

def sortino(DF, rf):
    "function to calculate Sortino Ratio of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    neg_return = np.where(df["return"]>0,0,df["return"])#Sortio takes into account only negative return.
    #So we must remove the positive return
    neg_vol = pd.Series(neg_return[neg_return!=0]).std() * np.sqrt(252)#by defauly std ignores nan value
    return (CAGR(df) - rf)/neg_vol

for ticker in ohlcv_data:
    print("Sharpe of {} = {}".format(ticker,sharpe(ohlcv_data[ticker],0.03)))#Rf varies from jurisdiction to jurisdiction for US it  is 0.03 
    #check 47. Sharpe Ratio and Sortino Ratio section
    print("Sortino of {} = {}".format(ticker,sortino(ohlcv_data[ticker],0.03)))
    
    
    
    