# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 16:37:24 2021

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
conn = sqlite3.connect('data.db')
c = conn.cursor()
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
 

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
def app():
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")