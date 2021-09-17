# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 16:36:57 2021

@author: 028906744
"""
import plotly.express as px
import plotly.graph_objects as go
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import base64
import time
from PIL import  Image
import os
from pathlib import Path
from kiteconnect import KiteConnect
def app():
        
        header=st.container()
        cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")
        #generate trading session
        #st.subheader(os.path.join(os.getcwd()))
        cwd = Path.cwd()
        
        goal_dir = cwd.parent.parent / "access_token.txt"
            
        #st.subheader(os.path.isfile(os.path.join(os.getcwd(), "access_token.txt")))
        
        
        #...............................................
        #Use this path in Heroku
        
        #access_token = open(os.path.join(os.getcwd(), "access_token.txt"),'r').read().split()
        #key_secret = open(os.path.join(os.getcwd(), "api_key.txt"),'r').read().split()
        #...............................................
        
        background_color='#F5F5F5'
        kite = KiteConnect(api_key=st.session_state.key_secret[0])
        kite.set_access_token(st.session_state.access_token[1].strip())
        st.subheader("Today's Profit ()")
        
        # Fetch position details
        positions = kite.positions()
        net_df=pd.DataFrame(positions['net']) 
        
        net_df=net_df[['product','tradingsymbol','quantity','average_price','last_price','pnl']]
        net_df['pnl']=net_df['pnl'].round(2)
        net_df['average_price']=net_df['average_price'].round(2)
        net_df = net_df.rename({'product':'Product','tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg.','last_price':'LTP','pnl':'P&L'}, axis='columns')
        st.subheader("Positions ("+str(net_df.shape[0])+")")
        
        st.table(net_df)
        dayshistory_df=pd.DataFrame(positions['day'])
        
        dayshistory_df=dayshistory_df[['product','tradingsymbol','quantity','average_price','last_price','pnl']]
        dayshistory_df['pnl']=dayshistory_df['pnl'].round(2)
        dayshistory_df['average_price']=dayshistory_df['average_price'].round(2)
        dayshistory_df = dayshistory_df.rename({'product':'Product','tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg.','last_price':'LTP','pnl':'P&L'}, axis='columns')
        st.subheader("Day's History")
        st.table(dayshistory_df)
        
        
        
        orders = kite.orders()
        
        order_df=pd.DataFrame(orders) 
        
        order_df=order_df[['order_timestamp','transaction_type','tradingsymbol','product','quantity','average_price','status']]
        
        order_df = order_df.rename({'order_timestamp':'Time','transaction_type':'Type','tradingsymbol':'Instrument','product':'Product',"quantity":'Qty.','average_price':'Avg.','status':'Status'}, axis='columns')
        order_df=order_df[order_df['Status']=="COMPLETE"]
        
        st.subheader("Orders")
        st.table(order_df)
        st.subheader("Holding")
        st.table(st.session_state.holding)
        
         
        
          

