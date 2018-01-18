import sys, os

import time, datetime

import csv
import pandas as pd
import numpy as np

import xml.etree.ElementTree as ET

from binance.client import Client

def get_binance_client(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	for service in settings.findall('service') :
		if service.get("name") == "binance" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text

	return Client(api_key, api_secret)

def get_out_dir(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	out_dir = settings.find('output').text
	if not os.path.exists(out_dir): os.makedirs(out_dir)
	if not os.path.exists(out_dir+'/market'): os.makedirs(out_dir+'/market')
	return out_dir+'/market'

def get_market_prices(client) :
	market_prices = {}
	market_prices['time'] = current_milli_time()

	prices = client.get_all_tickers()
	# print(prices)
	for price in prices :
		market_prices[price['symbol']] = float(price['price'])

	return market_prices

def percent_change(new_price: float, old_price: float) -> float:
	return (((new_price - old_price) / old_price) * 100)

def load_market_history() :
	file = 'market_'+time.strftime("%Y%m%d")+".csv"
	return pd.read_csv(file, parse_dates=True, date_parser=dateparse, index_col=[0])

def update_market_file(dir,market) :
	file = dir+'/market_'+time.strftime("%Y%m%d")+".csv"

	file_exists = os.path.exists(file)

	with open(file,'a') as f:
		w = csv.DictWriter(f, market.keys())
		if not file_exists :
			w.writeheader()
		w.writerow(market)

# Time

current_milli_time = lambda: int(round(time.time() * 1000))

def dateparse(time_in_secs):
	return datetime.datetime.fromtimestamp(int(time_in_secs)/1000).strftime('%H:%M:%S')

if __name__ == "__main__":

	if len(sys.argv) < 2 :
		print(u"Please use # python marketwatch.py settings.xml")
		sys.exit(1)
	else :
		client = get_binance_client(sys.argv[1])
		out_dir = get_out_dir(sys.argv[1])

	local_timestamp = current_milli_time()
	binance_timestamp = client.get_server_time()['serverTime']
	server_lag = binance_timestamp - local_timestamp
	# print(dateparse(local_timestamp))
	# print("Connected to binance with {} ms delay".format(server_lag))

	# sys.exit(1)
	# Get prices
	market_prices = get_market_prices(client)

	print('[ETHUSDT] {0}'.format(market_prices['ETHUSDT']))

	# Load last market file
	# history = load_market_history()
	# print(history)

	# Update market file
	update_market_file(out_dir,market_prices)

	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_3MINUTE)
	# print(candles)
	# Print prices

	# Save prices
	# for asset in market_prices :

