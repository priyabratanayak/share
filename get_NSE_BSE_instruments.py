# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import os
import connect
import pandas as pd
cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")
#generate trading session
access_token = open(os.path.join(os.getcwd(),"access_token.txt"),'r').read().split()
key_secret = open(os.path.join(os.getcwd(),"api_key.txt"),'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token[1].strip())

NSE_data=kite.instruments(exchange="NSE")
instrument_NSE=pd.DataFrame(NSE_data)
instrument_NSE.to_csv("instrument_NSE.csv",index=True,header=True) 

BSE_data=kite.instruments(exchange="BSE")
instrument_BSE=pd.DataFrame(BSE_data)
instrument_BSE.to_csv("instrument_BSE.csv",index=True,header=True) 
