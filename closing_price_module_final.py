import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import pickle
import time
import datetime
import pytz
import io
import requests
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Stock Analysis App",
    page_icon="🤑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('CLOSING PRICE ANALYSIS')

st.sidebar.image('https://www.fool.com.au/wp-content/uploads/2017/07/time-to-buy.jpg', width=270)
st.sidebar.write('')

dataset_name = st.sidebar.radio(
    'SELECT STOCK',
    ('Apple', 'Google', 'Microsoft', 'Tesla', 'IBM', 'Accenture')
)

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

def get_model(name):
    repo = 'Stock_Market_Analysis'
    if name == 'Apple':
        ticker_symbol = 'AAPL'
        url = "https://github.com/VishalShah1999/" + repo + "/blob/main/" + ticker_symbol + ".p?raw=true"
        byte_content = requests.get(url).content
        model = io.BytesIO(byte_content)
        reg = pickle.load(model)
        return ticker_symbol, reg
    elif name == 'Google':
        ticker_symbol = 'GOOG'
        url = "https://github.com/VishalShah1999/" + repo + "/blob/main/" + ticker_symbol + ".p?raw=true"
        byte_content = requests.get(url).content
        model = io.BytesIO(byte_content)
        reg = pickle.load(model)
        return ticker_symbol, reg
    elif name == 'Microsoft':
        ticker_symbol = 'MSFT'
        url = "https://github.com/VishalShah1999/" + repo + "/blob/main/" + ticker_symbol + ".p?raw=true"
        byte_content = requests.get(url).content
        model = io.BytesIO(byte_content)
        reg = pickle.load(model)
        return ticker_symbol, reg
    elif name == 'Tesla':
        ticker_symbol = "TSLA"
        url = "https://github.com/VishalShah1999/" + repo + "/blob/main/" + ticker_symbol + ".p?raw=true"
        byte_content = requests.get(url).content
        model = io.BytesIO(byte_content)
        reg = pickle.load(model)
        return ticker_symbol, reg
    elif name == 'IBM':
        ticker_symbol = "IBM"
        url = "https://github.com/VishalShah1999/" + repo + "/blob/main/" + ticker_symbol + ".p?raw=true"
        byte_content = requests.get(url).content
        model = io.BytesIO(byte_content)
        reg = pickle.load(model)
        return ticker_symbol, reg
    elif name == 'Accenture':
        ticker_symbol = "ACN"
        url = "https://github.com/VishalShah1999/" + repo + "/blob/main/" + ticker_symbol + ".p?raw=true"
        byte_content = requests.get(url).content
        model = io.BytesIO(byte_content)
        reg = pickle.load(model)
        return ticker_symbol, reg


now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
st.subheader('Actual Closing Price for ' + str(now.date()) + ' : ')
original = st.empty()
st.subheader('Predicted Closing Price for ' + str(now.date()) + ' : ')
predicted = st.empty()
st.subheader("Line Chart (Scaled) :")
line_chart_scaled = st.empty()
st.subheader("Line Chart (Transformed) :")
line_chart_transformed = st.empty()
st.subheader("Errors (Scaled): ")
mae_scaled = st.empty()
mse_scaled = st.empty()
rmse_scaled = st.empty()
r2_scaled = st.empty()
accuracy_scaled = st.empty()
st.subheader("Errors (Transformed): ")
mae_transformed = st.empty()
mse_transformed = st.empty()
rmse_transformed = st.empty()
r2_transformed = st.empty()
accuracy_transformed = st.empty()

while (True):
    ticker, reg = get_model(dataset_name)

    yf_data = yf.download(tickers=ticker, period='1d', interval='1m')
    yf_data.reset_index(inplace=True, drop=False)
    X_test = yf_data[['Open', 'High', 'Low', 'Volume']]
    y_test = yf_data[['Close']]
    size = y_test.size

    scaler = MinMaxScaler()
    scaler = scaler.fit(X_test)
    Xtest_scaled = scaler.transform(X_test)

    scaler = MinMaxScaler()
    scaler = scaler.fit(y_test)
    ytest_scaled = scaler.transform(y_test)

    y_pred = reg.predict(Xtest_scaled)
    y_pred_transform = scaler.inverse_transform(y_pred.reshape(size, 1))
    now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
    #st.write(str(y_test.tail(1)).split(" "))
    statement_for_actual = str(now.hour) + str(':') + str(now.minute) + str(' -- ') + str(y_test.tail(1).to_numpy()[0][0])
    original.write(statement_for_actual)
    statement_for_predicted = str(now.hour) + str(':') + str(now.minute) + str(' -- ') + str(y_pred_transform[-1][0])
    predicted.write(statement_for_predicted)

    ytest_scaled = ytest_scaled.reshape(size)

    y_pred = y_pred.reshape(size)
    y_test = y_test.to_numpy()
    y_test = y_test.reshape(size)
    y_pred_transform = y_pred_transform.reshape(size)

    df = pd.DataFrame({'Actual': ytest_scaled, 'Predicted': y_pred})
    line_chart_scaled.line_chart(df, width=900, height=500)

    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred_transform})
    line_chart_transformed.line_chart(df, width=900, height=500)

    mae_scaled.write('Mean Absolute Error: '+ str(mean_absolute_error(ytest_scaled, y_pred)))
    mse_scaled.write('Mean Squared Error: '+ str(mean_squared_error(ytest_scaled, y_pred)))
    rmse_scaled.write('Root Mean Squared Error: '+ str(np.sqrt(mean_squared_error(ytest_scaled, y_pred))))
    r2_scaled.write('R2 Score: '+ str(r2_score(ytest_scaled, y_pred)))
    accuracy_scaled.write('Accuracy Score: '+ str((1 - (mean_absolute_error(ytest_scaled, y_pred) / ytest_scaled.mean())) * 100))

    mae_transformed.write('Mean Absolute Error: '+ str(mean_absolute_error(y_test, y_pred_transform)))
    mse_transformed.write('Mean Squared Error: '+ str(mean_squared_error(y_test, y_pred_transform)))
    rmse_transformed.write('Root Mean Squared Error: '+ str(np.sqrt(mean_squared_error(y_test, y_pred_transform))))
    r2_transformed.write('R2 Score: '+ str(r2_score(y_test, y_pred_transform)))
    # st.write('Accuracy Score: ', str((1 - (mean_absolute_error(y_test.to_numpy(), y_pred_transform) / y_test.to_numpy().mean())) * 100))
    accuracy_transformed.write('Accuracy Score: '+ str((1 - (mean_absolute_error(y_test, y_pred_transform) / y_test.mean())) * 100))

    time.sleep(60)

