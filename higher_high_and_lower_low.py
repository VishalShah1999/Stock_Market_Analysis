# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:06:15 2021
@author: bansi
"""


import yfinance as yf
import time
import streamlit as st
import plotly.graph_objs as go


#time.sleep(190)
max1=-1
trigger=0
higher_high = False
lower_low = False
stop_loss = 0

st.set_page_config(
    page_title="Stock Analysis App",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title('HIGHER HIGH & LOWER LOW PATTERN')

st.sidebar.image('https://image.freepik.com/free-vector/buy-sell-concept-design-showing-bull-bear_1017-13716.jpg', width=270)
st.sidebar.write('')

stock_name = st.sidebar.radio(
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

data = yf.download(tickers=ticker_symbol, period='1d', interval="1m")
fig = go.Figure()

s = st.empty()
p = st.empty()



#Show
#fig.show()
st.markdown(
    """
    <style>
    .selector-rect {
        fill: grey  !important; 
    }
    img{
    margin-top: 10px;
    margin-left: 14px;
    }
    div.row-widget.stRadio > div[role='radiogroup'] > label[data-baseweb='radio'] > div:first-child{
    background-color: #5e829f;
    }
    .st-ce{
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
    p{
    font-size: 25px;
    color: #fff;
    margin-left: 40px;
    margin-top: 20px;
    animation: p 1s ease-in-out infinite alternate;
    }
    h1{
      text-align: center;}
    @-webkit-keyframes p {
    from {
    text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #e60073, 0 0 40px #e60073, 0 0 50px #e60073, 0 0 60px #e60073, 0 0 70px #e60073;
  }
  
  to {
    text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6, 0 0 50px #ff4da6, 0 0 60px #ff4da6, 0 0 70px #ff4da6, 0 0 80px #ff4da6;

  }

}
    </style>
    """,
    unsafe_allow_html=True
)


while(True):
    data1 = yf.download(tickers=ticker_symbol, period='1d', interval="1m")
    data1 = data1[:-1]
    #Candlestick
    fig.add_trace(go.Candlestick(x=data1.index,
                    open=data1['Open'],
                    high=data1['High'],
                    low=data1['Low'],
                    close=data1['Close'],
                    showlegend = False))
    
    # Add titles
    fig.update_layout(
        title= stock_name + ' live share price evolution',
        yaxis_title='Stock Price (USD per Shares)',
        width=800, height=800,
        margin=dict(l=0))
    
    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    data1.reset_index(inplace=True,drop=False)
    current_data = data1.tail(4)
    #st.write(current_data[['Datetime','Close','High','Low']])
    high = list(current_data['High'])
    low = list(current_data['Low'])
    count_h, count_l=0,0
    
    for i in range(3):
        if higher_high == False and lower_low == False:
            if high[i] > max1:
                count_h+=1
                max1 = high[i]
                min1 = low[i]
                count_l = 0
            else:
                count_h=0
                if low[i] < min1:
                    count_l+=1
                    min1 = low[i]
                    max1 = high[i]
                    
        elif higher_high == True :
            if high[i] > trigger:
                count_h+=1
                trigger = high[i]
                max1 = high[i]
                count_l = 0
            else:
                count_h=0
                if low[i] < min1:
                    count_l+=1
                    min1 = low[i]
                
                
        elif lower_low == True :
            if high[i] > max1:
                count_h+=1
                max1 = high[i]
                count_l = 0
            else:
                count_h=0
                if low[i] < trigger:
                    count_l+=1
                    trigger = low[i]
                    min1 = low[i]
            
    if count_h==3:
        s.write("SUGGESTION: GO FOR BUY")
        trigger = max1
        stop_loss = low[0]
        risk = (trigger - stop_loss) * 3
        min1 = stop_loss
        higher_high = True
        lower_low = False
        temp = trigger
        
        
    if count_l==3:
        s.write("SUGGESTION: GO FOR SELL")
        trigger = min1
        stop_loss = high[0]
        risk = (trigger - stop_loss) * 3
        max1 = stop_loss
        lower_low = True
        higher_high = False
        temp = trigger
        
    elif higher_high == True and count_h != 3 and count_l != 3 :
        #s.write("No Pattern Found This Time")
        trigger = temp
        min1 = stop_loss
        
        
    elif higher_high == False and lower_low == False :
        s.write("NO SUGGESTION YET!!")
        max1 = high[0]
        min1 = low[0]
      
    
    elif lower_low == True and count_l != 3 and count_h != 3:
        #s.write("No Pattern Found This Time")
        trigger = temp    
        max1 = stop_loss
        
    p.plotly_chart(fig)
        
    time.sleep(60)
    
    
