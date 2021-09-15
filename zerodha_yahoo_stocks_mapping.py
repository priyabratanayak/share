# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:39:13 2021

@author: 028906744
"""
# Import necesary libraries
import yfinance as yf
import pandas as pd
import numpy as np
# Download historical data for required stocks
zerodha_stocks=pd.read_csv('NSE_Instruments_zerodha_yahoo.csv')
tickers = zerodha_stocks['tradingsymbol Zerodha'].tolist()
yahoo_tickers = zerodha_stocks['tradingsymbol Yahoo'].tolist()
failed_count=0
test=yf.download("INDIA VIX.NS",period='1d',interval='1d')
for row in range(1,len(tickers)):
    if str(yahoo_tickers[row])=='nan':
        if tickers[row][-3:].lower()=='-be':
             temp = yf.download(tickers[row][:-3].replace(' ','')+".NS",period='1d',interval='1d')
        else:
            temp = yf.download(tickers[row].replace(' ','')+".NS",period='1d',interval='1d')
        
        if temp.shape[0]>0:
            
            yahoo_tickers[row]=tickers[row]+".NS"
        else:
            failed_count+=1
            print("Not Found:",tickers[row])
print("failed_count:",failed_count)
zerodha_stocks['tradingsymbol Yahoo']=yahoo_tickers
zerodha_stocks.to_csv('NSE_Instruments_zerodha_yahoo.csv',index=False)