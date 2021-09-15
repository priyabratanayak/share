# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
import os
import numpy as np
import statsmodels.api as sm



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

def slope(ohlc_df,n):
    "function to calculate the slope of regression line for n consecutive points on a plot"
    df = ohlc_df.iloc[-1*n:,:]#to get last n candles
    y = ((df["open"] + df["close"])/2).values#to get mean of open and close price
    x = np.array(range(n))
    y_scaled = (y - y.min())/(y.max() - y.min())#y
    x_scaled = (x - x.min())/(x.max() - x.min())#x
    x_scaled = sm.add_constant(x_scaled)#c
    #y=mx+c
    #Implementing ordinary least squares (OLS)
    model = sm.OLS(y_scaled,x_scaled)
    results = model.fit()
    slope = np.rad2deg(np.arctan(results.params[-1]))#to get the ast value. arctan function will convert to radian
    return slope

def trend(ohlc_df,n):
    "function to assess the trend by analyzing each candle"
    df = ohlc_df.copy()
    df["up"] = np.where(df["low"]>=df["low"].shift(1),1,0)#It says the low value of candle is greater than the low value of previous candle
                                                          # then we say up value in the dataframe is 1 otherwise 0
    df["dn"] = np.where(df["high"]<=df["high"].shift(1),1,0)#It says the high value of candle is less than the high value of previous candle
    if df["close"][-1] > df["open"][-1]:#it says last candle to be green
        if df["up"][-1*n:].sum() >= 0.7*n:
            return "uptrend"
    elif df["open"][-1] > df["close"][-1]:#it says last candle to be red
        if df["dn"][-1*n:].sum() >= 0.7*n:
            return "downtrend"
    else:
        return None
cwd = os.chdir("C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
ohlc = fetchOHLC("YESBANK","5minute",30)
print(slope(ohlc,7))# n =7 means analysing 7 candles
print(slope(ohlc,2))#Analysing last 2 candles
print(trend(ohlc,7))