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
        
        
        #...............................................
        #Use this path in Heroku
        
        access_token = open(os.path.join(os.getcwd(), "../access_token.txt"),'r').read().split()
        key_secret = open(os.path.join(os.getcwd(), "../api_key.txt"),'r').read().split()
        #...............................................
        background_color='#F5F5F5'
        
        kite = KiteConnect(api_key=key_secret[0])
        kite.set_access_token(access_token[1].strip())
        
        # Fetch position details
        orders = kite.orders()
        
        net_df=pd.DataFrame(orders) 
        
        net_df=net_df[['order_timestamp','transaction_type','tradingsymbol','product','quantity','average_price','status']]
        
        net_df = net_df.rename({'order_timestamp':'Time','transaction_type':'Type','tradingsymbol':'Instrument','product':'Product',"quantity":'Qty.','average_price':'Avg.','status':'Status'}, axis='columns')
        st.subheader("Executed orders ("+str(net_df.shape[0])+")")
        
        net_df.index = np.arange(1, len(net_df) + 1)
        fig=go.Figure(data=go.Table(
            columnwidth=[0.1,0.1,0.2,0.1,0.1,0.1,0.1],
            header=dict(values=list(["Row No.",'Time',"Type","Instrument",'Product',"Qty.","Avg.",'Status']),
            fill_color='#FD8E72',align='center'),cells=dict(values=([net_df.index[:],net_df["Time"][0:].tolist(),net_df["Type"][0:].tolist(),net_df["Instrument"][0:].tolist(),net_df["Product"][0:].tolist(),net_df["Qty."][0:].tolist(),net_df["Avg."][0:].tolist(),net_df["Status"][0:].tolist()]))))    
        fig.update_layout(width=1000,margin=dict(l=1,r=1,b=15,t=15),
                                paper_bgcolor = background_color
                                
                                )
        st.write(fig)  
        
       


