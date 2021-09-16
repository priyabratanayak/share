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
    
        # Fetch position details
        positions = kite.positions()
        
        net_df=pd.DataFrame(positions['net']) 
        
        net_df=net_df[['product','tradingsymbol','quantity','average_price','last_price','pnl']]
        net_df['pnl']=net_df['pnl'].round(2)
        net_df['average_price']=net_df['average_price'].round(2)
        net_df = net_df.rename({'product':'Product','tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg.','last_price':'LTP','pnl':'P&L'}, axis='columns')
        st.subheader("Positions ("+str(net_df.shape[0])+")")
        
        net_df.index = np.arange(1, len(net_df) + 1)
        fig=go.Figure(data=go.Table(
            columnwidth=[0.1,0.1,0.2,0.1,0.1,0.1,0.1],
            header=dict(values=list(["Row No.","Product","Instrument","Qty.","Avg.",'LTP','P&L']),
            fill_color='#FD8E72',align='center'),cells=dict(values=([net_df.index[:],net_df["Product"][0:].tolist(),net_df["Instrument"][0:].tolist(),net_df["Qty."][0:].tolist(),net_df["Avg."][0:].tolist(),net_df["LTP"][0:].tolist(),net_df["P&L"][0:].tolist()]))))    
        fig.update_layout(width=1000,margin=dict(l=1,r=1,b=15,t=15),
                                paper_bgcolor = background_color
                                
                                )
        st.write(fig)  
        
        dayshistory_df=pd.DataFrame(positions['day'])
        
        dayshistory_df=dayshistory_df[['product','tradingsymbol','quantity','average_price','last_price','pnl']]
        dayshistory_df['pnl']=dayshistory_df['pnl'].round(2)
        dayshistory_df['average_price']=dayshistory_df['average_price'].round(2)
        dayshistory_df = dayshistory_df.rename({'product':'Product','tradingsymbol':'Instrument',"quantity":'Qty.','average_price':'Avg.','last_price':'LTP','pnl':'P&L'}, axis='columns')
        st.subheader("Day's History ("+str(dayshistory_df.shape[0])+")")
        
        dayshistory_df.index = np.arange(1, len(dayshistory_df) + 1)
        fig=go.Figure(data=go.Table(
            columnwidth=[0.1,0.1,0.2,0.1,0.1,0.1,0.1],
            header=dict(values=list(["Row No.","Product","Instrument","Qty.","Avg.",'LTP','P&L']),
            fill_color='#FD8E72',align='center'),cells=dict(values=([net_df.index[:],net_df["Product"][0:].tolist(),net_df["Instrument"][0:].tolist(),net_df["Qty."][0:].tolist(),net_df["Avg."][0:].tolist(),net_df["LTP"][0:].tolist(),net_df["P&L"][0:].tolist()]))))    
        fig.update_layout(width=1000,margin=dict(l=1,r=1,b=15,t=15),
                                paper_bgcolor = background_color
                                
                                )
        st.write(fig)  

