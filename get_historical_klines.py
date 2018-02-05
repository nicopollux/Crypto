import os, time, sys
import argparse

from datetime import datetime, date, timedelta

import pandas as pd

import crypto

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--params", type=str, help="file.xml", required=True)
	parser.add_argument("--pair", type=str, help="Pair to trade (ie ETHBTC)", required=False)
	parser.add_argument("--exchange", type=str, help="platform (binance, kucoin, poloniex)", required=False)
	#parser.add_argument("--year", type=int, help="Year to check", required=True)
	option = parser.parse_args()

	clients = crypto.utils.get_clients(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	date_max = datetime.utcnow()

	for client in clients :
		if option.exchange is not None and option.exchange != crypto.utils.get_client_name(client) :
			continue

		list_pairs = {}
		if option.pair is None :
			list_pairs = crypto.utils.get_all_pairs(client)
		else :
			pairs_available = crypto.utils.get_all_pairs(client)
			if option.pair in pairs_available.keys() :
				list_pairs[option.pair] = pairs_available[option.pair]
			else :
				print('Pair {0} not available on {1}'.format(option.pair,crypto.utils.get_client_name(client)))

		if type(client) is binanceClient :
			# Binance opening : 14/07/2017
			date_original = datetime(2017, 7, 14)
		elif type(client) is kucoinClient :
			# Kucoin opening : 27/09/2017
			date_original = datetime(2017, 9, 27)
		elif type(client) is poloClient :
			# Dont know when opening but 01/01/2016 seems good.
			date_original = datetime(2016, 1, 1)
		# elif type(client) is bitfinexClient :
			# date_max = datetime(2015, 10, 1)
			# df = crypto.klines.get_historical_klines(client,'BTC_ETH',date_original,date_max)
			# print(df)

		# sys.exit(1)
		loop_timer = 0.5
		print ('{0} pairs found on {1}'.format(len(list_pairs),crypto.utils.get_client_name(client)))
		for pair in list_pairs :
			if type(client) is binanceClient :
				file = out_dir+'/history/binance/history_'+pair+".csv"
			elif type(client) is kucoinClient :
				file = out_dir+'/history/kucoin/history_'+pair+".csv"
			elif type(client) is poloClient :
				file = out_dir+'/history/poloniex/history_'+pair+".csv"

			# If file exists, complete
			if os.path.exists(file) :
				print('[{}] already found.. load and complete'.format(pair))
				resultat = pd.read_csv(file)
				resultat.index = resultat['time']
				resultat['time'] = resultat['time'].apply(pd.to_datetime)
				resultat = resultat.drop('time', 1)
				date = datetime.strptime(resultat.tail(1).index[0], '%Y-%m-%d %H:%M:%S')
			else :
				resultat = pd.DataFrame()
				date = date_original

			while date_max - date > timedelta(minutes = 5) :
				# print(date)
				# print(date_max)

				df = crypto.klines.get_historical_klines(client,list_pairs[pair],date,date_max)
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
