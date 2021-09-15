# -*- coding: utf-8 -*-
from kiteconnect import KiteConnect
from selenium import webdriver
import time
import os
import datetime
import os.path
import pytz

cwd=os.path.join(os.getcwd(),"Share Trading Zerodha")

def autologin():
    token_path = "api_key.txt"
    key_secret = open(os.path.join(os.getcwd(),token_path),'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service('./chromedriver')#change it to /usr/bin/chromedriverwhile uploading to linux
    #service = webdriver.chrome.service.Service('/usr/bin/chromedriver')
    
    service.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options = options.to_capabilities()
    driver = webdriver.Remote(service.service_url, options)
    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
    username.send_keys(key_secret[2])
    password.send_keys(key_secret[3])
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
    pin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
    pin.send_keys(key_secret[4])
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
    time.sleep(10)
    request_token=driver.current_url.split('request_token=')[1].split('&action')[0]
    with open('request_token.txt', 'w') as the_file:
       
        the_file.write(request_token)
    driver.quit()


if not os.path.isfile(os.path.join(os.getcwd(),'access_token.txt')) :
    
    autologin()
    #generating and storing access token - valid till 6 am the next day
    request_token = open(os.path.join(os.getcwd(),"request_token.txt"),'r').read()
    key_secret = open(os.path.join(os.getcwd(),"api_key.txt"),'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    data = kite.generate_session(request_token, api_secret=key_secret[1])
    
    with open(os.path.join(os.getcwd(),'access_token.txt'), 'w') as file:
            file.write(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d-%H:%M:%S')+"\n")
            
            file.write(data["access_token"])
else:
    access_token_date = open(os.path.join(os.getcwd(),"access_token.txt"),'r').read().split()
    datetime_object = datetime.datetime.strptime(access_token_date[0], '%Y-%m-%d-%H:%M:%S')
    datetime_object_reference = datetime.datetime.strptime(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d-')+'06:00:00', '%Y-%m-%d-%H:%M:%S')
    
    datetime_object_reference1 = datetime.datetime.strptime('2021-09-07-06:01:41', '%Y-%m-%d-%H:%M:%S')
    datetime_object_reference2 = datetime.datetime.strptime('2021-09-07-06:00:00', '%Y-%m-%d-%H:%M:%S')
   
    if int((datetime_object_reference-datetime_object).days)>=0:
        autologin()
        #generating and storing access token - valid till 6 am the next day
        request_token = open(os.path.join(os.getcwd(),"request_token.txt"),'r').read()
        key_secret = open(os.path.join(os.getcwd(),"api_key.txt"),'r').read().split()
        kite = KiteConnect(api_key=key_secret[0])
        data = kite.generate_session(request_token, api_secret=key_secret[1])
    
        with open(os.path.join(os.getcwd(),'access_token.txt'), 'w') as file:
                file.write(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d-%H:%M:%S')+"\n")
                
                file.write(data["access_token"])
    '''
    else:
        
        with open(os.path.join(os.getcwd(),'access_token.txt'), 'r') as file:
            lines=file.readlines()
            print(lines[0].strip())
            print(lines[1].strip())
    '''
        


