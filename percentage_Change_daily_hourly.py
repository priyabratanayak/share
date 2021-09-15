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
ohlc = fetchOHLC("BOROLTD","60minute",90)#90 days
ohlc=ohlc.reset_index()
#Convert hourly ata to daily data
#ohlc2=ohlc.set_index('Date', inplace=True)
ohlc_daily=ohlc.groupby(ohlc.date.dt.day)
counter_final=ohlc_daily.size().size
counter=1
for name, group in ohlc_daily:
    daily=daily.append(group.iloc[-1,:])
    

daily=daily.reset_index()
daily.drop('index', axis=1, inplace=True)
daily.set_index("date",inplace=True,drop=True)
daily=daily.sort_index()

daily['% change'] = daily["close"].pct_change()*100
daily=daily[['open','high','low','close','volume','% change']]
daily['% change']=daily['% change'].fillna(0)



# daily data can be calculated like below..................
#ohlc_dailydf = fetchOHLC("BOROLTD","day",90)#90 days
#ohlc_dailydf=ohlc_dailydf.sort_index()
#ohlc_dailydf['% change'] = ohlc_dailydf["close"].pct_change()*100
#ohlc_dailydf=daily[['open','high','low','close','volume','% change']]
#ohlc_dailydf['% change']=ohlc_dailydf['% change'].fillna(0)
#......................................


#To Calculate Hourly % Change
hourly=copy.deepcopy(ohlc)
hourly.set_index("date",inplace=True,drop=True)
hourly=hourly.sort_index()

hourly['% change'] = hourly["close"].pct_change()*100

hourly=hourly[['open','high','low','close','volume','% change']]
hourly['% change']=hourly['% change'].fillna(0)