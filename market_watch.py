import sys, os
import time, datetime
import argparse

import csv
import pandas as pd
import numpy as np

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--loop", type=int, help="Loop time in sec (0 one shot", default=0)
#parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: XVGBTC)", default='ALL')
option = parser.parse_args()

def percent_change(new_price: float, old_price: float) -> float:
	return (((new_price - old_price) / old_price) * 100)

def dateparse(time_in_secs):
	return datetime.datetime.fromtimestamp(int(time_in_secs)/1000).strftime('%H:%M:%S')

if __name__ == "__main__":

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	local_timestamp = crypto.utils.current_milli_time()
	binance_timestamp = client.get_server_time()['serverTime']
	server_lag = binance_timestamp - local_timestamp

	if option.loop > 0 :
		while True :
			market_prices = crypto.market.get_market_prices(client)
			crypto.market.update_market_file(out_dir,market_prices)
			time.sleep(option.loop)
			print('Loop [ETHUSDT] {0}'.format(market_prices['ETHUSDT']))
	else :
		market_prices = crypto.market.get_market_prices(client)
		print('[ETHUSDT] {0}'.format(market_prices['ETHUSDT']))


	# print(dateparse(local_timestamp))
	# print("Connected to binance with {} ms delay".format(server_lag))

	# sys.exit(1)
	# Get prices

	# Load last market file
	# history = load_market_history()
	# print(history)

	# Update market file

	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_3MINUTE)
	# print(candles)
	# Print prices

	# Save prices
	# for asset in market_prices :

