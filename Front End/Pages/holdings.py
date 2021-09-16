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
import os.path
from kiteconnect import KiteConnect
def app():
        
        
        #display = Image.open('5-oceans-map-for.jpg')
        #display = np.array(display)
        #st.image(display, width = 400)
        print(os.path.isfile(os.path.join(os.getcwd(), "access_token.txt")))
        print(os.path.isfile(os.path.join(os.getcwd(), "../access_token.txt")))
        print(os.path.isfile(os.path.join(os.getcwd(), "../../access_token.txt")))
        print(os.path.isfile(os.path.join(os.getcwd(), "../../../access_token.txt")))
        #st.subheader(os.path.isfile(os.path.join(os.getcwd(), "access_token.txt")))
        if 'access_token' not in st.session_state:
            st.session_state['access_token']=None
        if 'key_secret' not in st.session_state:
            st.session_state['key_secret']=None
        #...............................................
        #Use this path in Heroku
        
        #access_token = open(os.path.join(os.getcwd(), "access_token.txt"),'r').read().split()
        #key_secret = open(os.path.join(os.getcwd(), "api_key.txt"),'r').read().split()
        #...............................................
        st.session_state.access_token = open(os.path.join(os.getcwd(), "../../access_token.txt"),'r').read().split()
        st.session_state.key_secret = open(os.path.join(os.getcwd(), "../../api_key.txt"),'r').read().split()
        
        background_color='#F5F5F5'
        kite = KiteConnect(api_key=st.session_state.key_secret[0])
        kite.set_access_token(st.session_state.access_token[1].strip())
        # Fetch holding details
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
        holdings_df_to_display.index = np.arange(1, len(holdings_df_to_display) + 1)
        st.subheader("Holdings ("+str(holdings_df_to_display.shape[0])+")")
        fig=go.Figure(data=go.Table(
            columnwidth=[0.1,0.2,0.1,0.1,0.1,0.1],
            header=dict(values=list(["Row No.","Instrument","Qty.","Avg. cost",'LTP','Cur. val','P&L','Net chg.','Day chg.']),
            fill_color='#FD8E72',align='center'),cells=dict(values=([holdings_df_to_display.index[:],holdings_df_to_display["Instrument"][0:].tolist(),holdings_df_to_display["Qty."][0:].tolist(),holdings_df_to_display["Avg. cost"][0:].tolist(),holdings_df_to_display["LTP"][0:].tolist(),holdings_df_to_display["Cur. val"][0:].tolist(),holdings_df_to_display["P&L"][0:].tolist(),holdings_df_to_display["Net chg."][0:].tolist(),holdings_df_to_display["Day chg."][0:].tolist()]))))    
        fig.update_layout(width=1000,margin=dict(l=1,r=1,b=15,t=15),
                                paper_bgcolor = background_color
                                
                                )
        st.write(fig)  