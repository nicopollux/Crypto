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

	# Compute table with all pairs values
	result = None
	for client in clients :
		name = crypto.utils.get_client_name(client)
		market_prices = crypto.market.get_market_prices(client)
		t = pd.DataFrame(list(market_prices.items()), columns=['pair', name])
		t[name] = t[name].apply(pd.to_numeric)

		if result is None :
			result = t
		else :
			result = pd.merge(result, t, on='pair', how='outer')

	# print(result.head(10))

	# Find maximum deltas between two platforms
	result['delta'] = ((result.max(axis=1) - result.min(axis=1)) / result.min(axis=1)) * 100
	result.sort_values(by='delta', inplace=True, ascending=False)
	result['delta'] = pd.Series(["{0:.0f}%".format(val) for val in result['delta']], index = result.index)

	# df = result[clients_list].max()
	print(result.head(10))

	# For first line get
	list_clients = []
	for client in clients :
		list_clients.append(crypto.utils.get_client_name(client))

	result['From'] = result[list_clients].idxmin(axis=1)
	result['To'] = result[list_clients].idxmax(axis=1)
	print(result.head(10))

	# Get get_deposit_address
	from_exchange = result['From'].iloc[0]
	to_exchange = result['To'].iloc[0]
	coin = result['pair'].iloc[0].split('-')[0]
	print('Transfer {0} from {1} to {2}'.format(coin,from_exchange,to_exchange))
	address = crypto.assets.get_deposit_address(to_exchange,coin)
	print('Transfer {0} from {1} to {2} (adrress {3})'.format(coin,from_exchange,to_exchange,address))

	# if option.loop > 0 :
	# 	while True :
	# 		market_prices = crypto.market.get_market_prices(client)
	# 		if option.save :
	# 			crypto.market.update_market_file(out_dir,market_prices)
	# 		print('Loop [ETHUSDT] {0}'.format(market_prices['ETHUSDT']))
	# 		time.sleep(option.loop)
	# else :
	# 	market_prices = crypto.market.get_market_prices(client)
	# 	print('[ETHUSDT] {0}'.format(market_prices['ETHUSDT']))


