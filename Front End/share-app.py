import streamlit as st
import pandas as pd

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


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
    """Simple Login App"""

    

    menu = ["Login","SignUp","Home"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        
        cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")
        #generate trading session
        
        st.subheader(os.path.abspath("../access_token.txt"))
        access_token = open(os.path.abspath("../access_token.txt"),'r').read().split()
        key_secret = open(os.path.abspath("../api_key.txt"),'r').read().split()
        kite = KiteConnect(api_key=key_secret[0])
        kite.set_access_token(access_token[1].strip())
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
    elif choice == "Login":        
        st.subheader("Login Section")
        new_user = st.text_input("User")
        new_password = st.text_input("pw",type='password')

        if st.button("Sign In"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
			# if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")

                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")


    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()