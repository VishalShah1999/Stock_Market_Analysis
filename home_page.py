# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 15:44:51 2021

@author: Vishal
"""

import streamlit as st
import plotly.graph_objs as go
import yfinance as yf
from plotly.subplots import make_subplots
from bokeh.models.widgets import Div

st.set_page_config(
    page_title="Stock Analysis App",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="expanded",
)

#from PIL import Image
#image = Image.open('banner.jpg')

html_temp = """
    <h1><b>Analyzing Stock Market Behaviour using Stream Data Analytics</b></h1>
    <div class="description">
    <h2 style="color:black;text-align:left;line-height:1.4; text-align: justify;">
    This website provides real-time analysis of stock data for six companies 
    listed in the New York Stock Exchange. The analysis consists of
    predicting the closing price every minute and comparing it with 
    the actual one using a machine learning model that gets updated 
    daily through incremental learning approach. It also gives suggetions
    regarding buying and selling of shares by continuously scanning incoming
    stock data and applying trading strategies. </h2>
    </div>
    """
st.markdown(html_temp, unsafe_allow_html = True)

st.sidebar.image('https://cdn.lynda.com/course/614311/614311-637491164389647572-16x9.jpg', width=300)
st.sidebar.write('')
st.markdown("""
    <style>
    .css-1tdez3t {
        padding: 2em 1.3em;
        background-color: #c7c7c7;
        background-image: none;
    }
    div[role="radiogroup"] >  :first-child{
                display: none !important; }
    </style>
""", unsafe_allow_html=True)


#if dataset_name == 'Closing Price Analysis':
if st.sidebar.button('Closing Price Analysis'):
    js = "window.open('https://closing-price-analysis.herokuapp.com/')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

if st.sidebar.button('Higher High & Lower Low Pattern'):
    js = "window.open('https://higher-high-lower-low.herokuapp.com/')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

if st.sidebar.button('Volatality Index'):
    js = "window.open('https://stock-volatility.herokuapp.com/')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)


st.markdown(
    """
    <style>
    .reportview-container {
        background-color: white; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

#st.footer("Made with ❤💕")
hide = """
<style>
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
.st-bj {
    margin-top: 11px;
    }
div.row-widget.stRadio > div[role='radiogroup'] > label[data-baseweb='radio'] > div:first-child{
    background-color: #5e829f;
    }
.st-ch {
    background-color: #5e829f;
}
.st-ce {
    background-color: #5e829f ;
}
.st-cc{
       color: black;
       font-size: 17px;
       font-weight: 510;
       }
.st-cy {
    background-color: #b7d3e9 !important;
}
.css-vfskoc{
    font-size: 20px;
    color: black;
    font-weight: 900;
    }
h1{
     color: #085089;
     font-size: 45px;
     text-align: center;
     }
img{
    margin-top: 30px;
    }
.description
{
 background:#b7d3e9;
 padding:10px; 
 margin-top:30px; 
 border-style: none none none solid;
 border-color: #085089;
 border-width: 10px;
 }
h2{
   font-size: 20px;
   }
.selector-rect {
        fill: #c7c7c7  !important; 
    }
.selector-text {
        fill: black  !important; 
    }
.st-d0 {
    background-color: #5e829f;
}
.st-e2 {
    background-color: #5e829f;
}
.css-1sapc5z {
    background: #5e829f;
    color : black;
    font-weight: 600;}
</style>
"""
st.markdown(hide, unsafe_allow_html=True)

stock_name = st.selectbox(
    'SELECT STOCK',
    ('Apple', 'Google', 'Microsoft', 'Tesla', 'IBM', 'Accenture')
)

if stock_name == 'Apple':
        ticker_symbol = 'AAPL'
elif stock_name == 'Google':
        ticker_symbol = 'GOOG'
elif stock_name == 'Microsoft':
        ticker_symbol = 'MSFT'
elif stock_name == 'Tesla':
        ticker_symbol = 'TSLA'
elif stock_name == 'IBM':
        ticker_symbol = 'IBM'
elif stock_name == 'Accenture':
        ticker_symbol = 'ACN'

fig = go.Figure()


data1 = yf.download(tickers=ticker_symbol, period='1Y', interval="1d")
    
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=data1.index, y=data1['Close'], name="Close"),
        secondary_y=True,)

fig.add_trace(go.Scatter(x=data1.index, y=data1['Open'], name="Open"),
        secondary_y=True,)

fig.add_trace(go.Scatter(x=data1.index, y=data1['High'], name="High"),
        secondary_y=True,)

fig.add_trace(go.Scatter(x=data1.index, y=data1['Low'], name="Low"),
        secondary_y=True,)
    
    # Add titles
fig.update_layout(
        title= stock_name + ' live share price evolution',
        title_x = 0.5,
        yaxis_title='Stock Price (USD per Shares)',
        width=1035, height=700,
        margin=dict(l=0))
    
    # X-Axes
fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1 month", step="month", stepmode="backward"),
                dict(count=3, label="3 months", step="month", stepmode="backward"),
                dict(count=6, label="6 months", step="month", stepmode="todate"),
                dict(count=1, label="1 year", step="year", stepmode="backward"),
            ])
        )
    )


fig.layout.paper_bgcolor = '#085089'
fig.layout.plot_bgcolor = '#b7d3e9'

st.plotly_chart(fig)
