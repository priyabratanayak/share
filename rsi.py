# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
import os
import numpy as np
import connect
import copy

def instrumentLookup(instrument_df,symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1


def fetchOHLC(ticker,interval,duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data


def rsi(df, n):
    "function to calculate RSI"
    delta = df["close"].diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[n-1]] = np.mean( u[:n]) # first value is average of gains
    u = u.drop(u.index[:(n-1)])
    d[d.index[n-1]] = np.mean( d[:n]) # first value is average of losses
    d = d.drop(d.index[:(n-1)])
    rs = u.ewm(com=n,min_periods=n).mean()/d.ewm(com=n,min_periods=n).mean()
    return 100 - 100 / (1+rs)


cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")
#generate trading session
access_token = open(os.path.join(os.getcwd(),"access_token.txt"),'r').read().split()
key_secret = open(os.path.join(os.getcwd(),"api_key.txt"),'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token[1].strip())
#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
daily=pd.DataFrame()

ohlc=None
macd=None
ohlc = fetchOHLC("BOROLTD","60minute",90)#90 days


#To Calculate Hourly % Change
hourly=copy.deepcopy(ohlc)
print(hourly.columns)

hourly=hourly.sort_index()

hourly['% change'] = hourly["close"].pct_change()*100

hourly=hourly[['open','high','low','close','volume','% change']]
hourly['% change']=hourly['% change'].fillna(0)
rsi = rsi(ohlc,14)

hourly['RSI']=rsi
hourly=hourly.bfill(axis ='rows')
