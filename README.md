# Analyzing Stock Market Behaviour Using Stream Data Analytics

## Problem Description
Stock market trading is a side investment to a lot of people with other full-time jobs. Therefore, a system is needed to assist such people with all the cumbersome groundwork of studying, researching, analysing and finding patterns to understand stock behaviour. There is a need for a system that provides analysis of various stocks to traders to simplify and automate their task of predicting stock market behaviour, when to buy and sell the shares, what will be the closing prices of stocks, and how volatile each stock is.

## Scope
Our system is useful for people who want to invest in stocks and the people who are already a trader. Our system has various modules for making decisions of buying and selling the stock at the appropriate time.

##  Dataset
For collecting real-time data of stocks we first explored a way in which we needed to write a google script and pass the API from which the script fetched the intraday data of every stock. But due to some reasons, this approach didn’t work for us. As an alternative to this, we tried GoogleFinance API which directly works on Google Sheets. But the only drawback is that this API can only fetch the day-wise data so we thought of using this data for training our model. Now for testing, we again scrutinized some other options and we got a yfinance library. It can retrieve data in various periods such as minute-wise, hour-wise, etc.
