# -*- coding: utf-8 -*-


from yahoofinancials import YahooFinancials

ticker = 'MSFT'
yahoo_financials = YahooFinancials(ticker)
data = yahoo_financials.get_historical_price_data("2018-04-24", "2020-04-24", "daily")#start date, end date, daily. we can change it to weekly or monthly
#It is in the form of json datastructure

