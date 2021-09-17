# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 16:36:57 2021

@author: 028906744
"""

# Security
#passlib,hashlib,bcrypt,scrypt

import streamlit as st
import pandas as pd

from kiteconnect import KiteConnect
def app():
        
       
        #generate trading session
        #st.subheader(os.path.join(os.getcwd()))
             
        #st.subheader(os.path.isfile(os.path.join(os.getcwd(), "access_token.txt")))
        
        
        #...............................................
        #Use this path in Heroku
        
        #access_token = open(os.path.join(os.getcwd(), "access_token.txt"),'r').read().split()
        #key_secret = open(os.path.join(os.getcwd(), "api_key.txt"),'r').read().split()
        #...............................................
        #access_token = open("C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha\\Front End\\access_token.txt",'r').read().split()
        #key_secret = open("C:\\Users\\PRIYABRATANAYAK\\Documents\\Python Tutorial\\Share Trading Zerodha\\Front End\\api_key.txt",'r').read().split()
        
        # kite = KiteConnect(api_key=key_secret[0])
        #kite.set_access_token(access_token[1].strip())
        kite = KiteConnect(api_key=st.session_state.key_secret[0])
        kite.set_access_token(st.session_state.access_token[1].strip())
        
        # Fetch position details
        positions = kite.positions()
        net_df=pd.DataFrame(positions['net']) 
        
        net_df=net_df[['product','tradingsymbol','quantity','average_price','last_price','pnl']]
        net_df['pnl']=net_df['pnl'].round(2)
        net_df['average_price']=net_df['average_price'].round(2)
        net_df = net_df.rename({'product':'Product','tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg.','last_price':'LTP','pnl':'P&L'}, axis='columns')
        dayshistory_df=pd.DataFrame(positions['day'])
        
        dayshistory_df=dayshistory_df[['product','tradingsymbol','quantity','average_price','last_price','pnl']]
        dayshistory_df['pnl']=dayshistory_df['pnl'].round(2)
        dayshistory_df['average_price']=dayshistory_df['average_price'].round(2)
        dayshistory_df = dayshistory_df.rename({'product':'Product','tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg.','last_price':'LTP','pnl':'P&L'}, axis='columns')
        
        
        
        
        orders = kite.orders()
        
        order_df=pd.DataFrame(orders) 
        
        order_df=order_df[['order_timestamp','transaction_type','tradingsymbol','product','quantity','average_price','status']]
        
        order_df = order_df.rename({'order_timestamp':'Time','transaction_type':'Type','tradingsymbol':'Instrument','product':'Product',"quantity":'Qty.','average_price':'Avg.','status':'Status'}, axis='columns')
        order_df=order_df[order_df['Status']=="COMPLETE"]
        order_df_sell=order_df[order_df['Type']=="SELL"]
        order_df_buy=order_df[order_df['Type']=="BUY"]
        
        
        holdings = kite.holdings()
        holdings_df=pd.DataFrame(holdings)        
        holdings_df_to_display=holdings_df[['tradingsymbol','quantity','average_price','last_price','day_change','day_change_percentage','pnl']]
        holdings_df_to_display['Cur. val']=holdings_df_to_display['quantity']*holdings_df_to_display['last_price']
        holdings_df_to_display = holdings_df_to_display.rename({'tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg. cost','last_price':'LTP','Cur. val':'Cur. val','pnl':'P&L','day_change':'Net chg.','day_change_percentage':'Day chg.'}, axis='columns')
        holdings_df_to_display=holdings_df_to_display[['Instrument','Qty.','Avg. cost','LTP','Cur. val','P&L','Net chg.','Day chg.']]
        holdings_df_to_display['Net chg.']=holdings_df_to_display['Net chg.'].round(2)
        holdings_df_to_display['Cur. val']=holdings_df_to_display['Cur. val'].round(2)
        holdings_df_to_display['P&L']=holdings_df_to_display['P&L'].round(2)
        holdings_df_to_display['Avg. cost']=holdings_df_to_display['Avg. cost'].round(2)
        holdings_df_to_display['Net chg.']=holdings_df_to_display['Net chg.'].apply(str)
        holdings_df_to_display['Net chg.']=holdings_df_to_display['Net chg.']+"%"
        holdings_df_to_display['Day chg.']=holdings_df_to_display['Day chg.'].round(2)
        holdings_df_to_display['Day chg.']=holdings_df_to_display['Day chg.'].apply(str)
        holdings_df_to_display['Day chg.']=holdings_df_to_display['Day chg.']+"%"
        order_df_sell['STT']=0
        order_df_sell['Brokerage']=0
        
        order_df_sell['Profit/Loss']=0
        
        order_df_sell[['STT','Profit/Loss']]=order_df_sell.apply(calculation,dataframe_display=holdings_df_to_display,dataframe=order_df_buy,axis=1,result_type ='expand')
        
        
        order_df_sell.drop('Time', axis=1, inplace=True)
        order_df_sell.drop('Product', axis=1, inplace=True)
        order_df_sell['15% Tax']=round(0.15*order_df_sell['Profit/Loss'])
        order_df_sell['Net Profit/Loss']=(round(order_df_sell['Profit/Loss']-order_df_sell['15% Tax']))
        order_df_sell['Net Profit/Loss / 2']=(round(order_df_sell['Net Profit/Loss']/2))
        
        st.subheader("Today's Profit : Rs."+str(round(order_df_sell['Net Profit/Loss / 2'].sum(axis = 0, skipna = True))))
        order_df_sell['Net Profit/Loss / 2']=order_df_sell['Net Profit/Loss / 2'].astype(int)
        order_df_sell['Net Profit/Loss']=order_df_sell['Net Profit/Loss'].astype(int)
        order_df_sell['15% Tax']=order_df_sell['15% Tax'].astype(int)
        st.table(order_df_sell)
        
        st.subheader("Positions ("+str(net_df.shape[0])+")")
        
        st.table(net_df)
        
        st.subheader("Day's History")
        st.table(dayshistory_df)       
        
        st.subheader("Orders")
        st.table(order_df)
        st.subheader("Holding")
        st.table(st.session_state.holding)
        
def calculation(x,dataframe_display,dataframe):
    order_df_buy=dataframe
    
    holdings_df_to_display=dataframe_display
    temp_buy=order_df_buy[order_df_buy['Instrument'].str.contains(pat=x['Instrument'])]
    temp_hold=holdings_df_to_display[holdings_df_to_display['Instrument'].str.contains(pat=x['Instrument'])]
    
    if temp_hold.shape[0]>0:
        print(x['Instrument'])
        buyvalue=float(temp_hold['Avg. cost'].to_string(index=False))
        
        sellvalue=float(x['Avg.'])
        print(buyvalue,sellvalue,x['Qty.'])
        buytotal=int(x['Qty.'])*buyvalue
        selltotal=int(x['Qty.'])*sellvalue
        print(buytotal,selltotal)
        difference=selltotal-buytotal
        stt=(0.001*selltotal)+(0.001*buytotal)
        
        difference=difference-round(stt)
        
        
        
        print(round(stt),round(difference))
        return round(stt),round(difference)
    #print(order_df_sell)        
    return 0,0
    
          

