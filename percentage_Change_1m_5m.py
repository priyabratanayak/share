# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
import os
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


def MACD(DF,a,b,c):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26; 
                      c(signal line ma window) =9"""
    df = DF.copy()
    df["MA_Fast"]=df["close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    df.dropna(inplace=True)
    return df

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
ohlc_5min = fetchOHLC("BOROLTD","5minute",1)#1 day
ohlc_15min = fetchOHLC("BOROLTD","15minute",1)#1 day

ohlc_5min['% change'] = ohlc_5min["close"].pct_change()*100
ohlc_5min=ohlc_5min[['open','high','low','close','volume','% change']]
ohlc_5min['% change']=ohlc_5min['% change'].fillna(0)


ohlc_15min['% change'] = ohlc_15min["close"].pct_change()*100

ohlc_15min=ohlc_15min[['open','high','low','close','volume','% change']]
ohlc_15min['% change']=ohlc_15min['% change'].fillna(0)