# Import necesary libraries
import yfinance as yf
import pandas as pd

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

def fetchOHLC_BSE(ticker,interval,duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df_bse,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data



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


# Download historical data for required stocks
tickers = ["BOROLTD","ADANIPORTS","AMBUJACEM"]
ohlcv_data = {}
cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")
#generate trading session
access_token = open(os.path.join(os.getcwd(),"access_token.txt"),'r').read().split()
key_secret = open(os.path.join(os.getcwd(),"api_key.txt"),'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token[1].strip())
#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
instrument_dump_bse = kite.instruments("BSE")
instrument_df_bse = pd.DataFrame(instrument_dump)
bse_tradingsymbols=instrument_df_bse.loc[:,'tradingsymbol'].tolist()

invalid_tokens=[]

ohlc=None
ohlc_dict={}
# Fetch holding details
holdings = kite.holdings()
for holding in holdings:
    try:
        print('Reading Share: ',holding['tradingsymbol'])
        ohlc = fetchOHLC(holding['tradingsymbol'],"day",365)#210 days
        ohlc_dict[holding['tradingsymbol']]=ohlc
    except Exception as e: 
            invalid_tokens.append(holding['tradingsymbol'])           
            print("Error:",e)
print("Unable to Fetch data For these Tokens:",invalid_tokens)    

for ticker in ohlc_dict:
    print("CAGR of {} = {}".format(ticker,CAGR(ohlc_dict[ticker])))
    