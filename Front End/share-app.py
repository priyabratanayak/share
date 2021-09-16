import streamlit as st
import pandas as pd
from pathlib import Path
from kiteconnect import KiteConnect
import os
#import connect
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
from multipage import MultiPage
from Pages import sell,buy,login,signup,holdings,positions,orders
from PIL import  Image

st.set_page_config(layout="wide")
header=st.container()

timestr=time.strftime('%Y%m%d%H%M%S')
features=st.container()
df_result=None

background_color='#F5F5F5'
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
def text_downloader(raw_text,file,filename):
    csvfile=file.to_csv(index = False)
    b64=base64.b64encode(csvfile.encode()).decode()
    new_filename=filename+"_{}.csv".format(timestr)
    href=f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Download File</a>'
    st.markdown(href,unsafe_allow_html=True)





def main():
    """Simple Login App"""
    # Create an instance of the app 
    app = MultiPage()    
    # Title of the main page
    display = Image.open('5-oceans-map-for.jpg')
    display = np.array(display)
    
    app.add_page("Holdings", holdings.app)
    app.add_page("Buy", buy.app)
    
    app.add_page("Sell", sell.app)
    app.add_page("Positions", positions.app)
    app.add_page("Orders", orders.app)
    app.add_page("Login", login.app)
    app.add_page("Signup", signup.app)
    app.run()
    



if __name__ == '__main__':
    
	main()
