import time
import argparse

from datetime import datetime, date

import pandas as pd

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--pair", type=str, help="Pair to trade", required=True)
parser.add_argument("--year", type=int, help="Year to check", required=True)
option = parser.parse_args()

if __name__ == "__main__":

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	loop_timer = 0.5

	resultat = pd.DataFrame()

	date = datetime(option.year, 1, 1)
	date_max = datetime(option.year, 12, 31)

	while date < date_max :
		df = crypto.klines.get_historical_klines(client,option.pair,date)
		last_date = df.tail(1).index[0]
		date = last_date
		print(date)
		resultat = pd.concat([resultat, df])

		time.sleep(loop_timer)


	file = out_dir+'/klines_'+option.pair+'_'+str(option.year)+".csv"
	resultat.to_csv(file)





