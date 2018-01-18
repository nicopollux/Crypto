import sys

import argparse

import pandas as pd
import numpy as np

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--save", type=bool, help="Save portfolio", default=False)
option = parser.parse_args()

def get_original_buy_transactions(client,portfolio) :

	# For each trade in porteflio, try to get origin
	symbols = portfolio.index.values

	res = pd.DataFrame()

	for s in symbols :
		t = get_all_trades(client,s)
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
	print(res[['source','quantity','price','com','comAsset','time']])

	avg_val = []
	for s in symbols :
		print(s)
		pf = portfolio.loc[portfolio.index == s]
		quantity = float(pf.iloc[0]['quantity'])
		print('Looking for {0}'.format(quantity))


		value = 0
		r = res.loc[res.index == s]
		print(r)
		for index, row in r.iterrows():
			b_qty = float(row['quantity'])
			b_price = float(row['price'])
			if quantity > 0 :
				quantity = quantity - b_qty
				value += b_price*b_qty
				print('bought {0} at {1}'.format(b_qty,b_price))
		value = value / float(pf.iloc[0]['quantity'])
		print('average value {0}'.format(value))
		avg_val.append(value)

	# # Trade in eth
	# trade_eth = False
	# if asset_name+'ETH' in market_prices and len(trades_eth) > 0 :
	# 	asset_buy = float(trades_eth[len(trades_eth)-1]['price'])
	# 	asset_gain_eth = asset_balance * ( asset_eth - asset_buy )
	# 	trade_eth = True

	# # Trade in btc
	# trade_btc = False
	# if asset_name+'BTC' in market_prices and len(trades_btc) > 0 :
	# 	asset_buy = float(trades_btc[len(trades_btc)-1]['price'])
	# 	asset_gain_btc = asset_balance * ( asset_btc - asset_buy )
	# 	trade_btc = True



if __name__ == "__main__":

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	# Get prices
	market_prices = crypto.market.get_market_prices(client)

	# Get portfolio and add equivalent values
	portfolio = crypto.portfolio.get_portfolio(client)

	# Get active trading position
	trades = crypto.trades.get_active_trades(client,market_prices)

	# add active trades to portfolio
	portfolio = crypto.trades.add_active_trades_to_portfolio(portfolio, trades)

	# add current prices (eth, btc, usd)
	portfolio = crypto.portfolio.add_market_prices_to_portfolio(portfolio,market_prices)

	crypto.portfolio.show_portfolio(portfolio)
	crypto.trades.show_trades(trades)

	# In progress :

	# depth = client.get_order_book(symbol='ETHBTC')
	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
	# print(candles)

	# add buy price for each
	# get_original_buy_transactions(client,portfolio)



