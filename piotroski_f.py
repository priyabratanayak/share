# ============================================================================
# Piotroski f score implementation (data scraped from yahoo finance)

# Please report bugs/issues in the Q&A section
# =============================================================================


import requests
from bs4 import BeautifulSoup
import pandas as pd
import yahoo_fin.stock_info as si
tickers = ["MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KO","DIS","DWDP",
           "XOM","GE","GS","HD","IBM","INTC","JNJ","JPM","MCD","MRK",
           "MSFT","NKE","PFE","PG","TRV","UTX","UNH","VZ","V","WMT"]


#list of tickers whose financial data needs to be extracted
financial_dir_cy = {} #directory to store current year's information
financial_dir_py = {} #directory to store last year's information
financial_dir_py2 = {} #directory to store last to last year's information

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
            if 'Total Assets' not in temp_dir:                
                temp_dir['Total Assets']="0"
            
            temp_dir2['Total current assets']="0"
            temp_dir2['Total current liabilities']="0"
            temp_dir2['Total stockholder equity']="0"
            temp_dir2['Long-term debt']="0"
            temp_dir2['Minority interest']="0"
            temp_dir2['Common stock']="0"
            temp_dir2['Other liabilities']="0"
           
            if 'Total Assets' not in temp_dir2:
                temp_dir2['Total Assets']="0"
            
            
            temp_dir3['Total current assets']="0"
            temp_dir3['Total current liabilities']="0"
            temp_dir3['Total stockholder equity']="0"
            temp_dir3['Long-term debt']="0"
            temp_dir3['Minority interest']="0"
            temp_dir3['Common stock']="0"
            temp_dir3['Other liabilities']="0"
            if 'Total Assets' not in temp_dir3: 
                temp_dir3['Total Assets']="0"
    else:
            if 'Total Assets' not in temp_dir:                
                temp_dir['Total Assets']="0"
            if 'Total Assets' not in temp_dir3: 
                temp_dir3['Total Assets']="0"
            if 'Total Assets' not in temp_dir2:
                temp_dir2['Total Assets']="0"
                
            if temp_dir['Total Assets']=="0":
                temp_dir['Total Assets']=str(balance_sheet.loc['totalAssets'][0])
            temp_dir['Total current assets']=str(balance_sheet.loc['totalAssets'][0])
            temp_dir['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][0])
            temp_dir['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][0])
            temp_dir['Long-term debt']=str(balance_sheet.loc['longTermDebt'][0])
            temp_dir['Minority interest']=str(balance_sheet.loc['totalLiab'][0])
            try:
                temp_dir['Common stock']=str(balance_sheet.loc['commonStock'][0])
            except:
                temp_dir['Common stock']="0"
            temp_dir['Other liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][0])
            
            temp_dir2['Total current assets']=str(balance_sheet.loc['totalCurrentAssets'][1])
            temp_dir2['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][1])
            temp_dir2['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][1])
            temp_dir2['Long-term debt']=str(balance_sheet.loc['longTermDebt'][1])
            temp_dir2['Minority interest']=str(balance_sheet.loc['totalLiab'][1])
            try:
                temp_dir2['Common stock']=str(balance_sheet.loc['commonStock'][1])
            except:
                temp_dir2['Common stock']="0"
            temp_dir2['Other liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][1])
            if temp_dir2['Total Assets']=="0":
                temp_dir2['Total Assets']=str(balance_sheet.loc['totalAssets'][1])
            
            temp_dir3['Total current assets']=str(balance_sheet.loc['totalCurrentAssets'][2])
            temp_dir3['Total current liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][2])
            temp_dir3['Total stockholder equity']=str(balance_sheet.loc['totalStockholderEquity'][2])
            temp_dir3['Long-term debt']=str(balance_sheet.loc['longTermDebt'][2])
            temp_dir3['Minority interest']=str(balance_sheet.loc['totalLiab'][2])
            try:
                temp_dir3['Common stock']=str(balance_sheet.loc['commonStock'][2])
            except:
                temp_dir3['Common stock']="0"
            temp_dir3['Other liabilities']=str(balance_sheet.loc['totalCurrentLiabilities'][2])
            if temp_dir3['Total Assets']=="0":
                temp_dir3['Total Assets']=str(balance_sheet.loc['totalAssets'][2])
            
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
            
            temp_dir['Total Revenue']=0
            temp_dir2['Total Revenue']=0
            temp_dir3['Total Revenue']=0
            temp_dir['Gross Profit']=0
            temp_dir2['Gross Profit']=0
            temp_dir3['Gross Profit']=0
            
            
            
    else:   
            
            if 'Gross Profit'not in temp_dir:
                temp_dir['Gross Profit']=0
                temp_dir2['Gross Profit']=0
                temp_dir3['Gross Profit']=0
            temp_dir['Gross Profit']=income_statement.loc['grossProfit'][0]
            temp_dir2['Gross Profit']=income_statement.loc['grossProfit'][1]
            temp_dir3['Gross Profit']=income_statement.loc['grossProfit'][2]
            
            if 'Total Revenue'not in temp_dir:
                temp_dir['Total Revenue']=0
                temp_dir2['Total Revenue']=0
                temp_dir3['Total Revenue']=0
                
            temp_dir['Total Revenue']=income_statement.loc['totalRevenue'][0]
             
            temp_dir2['Total Revenue']=income_statement.loc['totalRevenue'][1]
            
            temp_dir3['Total Revenue']=income_statement.loc['totalRevenue'][2]
            
            
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
                temp_dir2[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[2]
                temp_dir3[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[3]
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
    financial_dir_cy[ticker] = temp_dir
    financial_dir_py[ticker] = temp_dir2
    financial_dir_py2[ticker] = temp_dir3


#storing information in pandas dataframe
combined_financials_cy = pd.DataFrame(financial_dir_cy)

combined_financials_cy.dropna(inplace=True) #dropping columns with all NaN values

combined_financials_py = pd.DataFrame(financial_dir_py)
combined_financials_py.dropna(inplace=True)
combined_financials_py2 = pd.DataFrame(financial_dir_py2)
combined_financials_py2.dropna(inplace=True)
tickers = combined_financials_cy.columns #updating the tickers list based on only those tickers whose values were successfully extracted

# selecting relevant financial information for each stock using fundamental data
stats = ["Net income applicable to common shares",
         "Total Assets",
         "Total cash flow from operating activities",
         "Long-term debt",
         "Other liabilities",
         "Total current assets",
         "Total current liabilities",
         "Common stock",
         "Total Revenue",
         "Gross Profit"] # change as required

indx = ["NetIncome","TotAssets","CashFlowOps","LTDebt","OtherLTDebt",
        "CurrAssets","CurrLiab","CommStock","TotRevenue","GrossProfit"]


def info_filter(df,stats,indx):
    """function to filter relevant financial information for each 
       stock and transforming string inputs to numeric"""
    
    tickers = df.columns
    
    all_stats = {}
    for ticker in tickers:
        try:
            
            temp = df[ticker]
            ticker_stats = []
            for stat in stats:
                
                ticker_stats.append(temp.loc[stat])
            all_stats['{}'.format(ticker)] = ticker_stats
        except:
            print("can't read data for ",ticker)
    
    all_stats_df = pd.DataFrame(all_stats,index=indx)
    
    # cleansing of fundamental data imported in dataframe
    all_stats_df[tickers] = all_stats_df[tickers].replace({',': ''}, regex=True)
    for ticker in all_stats_df.columns:
        all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values,errors='coerce')
    return all_stats_df

def piotroski_f(df_cy,df_py,df_py2):
    """function to calculate f score of each stock and output information as dataframe"""
    f_score = {}
    tickers = df_cy.columns
    for ticker in tickers:
        ROA_FS = int(df_cy.loc["NetIncome",ticker]/((df_cy.loc["TotAssets",ticker]+df_py.loc["TotAssets",ticker])/2) > 0)
        CFO_FS = int(df_cy.loc["CashFlowOps",ticker] > 0)
        ROA_D_FS = int(df_cy.loc["NetIncome",ticker]/(df_cy.loc["TotAssets",ticker]+df_py.loc["TotAssets",ticker])/2 > df_py.loc["NetIncome",ticker]/(df_py.loc["TotAssets",ticker]+df_py2.loc["TotAssets",ticker])/2)
        CFO_ROA_FS = int(df_cy.loc["CashFlowOps",ticker]/df_cy.loc["TotAssets",ticker] > df_cy.loc["NetIncome",ticker]/((df_cy.loc["TotAssets",ticker]+df_py.loc["TotAssets",ticker])/2))
        LTD_FS = int((df_cy.loc["LTDebt",ticker] + df_cy.loc["OtherLTDebt",ticker])<(df_py.loc["LTDebt",ticker] + df_py.loc["OtherLTDebt",ticker]))
        CR_FS = int((df_cy.loc["CurrAssets",ticker]/df_cy.loc["CurrLiab",ticker])>(df_py.loc["CurrAssets",ticker]/df_py.loc["CurrLiab",ticker]))
        DILUTION_FS = int(df_cy.loc["CommStock",ticker] <= df_py.loc["CommStock",ticker])
        GM_FS = int((df_cy.loc["GrossProfit",ticker]/df_cy.loc["TotRevenue",ticker])>(df_py.loc["GrossProfit",ticker]/df_py.loc["TotRevenue",ticker]))
        ATO_FS = int(df_cy.loc["TotRevenue",ticker]/((df_cy.loc["TotAssets",ticker]+df_py.loc["TotAssets",ticker])/2)>df_py.loc["TotRevenue",ticker]/((df_py.loc["TotAssets",ticker]+df_py2.loc["TotAssets",ticker])/2))
        f_score[ticker] = [ROA_FS,CFO_FS,ROA_D_FS,CFO_ROA_FS,LTD_FS,CR_FS,DILUTION_FS,GM_FS,ATO_FS]
    f_score_df = pd.DataFrame(f_score,index=["PosROA","PosCFO","ROAChange","Accruals","Leverage","Liquidity","Dilution","GM","ATO"])
    return f_score_df
df=combined_financials_cy
# Selecting stocks with highest Piotroski f score
transformed_df_cy = info_filter(combined_financials_cy,stats,indx)
transformed_df_py = info_filter(combined_financials_py,stats,indx)
transformed_df_py2 = info_filter(combined_financials_py2,stats,indx)

f_score_df = piotroski_f(transformed_df_cy,transformed_df_py,transformed_df_py2)
f_score_df_sum=f_score_df.sum().sort_values(ascending=False)
#Don not change the nan value to 0. It wi make the calculation wrong
print("...................................")
print(f_score_df.sum().sort_values(ascending=False))

#Try to pick stocks with 9. If not at max 8
