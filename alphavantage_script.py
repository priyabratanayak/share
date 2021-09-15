

# importing libraries
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
import os
token_path = "AlphaVantage_key.txt"
key_path = os.path.join(os.getcwd(),token_path)

# extracting data for a single ticker
ts = TimeSeries(key=open(key_path,'r').read(), output_format='pandas')#output_format='pandas' converts json to pandas
data = ts.get_daily(symbol='EURUSD', outputsize='full')[0]#as get_daily function returns a tuple.
#first value contains the data and the second value contains metadata.we use [0] to get the data
data.columns = ["open","high","low","close","volume"]#for forex data like EURSD volume column returns 0
data = data.iloc[::-1]#data cmes in a reverse format that is descending order. we need to chane it to ascending order


# extracting stock data (historical close price) for multiple stocks
all_tickers = ["AAPL","MSFT","CSCO","AMZN","GOOG",
               "FB","BA","MMM","XOM","NKE","INTC"]
close_prices = pd.DataFrame()
api_call_count = 1
ts = TimeSeries(key=open(key_path,'r').read(), output_format='pandas')
start_time = time.time()
for ticker in all_tickers:
    data = ts.get_intraday(symbol=ticker,interval='1min', outputsize='compact')[0]
    api_call_count+=1
    data.columns = ["open","high","low","close","volume"]
    data = data.iloc[::-1]
    close_prices[ticker] = data["close"]
    if api_call_count==5:#as for free account 5 api calls per minute
        api_call_count = 1
        time.sleep(60 - ((time.time() - start_time) % 60.0))


# extracting ohlcv data for multiple stocks
all_tickers = ["AAPL","MSFT","CSCO","AMZN","GOOG",
               "FB","BA","MMM","XOM","NKE","INTC"]
ohlv_dict = {}
api_call_count = 1
ts = TimeSeries(key=open(key_path,'r').read(), output_format='pandas')
start_time = time.time()
for ticker in all_tickers:
    data = ts.get_intraday(symbol=ticker,interval='1min', outputsize='compact')[0]
    api_call_count+=1
    data.columns = ["open","high","low","close","volume"]
    data = data.iloc[::-1]
    ohlv_dict[ticker] = data
    if api_call_count==5:
        api_call_count = 1
        time.sleep(60 - ((time.time() - start_time) % 60.0))