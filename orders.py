# -*- coding: utf-8 -*-

from kiteconnect import KiteConnect
import logging
import os



def placeMarketOrder(symbol,buy_sell,quantity):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NSE,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_MARKET,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR)
#kite.EXCHANGE_BSE
#kite.ORDER_TYPE_LIMIT
    #Refer class variables section in https://kite.trade/docs/pykiteconnect/v3/
def placeLimitOrder(symbol,buy_sell,quantity,buyprice):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NSE,
                    transaction_type=t_type,
                    price=buyprice,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    product=kite.PRODUCT_CNC,
                    variety=kite.VARIETY_REGULAR)
def placeBracketOrder(symbol,buy_sell,quantity,atr,price):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=kite.EXCHANGE_NSE,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    price=price, #BO has to be a limit order, set a low price threshold
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_BO,
                    squareoff=int(6*atr), 
                    stoploss=int(3*atr), 
                    trailing_stoploss=2)
#if atr is suppose 10 then square off price will be 6x10=60 rs + the price in which you bought the share
cwd = os.chdir("C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
placeLimitOrder("PRAKASH","buy",1,70)