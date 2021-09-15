
# Import necesary libraries
import yfinance as yf
import numpy as np

# Download historical data for required stocks
tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='7mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)#for daily data
    #df["daily_ret"].std() gives daily volatility
    #df["daily_ret"].std() * np.sqrt(252) gives anualised volatility
    #Refer 45. How to Measure Volatility in the document
    return vol

for ticker in ohlcv_data:
    print("vol for {} = {}".format(ticker,volatility(ohlcv_data[ticker])))