import os
import time

import csv

import crypto

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient
from poloniex import Poloniex as poloClient

# Return dictionary with pairs as index (ie ETH-BTC) and value.
# Pairs are in global format.
def get_market_prices(client) :
	market_prices = {}
	# market_prices['time'] = crypto.utils.dateparse(crypto.utils.current_milli_time())
	# print(market_prices['time'])

	if type(client) is binanceClient :
		prices = client.get_all_tickers()
		for price in prices :
			if price['symbol'] == '123456' : continue
			p = crypto.utils.rchop(price['symbol'])
			u = crypto.utils.unit(price['symbol'])
			market_prices[p+'-'+u] = float(price['price'])
			# print('[{0}] {1}'.format(price['symbol'],price['price']))

	elif type(client) is kucoinClient :
		prices = client.get_tick()
		for price in prices :
			market_prices[price['coinType']+'-'+price['coinTypePair']] = float(price['lastDealPrice'])

	elif type(client) is poloClient :
		prices = client.returnTicker()
		for price in prices :
			p = price.split('_')
			# print(p)
			market_prices[p[1]+'-'+p[0]] = float(prices[price]['last'])

	market_prices['ETH-ETH'] = 1
	market_prices['BTC-BTC'] = 1
	if 'ETH-BTC' in market_prices :
		market_prices['BTC-ETH'] = 1 / market_prices['ETH-BTC']
	elif 'BTC-ETH' in market_prices :
		market_prices['ETH-BTC'] = 1 / market_prices['BTC-ETH']

	if 'ETH-USDT' in market_prices :
		market_prices['USDT-ETH'] = 1 / market_prices['ETH-USDT']
	if 'BTC-USDT' in market_prices :
		market_prices['USDT-BTC'] = 1 / market_prices['BTC-USDT']

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
