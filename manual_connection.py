# -*- coding: utf-8 -*-
"""
Connecting to KiteConnect API

@author: Priyabrata Nayak
"""

from kiteconnect import KiteConnect
import pandas as pd

api_key = "42sivs5p2mhhkzmi"
api_secret = "u412e3x3lahos208ifblbsoig15k89hg"
kite = KiteConnect(api_key=api_key)
print(kite.login_url()) #use this url to manually login and authorize yourself

#generate trading session
request_token = "BKcdhFmxiG9pyUc3fvk951ENzKaE2VtU" #Extract request token from the redirect url obtained after you authorize yourself by loggin in
data = kite.generate_session(request_token, api_secret=api_secret)

#create kite trading object
kite.set_access_token(data["access_token"])


#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)
instrument_df.to_csv("NSE_Instruments.csv",index=False)