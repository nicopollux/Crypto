import os, time
import argparse

from datetime import datetime, date, timedelta

import pandas as pd

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--pair", type=str, help="Pair to trade (ALL for all)", required=True)
#parser.add_argument("--year", type=int, help="Year to check", required=True)
option = parser.parse_args()

if __name__ == "__main__":

	clients = crypto.utils.get_clients(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	# binance only
	client = None
	for c in clients :
		if type(c) is binanceClient :
			client = c

	if client is None :
		sys.exit(1)

	list_pairs = []
	if option.pair == 'ALL' :
		prices = client.get_all_tickers()
		for price in prices :
			if price['symbol'] == '123456' : continue
			list_pairs.append(price['symbol'])
	else :
		list_pairs.append(option.pair)

	# Binance opening : 14/07/2017
	date_original = datetime(2017, 7, 14)
	date_max = datetime.utcnow()

	loop_timer = 0.5
	for pair in list_pairs :
		file = out_dir+'/history_'+pair+".csv"

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
			print(date)
			print(date_max)

			df = crypto.klines.get_historical_klines(client,pair,date)
			last_date = df.tail(1).index[0]
			date = last_date
			print('[{0}] Getting {1}'.format(pair,date))
			resultat = pd.concat([resultat, df])

			time.sleep(loop_timer)

		resultat.to_csv(file)





