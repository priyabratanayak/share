# Import necesary libraries
import yfinance as yf
import pandas as pd
# Download historical data for required stocks
tickers = ["BOROLTD.BO","BOROLTD.NS","ADANIPORTS.NS","AMBUJACEM.NS"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='7mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    if 'Adj Close' in DF.keys():
        df["return"] = DF["Adj Close"].pct_change()
    if 'close' in DF.keys():
        df["return"] = DF["close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()#cumulative product cumprod
    n = len(df)/252 #252 is the total number of trading days in a year. This is for daily data
    #For hourly data we need to divide further with the number of hour constitute a trdaing day.If it is 6 hrs then
    #n = len(df)/252/6
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    if pd.isna(CAGR):
        CAGR='Insufficient Data'
    
    return CAGR

for ticker in ohlcv_data:
    print("CAGR of {} = {}".format(ticker,CAGR(ohlcv_data[ticker])))
    