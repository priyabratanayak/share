# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 19:24:19 2021

@author: 028906744
"""
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
from lxml import html
import yahoo_fin.stock_info as yf


tickers = ["MSFT"]
balance_sheet=yf.get_balance_sheet(tickers[0],yearly=True)
balance_sheet=balance_sheet/1000
print(balance_sheet.index.tolist())