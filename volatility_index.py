# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:11:49 2021

@author: bansi
"""


import yfinance as yf
import time
import streamlit as st
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import statistics


st.set_page_config(
    page_title="Stock Analysis App",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('STOCK VOLATILITY')

st.sidebar.image('https://media.captrust.com/wordpress-content/2019/03/volatility.jpg', width=290)
st.sidebar.write('')

st.sidebar.info(
        "**Volatility is a measure of risk and shows how values are spread out around the average price. A stock with a price that fluctuates wildly hits new highs and lows or moves erratically, is taken under consideration as highly volatile. A highly volatile stock is inherently riskier, but that risk cuts both ways.**"
    )

months = st.selectbox(
    'SELECT NUMBER OF MONTHS',
    ('1','2', '3', '4', '5', '6', '7','8','9', '10', '11', '12', '13', '14')
)

tf = months + 'mo'
#st.write(periods) 

st.markdown(
    """
    <style>
    .selector-rect {
        fill: grey  !important; 
    }
    p{
    color: black;
    text-align: justify;
    }
    img{
    margin-top: 10px;
    margin-left: 7px;
    }
    div.row-widget.stRadio > div[role='radiogroup'] > label[data-baseweb='radio'] > div:first-child{
    background-color: #5e829f;
    }
    .st-av{
    background-color: #5e829f ;
    }
    .st-ch {
    background-color: #5e829f;
    }
    .st-cc{
       font-size: 17px;
       font-weight: 510;
       }
    .css-vfskoc{
    font-size: 20px;
    color: white;
    font-weight: 900;
    }
    .st-bj {
    margin-top: 11px;
    }
    #MainMenu {visibility : hidden;}
    footer {visibility : hidden;}
    footer:after {
    font-size: 15px;
    content: 'Made By: Namrata Patel, Bansi Shah, Darshi Shah, Vishal Shah';
    visibility: visible;
    position: relative;
    display: block;
    background-color: #5e829f;
    color: white;
    text-align: center;
    }
    h3{
    font-size: 18px;
    font-weight: 700;
    color: #2cab18;
    }
    h1{
      text-align: center;}
    </style>
    """,
    unsafe_allow_html=True
)


data_apple = yf.download(tickers='AAPL', period=tf, interval="1d")
data_google = yf.download(tickers='GOOG', period=tf, interval="1d")
data_microsoft = yf.download(tickers='MSFT', period=tf, interval="1d")
data_tesla = yf.download(tickers='TSLA', period=tf, interval="1d")
data_accenture = yf.download(tickers='ACN', period=tf, interval="1d")
data_ibm = yf.download(tickers='IBM', period=tf, interval="1d")
var_apple = statistics.pstdev(data_apple['Close'])
var_google = statistics.pstdev(data_google['Close'])
var_microsoft = statistics.pstdev(data_microsoft['Close'])
var_tesla = statistics.pstdev(data_tesla['Close'])
var_accenture = statistics.pstdev(data_accenture['Close'])
var_ibm = statistics.pstdev(data_ibm['Close'])
arr = [['Apple', var_apple], ['Google', var_google], ['Microsoft', var_microsoft], ['Tesla', var_tesla], ['Accenture', var_accenture], ['IBM', var_ibm]]
for i in range(6):
    for j in range(0, 6-i-1):
        if arr[j][1] > arr[j+1][1] :
          arr[j], arr[j+1] = arr[j+1], arr[j]

col1, col2, col3 = st.beta_columns((7,1,7))

x_values = ['Apple', 'Google', 'Microsoft', 'Tesla', 'IBM', 'Accenture']
y_values = [var_apple, var_google, var_microsoft, var_tesla, var_ibm, var_accenture]

fig = go.Figure(data=[go.Bar(
    x=x_values,
    y=y_values,
    marker={'color': 'darkorange'},
    )
])
fig.update_layout(
        barmode='group',
        width=550,
        margin=dict(l=0),
        plot_bgcolor='darkgrey')
col1.plotly_chart(fig)

v = np.array(arr)

df = pd.DataFrame()

df["Stock"], df["Volatility"] = v.T

#st.write(data_google)
 
fig = go.Figure(data=[go.Table(
    header=dict(values=['Stock', 'Volatility'],
                line_color='darkslategray',
                fill_color='#085089',
                align='center',
                font=dict(color='black', size=25),
                height=40),
    cells=dict(values=[df["Stock"],
                      df["Volatility"]],
                line_color='darkslategray',
                fill=dict(color=['#b7d3e9', '#b7d3e9']),
                align='center',
                font=dict(color='black', size=20),
                height=35))
])

fig.update_layout(
           
        width=550,
        margin=dict(l=0))

col3.plotly_chart(fig)

