# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import os
import connect

cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")
#generate trading session
access_token = open(os.path.join(os.getcwd(),"access_token.txt"),'r').read().split()
key_secret = open(os.path.join(os.getcwd(),"api_key.txt"),'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token[1].strip())



# Fetch quote details
quote = kite.quote("NSE:INFY")

# Fetch last trading price of an instrument
ltp = kite.ltp("NSE:WIPRO")

# Fetch all the orders that you placed in a given trading session
orders = kite.orders()

# Fetch position details
positions = kite.positions()

# Fetch holding details
holdings = kite.holdings()
