# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
import os



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

def doji(ohlc_df):    
    """returns dataframe with doji candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df["close"] - df["open"]).median()#we can also use mean. But the problem with mean
    #is that if the data is skewed then it will affect the candle size 
    df["doji"] = abs(df["close"] - df["open"]) <=  (0.05 * avg_candle_size)# If the candle size is less than
    # 5% of the average candle size then we consider it as a doji candle
    return df

cwd = os.chdir("C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

ohlc = fetchOHLC("PCJEWELLER","5minute",5)
doji_df = doji(ohlc)