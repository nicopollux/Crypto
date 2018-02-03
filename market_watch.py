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

	# clients_list = []
	# for client in clients :
	# 	name = crypto.utils.get_client_name(client)
	# 	print(name)
	# 	clients_list.append(name)

	# df = pd.DataFrame(columns=clients_list)
	# print(df)

	result = None
	for client in clients :
		name = crypto.utils.get_client_name(client)
		market_prices = crypto.market.get_market_prices(client)
		t = pd.DataFrame(list(market_prices.items()), columns=['pair', name])
		if result is None :
			result = t
		else :
			result = pd.merge(result, t, on='pair', how='outer')

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


