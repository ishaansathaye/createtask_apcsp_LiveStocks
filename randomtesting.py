import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.dates import date2num
from mplfinance.original_flavor import candlestick_ohlc
import numpy as np
import requests
import time
import pandas as pd
import datetime as dt

def getNow(pair):
    return requests.get('https://poloniex.com/public?command=returnTicker').json()[pair]

def getPast(pair, period, daysBack, daysData):
    now = int(time.time())
    end = now-(24*60*60*daysBack)
    start = end-(24*60*60*daysData)
    base = 'https://poloniex.com/public?command=returnChartData&currencyPair='
    response = requests.get('{0}{1}&start={2}&end={3}&period={4}'.format(base, pair, start, end, period))
    return response.json()

pair = "USDT_BTC"    # Use ETH pricing data on the BTC market
period = 7200       # Use 7200 second candles
daysBack = 0       # Grab data starting 0 days ago
daysData = 15       # From there collect 15 days of data

# Request data from Poloniex
data = getPast(pair, period, daysBack, daysData)

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)

#Convert dates do float for matplotlib
data.date = data.date.astype(float)

#Define ohlc
date, closes, highs, lows, opens, volume = data['date'], data['close'], data['high'],data['low'], data['open'], data['volume']
ohlc = [date, opens, highs, lows, closes, volume]


ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1)
#ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1, sharex=ax1)
plt.xlabel('Date')
ax2v = ax2.twinx()

#Customize the grid
ax2.grid(True, color='k', linestyle='--', linewidth=0.5)  

#Rotate the axis ticklabels
for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45) 

#Format the dates in the label    
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d%h'))
labels = ax2.get_xticklabels()

#Plot candlestick chart in the figure and set title, xlabel and ylabel
candlestick_ohlc(ax2, ohlc, colorup='#77d879', colordown='#db3f3f', width = 1)
ax2.set_title(pair+'\n')
ax2.set_xlabel('Date')
ax2.set_ylabel('Price')

plt.show()