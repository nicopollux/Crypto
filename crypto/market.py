import os
import time

import csv

import crypto

def get_market_prices(client) :
	market_prices = {}
	market_prices['time'] = crypto.utils.dateparse(crypto.utils.current_milli_time())
	print(market_prices['time'])

	prices = client.get_all_tickers()
	for price in prices :
		if price['symbol'] == '123456' : continue
		market_prices[price['symbol']] = float(price['price'])
		# print('[{0}] {1}'.format(price['symbol'],price['price']))

	market_prices['ETHETH'] = 1
	market_prices['BTCBTC'] = 1
	market_prices['BTCETH'] = 1 / market_prices['ETHBTC']
	market_prices['USDTETH'] = 1 / market_prices['ETHUSDT']
	market_prices['USDTBTC'] = 1 / market_prices['BTCUSDT']

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
