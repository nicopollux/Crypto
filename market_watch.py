import sys, os
import time
import argparse

import csv
import pandas as pd
import numpy as np

import crypto

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--params", type=str, help="file.xml", required=True)
	parser.add_argument("--loop", type=int, help="Loop time in sec (0 one shot)", default=0)
	parser.add_argument("--save", type=bool, help="Write file True/False", default=False)
	#parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: XVGBTC)", default='ALL')
	option = parser.parse_args()

	clients = crypto.utils.get_clients(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	# binance only
	client = None
	for c in clients :
		if type(c) is binanceClient :
			client = c

	if client is None :
		sys.exit(1)

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

