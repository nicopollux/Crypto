import time
import calendar

import pandas as pd
import numpy as np

from datetime import datetime, date

import crypto

from binance.client import Client

# Get Historical data (for training model use) :
# pair can be 'NEOBTC'
# when should be a date string DD/MM/YYYY
# Warning : We stay in UTC !!

def get_historical_klines(client, pair, day) :
	timestamp = int(time.mktime(day.timetuple())) * 1000
	# print(timestamp)
	klines = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_5MINUTE, startTime=timestamp)
	return format_klines(pd.DataFrame(klines))

def get_klines(pair) :
	klines = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1MINUTE)
	return format_klines(pd.DataFrame(klines))

# Return time is in Paris time
def format_klines(df) :
	df.columns = ['Open time', 'Open', 'High','Low','Close','Volume','Close time','Quote asse volume','Number of trades','Taker base','Taker quote','Ignore']
	df = df.drop('Quote asse volume', 1)
	df = df.drop('Number of trades', 1)
	df = df.drop('Taker base', 1)
	df = df.drop('Taker quote', 1)
	df = df.drop('Ignore', 1)
	df = df.drop('Close time', 1)

	# Sort with last in first
	df.sort_values(by='Open time', inplace=True, ascending=True)

	# Remove lines without transfer
	df['Volume'] = df['Volume'].apply(pd.to_numeric)
	df = df[(df['Volume'] > 0 )]

	# Convert unix timestamp (ms) to UTC date
	df['time'] = pd.to_datetime(df['Open time'], unit='ms')
	df = df.drop('Open time', 1)

	df.index =  df['time']
	df = df.drop('time', 1)

	df['Open'] = df['Open'].apply(pd.to_numeric)
	df['High'] = df['High'].apply(pd.to_numeric)
	df['Low'] = df['Low'].apply(pd.to_numeric)
	df['Close'] = df['Close'].apply(pd.to_numeric)

	return df

def show_klines(df) :
	df = format_klines(df)

	df['time'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('Europe/Paris').apply(lambda x: x.strftime('%d/%m/%Y %H:%M'))
	# Compute change
	df['Open'] = df['Open'].apply(pd.to_numeric)
	df['Close'] = df['Close'].apply(pd.to_numeric)
	df['change'] = crypto.utils.percent_change(df['Open'],df['Close'])

	return df
