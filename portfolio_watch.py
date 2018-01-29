import sys

import argparse

import pandas as pd
import numpy as np

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--save", type=bool, help="Save portfolio", default=False)
parser.add_argument("--dust", help="Show dust", action='store_true')
option = parser.parse_args()
kucoin = 1

def get_original_buy_transactions(client,portfolio) :

	# For each trade in portflio, try to get origin
	symbols = portfolio.index.values

	res = pd.DataFrame()

	for s in symbols :

		# debug
		if s != 'VIBE' : continue

		print("Looking for [{}] buy orders".format(s))
		t = crypto.trades.get_all_trades(client,s)
		res = pd.concat([res,t])

	res = res.drop('id', 1)
	res = res.drop('orderId', 1)
	res = res.drop('symbol', 1)

	res['time'] = pd.to_datetime(res['time'], unit='ms')

	res =  res[(res['isBuyer'] == True )]
	res = res.drop('isBuyer', 1)
	res = res.drop('isBestMatch', 1)

	res.rename(columns={'qty':'quantity'}, inplace=True)
	res.rename(columns={'commissionAsset':'comAsset'}, inplace=True)
	res.rename(columns={'commission':'com'}, inplace=True)

	res['quantity'] = res['quantity'].apply(pd.to_numeric)
	res['price'] = res['price'].apply(pd.to_numeric)
	res['com'] = res['com'].apply(pd.to_numeric)

	# A quoi ca sert 'isMaker' ?
	# print(res)
	#print(res[['source','quantity','price','com','comAsset','time']])

	res = res[['source','quantity','price','time']]
	res.sort_values(by='time', inplace=True, ascending=False)
	#t['time'] = t.to_datetime(t['time'])
	print(res)
	# print(t.sort('time'))

	buy_price = []
	buy_symbol = []
	for s in symbols :
		# Debug
		if s != 'VIBE' : continue

		pf = portfolio.loc[portfolio.index == s]
		bag = float(pf.iloc[0]['quantity'])
		print('Looking for {0} units of {1}'.format(bag,s))

		value = 0
		b_symbol = '-'

		quantity = bag
		r = res.loc[res.index == s]
		print(r)
		for index, row in r.iterrows():
			b_qty = float(row['quantity'])
			b_price = float(row['price'])
			b_symbol = float(row['source'])
			if quantity > 0 :
				quantity = quantity - b_qty
				value += b_price * b_qty
				print('bought {0} at {1}'.format(b_qty,b_price))
		value = value / float(pf.iloc[0]['quantity'])
		print('Looking for {0} units of {1}'.format(bag,s))
		print('Bought value {0}'.format(value))
		buy_price.append(value)
		buy_symbol.append(b_symbol)


if __name__ == "__main__":

	
	# Try kucoin
	if(kucoin) : 
		client = crypto.utils.get_kucoin_client(option.params)
	else : 
		client = crypto.utils.get_binance_client(option.params)

	out_dir = crypto.utils.get_out_dir(option.params)

	# Get prices
	if(kucoin) :
		market_prices = crypto.market.get_market_prices_kucoin(client)
	else :
		market_prices = crypto.market.get_market_prices(client)

	# Get portfolio and add equivalent values
	if(kucoin) :
		portfolio = crypto.portfolio.get_portfolio_kucoin(client)
	else :
		portfolio = crypto.portfolio.get_portfolio(client)
	# Get active trading position
	if(kucoin == 0) :
		trades = crypto.trades.get_active_trades(client,market_prices)


	# add active trades to portfolio
	if(kucoin == 0) :
		portfolio = crypto.trades.add_active_trades_to_portfolio(portfolio, trades)

	# add current prices (eth, btc, usd)
	if(kucoin == 1) :
		portfolio = crypto.portfolio.add_market_prices_to_portfolio_kucoin(portfolio,market_prices)
	else :
		portfolio = crypto.portfolio.add_market_prices_to_portfolio(portfolio,market_prices)

	if option.dust :
		dust_limit = 0
	else :
		dust_limit = 5

	if(kucoin == 1) :
		crypto.portfolio.show_portfolio_kucoin(portfolio,dust_limit)
	else :
		crypto.portfolio.show_portfolio(portfolio,dust_limit)
	#crypto.trades.show_trades(trades)

	# In progress :
	#get_original_buy_transactions(client, portfolio)

	# depth = client.get_order_book(symbol='ETHBTC')
	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
	# print(candles)

	# add buy price for each
	# get_original_buy_transactions(client,portfolio)



