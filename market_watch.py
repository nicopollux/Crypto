import sys, os
import time
import argparse

import csv
import pandas as pd
import numpy as np

import crypto

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--params", type=str, help="file.xml", required=True)
	parser.add_argument("--loop", type=int, help="Loop time in sec (0 one shot)", default=0)
	parser.add_argument("--save", type=bool, help="Write file True/False", default=False)
	#parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: XVGBTC)", default='ALL')
	option = parser.parse_args()

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	local_timestamp = crypto.utils.current_milli_time()
	binance_timestamp = client.get_server_time()['serverTime']
	server_lag = binance_timestamp - local_timestamp

	if option.loop > 0 :
		while True :
			market_prices = crypto.market.get_market_prices(client)
			if option.save :
				crypto.market.update_market_file(out_dir,market_prices)
			print('Loop [ETHUSDT] {0}'.format(market_prices['ETHUSDT']))
			time.sleep(option.loop)
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

