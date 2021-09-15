# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 00:45:43 2021

@author: 028906744
"""
import yahoo_fin.stock_info as si
'''

quote=si.get_quote_table("MSFT")
print(quote['Forward Dividend & Yield'].split()[1].split()[0].replace("(","").replace(")","").strip())#SUmmary section
print(quote['Market Cap'])#SUmmary section

cash_flow = si.get_cash_flow("MSFT")

print(cash_flow.loc['capitalExpenditures',:])#under cash flow section
print(cash_flow.loc['totalCashFromOperatingActivities',:])#Operating Cash Flow under cash flow section
balance_sheet = si.get_balance_sheet("MSFT")
print(balance_sheet.loc['totalCurrentAssets',:])#Total current assets
print(balance_sheet.loc['totalCurrentLiabilities',:])#Current Liabilities
print(balance_sheet.loc['totalStockholderEquity',:])#Common Stock Equity
print(balance_sheet.loc['longTermDebt',:])#Total Debt
print(balance_sheet.loc['totalLiab',:])#Minority interest
print(balance_sheet.loc['totalStockholderEquity',:])#Common Stock Equity

income_statement = si.get_income_statement("MSFT")
print(income_statement.loc['netIncomeApplicableToCommonShares',:])#Net Income Common Stockholders
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
#Dao Jones Stocks
tickers = ["MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KO","DIS",
           "XOM","GE","GS","HD","IBM","INTC","JNJ","JPM","MCD","MRK",
           "MSFT","NKE","PG","TRV","UTX","UNH","VZ","V","WMT"]
tickers=["AAPL"]
#list of tickers whose financial data needs to be extracted
financial_dir = {}

for ticker in tickers:
    print(ticker)
    #getting balance sheet data from yahoo finance for the given ticker
    temp_dir = {}
    temp_dir2 = {}
    temp_dir3 = {}
    url = 'https://finance.yahoo.com/quote/'+ticker+'/balance-sheet?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')     
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2])>1:
                temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
                temp_dir2[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[2]
                temp_dir3[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[3]
    
    balance_sheet = pd.DataFrame()
    try:
        balance_sheet=si.get_balance_sheet(ticker)
    except:
        pass
    
    quote=pd.DataFrame()
    try:
        quote=si.get_quote_table(ticker)
    except:
        pass
    income_statement =pd.DataFrame()
    try:
        income_statement=si.get_income_statement(ticker)
    except:
        pass   
    
    cash_flow =pd.DataFrame()
    try:
        cash_flow=si.get_cash_flow(ticker)
    except:
        pass
    
    if(cash_flow.shape[0]==0):
            
            temp_dir['Capital expenditure']="0"
            temp_dir['Total cash flow from operating activities']="0"
            
            temp_dir2['Capital expenditure']="0"
            temp_dir2['Total cash flow from operating activities']="0"
            
            temp_dir3['Capital expenditure']="0"
            temp_dir3['Total cash flow from operating activities']="0"
    else:   
            if 'Capital expenditure' in cash_flow:
                temp_dir['Capital expenditure']=cash_flow.loc['capitalExpenditures'][0]
                temp_dir2['Capital expenditure']=cash_flow.loc['capitalExpenditures'][1]
                temp_dir3['Capital expenditure']=cash_flow.loc['capitalExpenditures'][2]
            else:
                temp_dir['Capital expenditure']="0"
                temp_dir2['Capital expenditure']="0"
                temp_dir3['Capital expenditure']="0"
            temp_dir['Total cash flow from operating activities']=cash_flow.loc['totalCashFromOperatingActivities'][0]
            temp_dir2['Total cash flow from operating activities']=cash_flow.loc['totalCashFromOperatingActivities'][1]
            temp_dir3['Total cash flow from operating activities']=cash_flow.loc['totalCashFromOperatingActivities'][2]

    if(balance_sheet.shape[0]==0):
            temp_dir['Total current assets']="0"
            temp_dir['Total current liabilities']="0"
            temp_dir['Total stockholder equity']="0"
            temp_dir['Long-term debt']="0"
            temp_dir['Minority interest']="0"
            temp_dir['Common stock']="0"
            temp_dir['Other liabilities']="0"
            
            temp_dir2['Total current assets']="0"
            temp_dir2['Total current liabilities']="0"
            temp_dir2['Total stockholder equity']="0"
            temp_dir2['Long-term debt']="0"
            temp_dir2['Minority interest']="0"
            temp_dir2['Common stock']="0"
            temp_dir2['Other liabilities']="0"
            
            temp_dir3['Total current assets']="0"
            temp_dir3['Total current liabilities']="0"
            temp_dir3['Total stockholder equity']="0"
            temp_dir3['Long-term debt']="0"
            temp_dir3['Minority interest']="0"
            temp_dir3['Common stock']="0"
            temp_dir3['Other liabilities']="0"
            
    else:
            temp_dir['Total current assets']=str(balance_sheet.loc['totalCurrentAssets'][0])
            temp_dir['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][0])
            temp_dir['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][0])
            temp_dir['Long-term debt']=str(balance_sheet.loc['longTermDebt'][0])
            temp_dir['Minority interest']=str(balance_sheet.loc['totalLiab'][0])
            temp_dir['Common stock']=str(balance_sheet.loc['commonStock'][0])
            temp_dir['Other liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][0])
            
            temp_dir2['Total current assets']=str(balance_sheet.loc['totalCurrentAssets'][1])
            temp_dir2['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][1])
            temp_dir2['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][1])
            temp_dir2['Long-term debt']=str(balance_sheet.loc['longTermDebt'][1])
            temp_dir2['Minority interest']=str(balance_sheet.loc['totalLiab'][1])
            temp_dir2['Common stock']=str(balance_sheet.loc['commonStock'][1])
            temp_dir2['Other liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][1])
            
            temp_dir3['Total current assets']=str(balance_sheet.loc['totalCurrentAssets'][2])
            temp_dir3['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][2])
            temp_dir3['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][2])
            temp_dir3['Long-term debt']=str(balance_sheet.loc['longTermDebt'][2])
            temp_dir3['Minority interest']=str(balance_sheet.loc['totalLiab'][2])
            temp_dir3['Common stock']=str(balance_sheet.loc['commonStock'][2])
            temp_dir3['Other liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][2])
            if "propertyPlantEquipment" in balance_sheet:
                temp_dir['Property plant and equipment']=str(balance_sheet.loc['propertyPlantEquipment'][0])
                temp_dir2['Property plant and equipment']=str(balance_sheet.loc['propertyPlantEquipment'][1])
                temp_dir3['Property plant and equipment']=str(balance_sheet.loc['propertyPlantEquipment'][2])
            else:
                temp_dir['Property plant and equipment']="0"
                temp_dir2['Property plant and equipment']="0"
                temp_dir3['Property plant and equipment']="0"
            
    if income_statement.shape[0]==0:
            temp_dir['Net income applicable to common shares']="0"
            temp_dir2['Net income applicable to common shares']="0"
            temp_dir3['Net income applicable to common shares']="0"
            
            
    else:
            
            
            temp_dir['Net income applicable to common shares']=income_statement.loc['netIncomeApplicableToCommonShares'][0]
            temp_dir2['Net income applicable to common shares']=income_statement.loc['netIncomeApplicableToCommonShares'][1]
            temp_dir3['Net income applicable to common shares']=income_statement.loc['netIncomeApplicableToCommonShares'][2]
    if 'Market Cap' in quote:
            temp_dir['Market cap (intra-day)']=quote['Market Cap']
            temp_dir2['Market cap (intra-day)']=quote['Market Cap']
            temp_dir3['Market cap (intra-day)']=quote['Market Cap']
    else:
            temp_dir['Market cap (intra-day)']='0'
            temp_dir2['Market cap (intra-day)']='0'
            temp_dir3['Market cap (intra-day)']='0'
    
    
    #getting income statement data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2])>1:
                temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
    
    #getting cashflow statement data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/'+ticker+'/cash-flow?p='+ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("table", {"class" : "Lh(1.7) W(100%) M(0)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2])>1:
                temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
                temp_dir2[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[2]
                temp_dir3[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[3]
    
    #getting key statistics data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.findAll("table", {"class": "W(100%) Bdcl(c)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2])>0:  
                temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[-1]    
               
    #combining all extracted information with the corresponding ticker
    financial_dir[ticker] = temp_dir
