import pandas as pd
import yfinance as yf
import datetime as dt
import pandas_ta as ta
import numpy as np
from stqdm import stqdm
from pytz import timezone 
from datetime import datetime
import io
import requests
import streamlit as st

st.title('Nifty 100 Doji & Green App')

@st.cache
def load_data():
    url="https://raw.githubusercontent.com/rushiai/data_csv/main/nifty_fir_100.csv"
    link=requests.get(url).content
    tickers=pd.read_csv(io.StringIO(link.decode('utf-8')))
    return tickers

tickers = load_data()

master_data = {}
today_doji = []
green_candle = []
# today - how many days
when = -1
# after second day of doji
when_green = when + 1

def stock_data():
    ind_time = datetime.now(timezone("Asia/Kolkata"))
    st.write('we are watching the green candle of following day and doji previous day market days only')
    st.write('Please use after 9.30 AM so you can get a right result for Green candles')
    st.write(ind_time)
    
    start = ind_time-dt.timedelta(200)
    end = ind_time
    
    for tick in stqdm(tickers.name):
        fdf = yf.download(tick,start=start, end=end,interval='1d', progress=False)
        fdf['green'] = fdf.Close > fdf.Open
        master_data[tick] = fdf
        try:
            # kk = fdf.copy()
            # doji_df = talib.CDLDOJI(fdf.Open, fdf.High, fdf.Low, fdf.Close)
            doji_df = fdf.ta.cdl_pattern(name="doji")
            if doji_df.iloc[when][0] >= 50:
                today_doji.append(tick)
        except:
            pass
        try:
            if master_data[tick]['green'][when_green] == True:
                green_candle.append(tick)
        except:
            pass
    print(list(set(today_doji) & set(green_candle)))
    return list(set(today_doji) & set(green_candle))

if st.button('Start app'):
    st.write('Please wait...')
    final_list = stock_data()
    st.markdown(final_list)
