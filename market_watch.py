import sys, os

import time, datetime

import csv
import pandas as pd
import numpy as np

import crypto

def percent_change(new_price: float, old_price: float) -> float:
	return (((new_price - old_price) / old_price) * 100)

def dateparse(time_in_secs):
	return datetime.datetime.fromtimestamp(int(time_in_secs)/1000).strftime('%H:%M:%S')

if __name__ == "__main__":

	if len(sys.argv) < 2 :
		print(u"Please use # python {} settings.xml".format(sys.argv[0] ))
		sys.exit(1)
	else :
		client = crypto.utils.get_binance_client(sys.argv[1])
		out_dir = crypto.utils.get_out_dir(sys.argv[1])

	local_timestamp = crypto.utils.current_milli_time()
	binance_timestamp = client.get_server_time()['serverTime']
	server_lag = binance_timestamp - local_timestamp
	# print(dateparse(local_timestamp))
	# print("Connected to binance with {} ms delay".format(server_lag))

	# sys.exit(1)
	# Get prices
	market_prices = crypto.market.get_market_prices(client)
	print('[ETHUSDT] {0}'.format(market_prices['ETHUSDT']))

	# Load last market file
	# history = load_market_history()
	# print(history)

	# Update market file
	crypto.market.update_market_file(out_dir,market_prices)

	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_3MINUTE)
	# print(candles)
	# Print prices

	# Save prices
	# for asset in market_prices :

