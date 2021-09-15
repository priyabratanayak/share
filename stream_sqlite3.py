# -*- coding: utf-8 -*-


from kiteconnect import KiteTicker, KiteConnect
import datetime
import sys
import pandas as pd
import os
import sqlite3



def create_tables(tokens):
    #tokens are numerical values. For token 5678 it will be TOKEN5678
    c=db.cursor()
    for i in tokens:
        c.execute("CREATE TABLE IF NOT EXISTS TOKEN{} (ts datetime primary key,price real(15,5), volume integer)".format(i))
        #ts is the column name with data type datetime
    try:
        db.commit()
    except:
        db.rollback()

def insert_ticks(ticks):
    c=db.cursor()
    for tick in ticks:
        try:
            tok = "TOKEN"+str(tick['instrument_token'])
            vals = [tick['timestamp'],tick['last_price'], tick['last_quantity']]
            query = "INSERT INTO {}(ts,price,volume) VALUES (?,?,?)".format(tok)
            c.execute(query,vals)
        except:
            pass
    try:
        db.commit()
    except:
        db.rollback()    


#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

def tokenLookup(instrument_df,symbol_list):
    """Looks up instrument token for a given script from instrument dump"""
    token_list = []
    for symbol in symbol_list:
        token_list.append(int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]))
    return token_list




cwd = os.chdir("C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

db = sqlite3.connect('C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha/7_streaming_data/ticks.db')

#####################update ticker list######################################
tickers = ["ZEEL","WIPRO","VEDL","ULTRACEMCO","UPL","TITAN","TECHM","TATASTEEL",
           "TATAMOTORS","TCS","SUNPHARMA","SBIN","SHREECEM","RELIANCE","POWERGRID",
           "ONGC","NESTLEIND","NTPC","MARUTI","M&M","LT","KOTAKBANK","JSWSTEEL","INFY",
           "INDUSINDBK","IOC","ITC","ICICIBANK","HDFC","HINDUNILVR","HINDALCO",
           "HEROMOTOCO","HDFCBANK","HCLTECH","GRASIM","GAIL","EICHERMOT","DRREDDY",
           "COALINDIA","CIPLA","BRITANNIA","BHARTIARTL","BPCL","BAJAJFINSV",
           "BAJFINANCE","BAJAJ-AUTO","AXISBANK","ASIANPAINT","ADANIPORTS"]
#############################################################################

#create KiteTicker object
kws = KiteTicker(key_secret[0],kite.access_token)
tokens = tokenLookup(instrument_df,tickers)

#create table
create_tables(tokens)

#callback
def on_ticks(ws,ticks):
    insert_tick=insert_ticks(ticks)
    print(ticks)
#callback
def on_connect(ws,response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL,tokens)
    

while True:
    now = datetime.datetime.now()
    if (now.hour >= 9 and now.minute >= 15 ):
        kws.on_ticks=on_ticks
        kws.on_connect=on_connect
        kws.connect()
    if (now.hour >= 15 and now.minute >= 30):
        sys.exit()

db.close()

"""
c.execute('SELECT name from sqlite_master where type= "table"')
c.fetchall()

c.execute('''PRAGMA table_info(TOKEN975873)''')
c.fetchall()

for m in c.execute('''SELECT * FROM TOKEN975873'''):
    print(m)
"""