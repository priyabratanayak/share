# ============================================================================
# Greenblatt's Magic Formula Implementation

# Please report bugs/issues in the Q&A section
# =============================================================================


import requests
from bs4 import BeautifulSoup
import pandas as pd
import yahoo_fin.stock_info as si
#Dao Jones Stocks
tickers = ["MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KO","DIS","DWDP",
           "XOM","GE","GS","HD","IBM","INTC","JNJ","JPM","MCD","MRK",
           "MSFT","NKE","PFE","PG","TRV","UTX","UNH","VZ","V","WMT"]

#list of tickers whose financial data needs to be extracted
financial_dir = {}



for ticker in tickers:
    print(ticker)
    #getting balance sheet data from yahoo finance for the given ticker
    temp_dir = {}
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
    else:   
            if 'Capital expenditure' in cash_flow:
                temp_dir['Capital expenditure']=cash_flow.loc['capitalExpenditures'][0]
            else:
                temp_dir['Capital expenditure']="0"
            temp_dir['Total cash flow from operating activities']=cash_flow.loc['totalCashFromOperatingActivities'][0]

    if(balance_sheet.shape[0]==0):
            temp_dir['Total current assets']="0"
            temp_dir['Total current liabilities']="0"
            temp_dir['Total stockholder equity']="0"
            temp_dir['Long-term debt']="0"
            temp_dir['Minority interest']="0"
    else:
            temp_dir['Total current assets']=str(balance_sheet.loc['totalCurrentAssets'][0])
            temp_dir['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][0])
            temp_dir['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][0])
            temp_dir['Long-term debt']=str(balance_sheet.loc['longTermDebt'][0])
            temp_dir['Minority interest']=str(balance_sheet.loc['totalLiab'][0])
            if "propertyPlantEquipment" in balance_sheet:
                temp_dir['Property plant and equipment']=str(balance_sheet.loc['propertyPlantEquipment'][0])
            else:
                temp_dir['Property plant and equipment']="0"
            
    if income_statement.shape[0]==0:
            temp_dir['Net income applicable to common shares']="0"
    else:
            temp_dir['Net income applicable to common shares']=income_statement.loc['netIncomeApplicableToCommonShares'][0]
    if 'Market Cap' in quote:
            temp_dir['Market cap (intra-day)']=quote['Market Cap']
    else:
            temp_dir['Market cap (intra-day)']='0'
    if 'Forward Dividend & Yield' in quote:
            temp_dir["Forward annual dividend yield"]=quote['Forward Dividend & Yield'].split()[1].split()[0].replace("(","").replace(")","").strip()
    else:
            temp_dir["Forward annual dividend yield"]="0"
    
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


#storing information in pandas dataframe
combined_financials = pd.DataFrame(financial_dir)
combined_financials.dropna(how='all',axis=1,inplace=True) #dropping columns with all NaN values
tickers = combined_financials.columns #updating the tickers list based on only those tickers whose values were successfully extracted

# creating dataframe with relevant financial information for each stock using fundamental data

stats = ["EBIT",
         "Market cap (intra-day)",
         "Net income applicable to common shares",
         "Total cash flow from operating activities",
         "Capital expenditure",
         "Total current assets",
         "Total current liabilities",
         "Property plant and equipment",
         "Total stockholder equity",
         "Long-term debt",
        # "Preferred stock",
         "Minority interest",
         "Forward annual dividend yield"] # change as required


#......................................................
#Forward annual dividend yield:Forward Dividend & Yield
#Earnings before interest and taxes:EBIT
#Long-term debt:Total Debt
#Total stockholder equity:Common Stock Equity
#Market cap (intra-day):Market Cap under summary section
#Net income applicable to common shares: Net Income Common Stockholders
#Total cash flow from operating activities:Operating Cash Flow under cash flow section
# Minority interest:Minority Interest

#share holders equity total:Common Stock Equity
#Total current liabilities:Current Liabilities
#Current Assets:Total current assets
#Capital expenditures:Capital Expenditure under cash flow
#......................................................
indx = ["EBIT","MarketCap","NetIncome","CashFlowOps","Capex","CurrAsset",
        "CurrLiab","PPE","BookValue","TotDebt","MinInterest","DivYield"]#removed "PrefStock"
all_stats = {}
for ticker in tickers:
    try:
        temp = combined_financials[ticker]
        ticker_stats = []
        for stat in stats:
            ticker_stats.append(temp.loc[stat])
        all_stats['{}'.format(ticker)] = ticker_stats
    except:
        print("can't read data for ",ticker)

all_stats_df = pd.DataFrame(all_stats,index=indx)

# cleansing of fundamental data imported in dataframe
all_stats_df.iloc[1,:] = [x.replace("M","E+03") for x in all_stats_df.iloc[1,:].values]
all_stats_df.iloc[1,:] = [x.replace("B","E+06") for x in all_stats_df.iloc[1,:].values]
all_stats_df.iloc[1,:] = [x.replace("T","E+09") for x in all_stats_df.iloc[1,:].values]
all_stats_df.iloc[-1,:] = [str(x).replace("%","E-02") for x in all_stats_df.iloc[-1,:].values]
all_stats_df[tickers] = all_stats_df[tickers].replace({',': ''}, regex=True)
for ticker in all_stats_df.columns:
    all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values,errors='coerce')

# calculating relevant financial metrics for each stock
transpose_df = all_stats_df.transpose()
final_stats_df = pd.DataFrame()
final_stats_df["EBIT"] = transpose_df["EBIT"]
final_stats_df["TEV"] =  transpose_df["MarketCap"].fillna(0) \
                         +transpose_df["TotDebt"].fillna(0) \
                         +transpose_df["MinInterest"].fillna(0) \
                         -(transpose_df["CurrAsset"].fillna(0)-transpose_df["CurrLiab"].fillna(0))
final_stats_df["EarningYield"] =  final_stats_df["EBIT"]/final_stats_df["TEV"]
final_stats_df["FCFYield"] = (transpose_df["CashFlowOps"]-transpose_df["Capex"])/transpose_df["MarketCap"]
final_stats_df["ROC"]  = transpose_df["EBIT"]/(transpose_df["PPE"]+transpose_df["CurrAsset"]-transpose_df["CurrLiab"])
final_stats_df["BookToMkt"] = transpose_df["BookValue"]/transpose_df["MarketCap"]
final_stats_df["DivYield"] = transpose_df["DivYield"]


################################Output Dataframes##############################

# finding value stocks based on Magic Formula
final_stats_val_df = final_stats_df.loc[tickers,:]
final_stats_val_df["CombRank"] = final_stats_val_df["EarningYield"].rank(ascending=False,na_option='bottom')+final_stats_val_df["ROC"].rank(ascending=False,na_option='bottom')
final_stats_val_df["MagicFormulaRank"] = final_stats_val_df["CombRank"].rank(method='first')
value_stocks = final_stats_val_df.sort_values("MagicFormulaRank").iloc[:,[2,4,8]]
print("------------------------------------------------")
print("Value stocks based on Greenblatt's Magic Formula")
print(value_stocks)


# finding highest dividend yield stocks
high_dividend_stocks = final_stats_df.sort_values("DivYield",ascending=False).iloc[:,6]
print("------------------------------------------------")
print("Highest dividend paying stocks")
print(high_dividend_stocks)


# # Magic Formula & Dividend yield combined
final_stats_df["CombRank"] = final_stats_df["EarningYield"].rank(ascending=False,method='first') \
                              +final_stats_df["ROC"].rank(ascending=False,method='first')  \
                              +final_stats_df["DivYield"].rank(ascending=False,method='first')
final_stats_df["CombinedRank"] = final_stats_df["CombRank"].rank(method='first')
value_high_div_stocks = final_stats_df.sort_values("CombinedRank").iloc[:,[2,4,6,8]]
print("------------------------------------------------")
print("Magic Formula and Dividend Yield combined")
print(value_high_div_stocks)
