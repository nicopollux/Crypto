import os, time, sys
import argparse

from datetime import datetime, date, timedelta

import pandas as pd

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--pair", type=str, help="Pair to trade (ALL for all)", required=True)
# parser.add_argument("--exchange", type=str, help="platform (binance or kucoin)", required=False)
#parser.add_argument("--year", type=int, help="Year to check", required=True)
option = parser.parse_args()

if __name__ == "__main__":

	clients = crypto.utils.get_clients(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	date_max = datetime.utcnow()

	for client in clients :
		list_pairs = []
		if option.pair == 'ALL' :
			list_pairs = crypto.utils.get_all_pairs(client)
		else :
			pairs_available = crypto.utils.get_all_pairs(client)
			if option.pair in pairs_available :
				list_pairs.append(option.pair)
			else :
				print('Pair {0} not available on {1}'.format(option.pair,client))
		# print(list_pairs)

		if type(client) is binanceClient :
			# Binance opening : 14/07/2017
			date_original = datetime(2017, 7, 14)
		elif type(client) is kucoinClient :
			# Kucoin opening : 27/09/2017
			date = datetime(2017, 9, 27)
			# df = crypto.klines.get_historical_klines(client,pair,date,date_max)
			# print(df)

		loop_timer = 0.5
		for pair in list_pairs :
			if type(client) is binanceClient :
				file = out_dir+'/binance_history_'+pair+".csv"
			elif type(client) is kucoinClient :
				file = out_dir+'/kucoin_history_'+pair+".csv"

			# If file exists, complete
			if os.path.exists(file) :
				print('[{}] already found.. load and complete'.format(pair))
				resultat = pd.read_csv(file)
				resultat.index = resultat['time']
				resultat['time'] = resultat['time'].apply(pd.to_datetime)
				resultat = resultat.drop('time', 1)
				date = datetime.strptime(resultat.tail(1).index[0], '%Y-%m-%d %H:%M:%S')

			# If not, get all history
			else :
				resultat = pd.DataFrame()
				date = date_original

			while date_max - date > timedelta(minutes = 5) :
				# print(date)
				# print(date_max)

				df = crypto.klines.get_historical_klines(client,pair,date,date_max)
				last_date = df.tail(1).index[0]
				print('[{0}] Updated from {1} to {2}'.format(pair,date,last_date))

				# End of list
				if date == last_date :
					break
				else :
					date = last_date
				resultat = pd.concat([resultat, df])

				time.sleep(loop_timer)

			resultat.to_csv(file)





