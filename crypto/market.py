import os
import time

import csv

import crypto

def get_market_prices(client) :
	market_prices = {}
	market_prices['time'] = crypto.utils.current_milli_time()

	prices = client.get_all_tickers()
	# print(prices)
	for price in prices :
		market_prices[price['symbol']] = float(price['price'])

	return market_prices

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
