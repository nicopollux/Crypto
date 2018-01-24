import time
import argparse

from datetime import datetime, date

import pandas as pd

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--pair", type=str, help="Pair to trade (ALL for all)", required=True)
parser.add_argument("--year", type=int, help="Year to check", required=True)
option = parser.parse_args()

if __name__ == "__main__":

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	list_pairs = []
	if option.pair == ALL :
		prices = client.get_all_tickers()
		for price in prices :
			list_pairs.append(price['symbol'])
	else :
		list_pairs.append(option.pair)

	resultat = pd.DataFrame()
	date = datetime(option.year, 1, 1)
	date_max = datetime(option.year, 12, 31)

	loop_timer = 0.5
	for pair in list_pairs :
		while date < date_max :
			df = crypto.klines.get_historical_klines(client,pair,date)
			last_date = df.tail(1).index[0]
			date = last_date
			print('[{0}] {1}'.format(pair,date))
			resultat = pd.concat([resultat, df])

			time.sleep(loop_timer)

		file = out_dir+'/klines_'+option.pair+'_'+".csv"
		resultat.to_csv(file)





