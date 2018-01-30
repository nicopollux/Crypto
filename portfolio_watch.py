import sys

import argparse

import pandas as pd
import numpy as np

import crypto

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--params", type=str, help="file.xml", required=True)
	parser.add_argument("--save", type=bool, help="Save portfolio", default=False)
	parser.add_argument("--dust", help="Show dust", action='store_true')
	option = parser.parse_args()

	clients = crypto.utils.get_clients(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	for client in clients :
		print(type(client))

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

		if option.dust :
			dust_limit = 0
		else :
			dust_limit = 5

		crypto.portfolio.show_portfolio(portfolio,dust_limit)
		crypto.trades.show_trades(trades)

	# In progress :
	#get_original_buy_transactions(client, portfolio)

	# depth = client.get_order_book(symbol='ETHBTC')
	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
	# print(candles)

	# add buy price for each
	# get_original_buy_transactions(client,portfolio)



