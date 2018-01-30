import pandas as pd
import numpy as np

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient

def get_portfolio(client) :

	if type(client) is binanceClient :
		info = client.get_account()
		df = pd.DataFrame(info['balances'])
		df['free'] = df['free'].apply(pd.to_numeric)
		df = df.drop('locked', 1)
		df.columns = ['symbol', 'quantity']

	elif type(client) is binanceClient :
		df = pd.DataFrame(info)
		df = df.drop(['freezeBalance','balanceStr', 'freezeBalanceStr'],1)
		df.columns = ['quantity', 'symbol']

	df.index =  df['symbol']
	df = df.drop('symbol', 1)

	return df[(df['quantity'] > 0)]

def add_market_prices_to_portfolio(portfolio, market_prices) :
	portfolio_eth = []
	portfolio_btc = []

	portfolio['quantity'] = portfolio['quantity'].apply(pd.to_numeric)

	for s in portfolio.index.values :
		if s+'ETH' in market_prices :
			portfolio_eth.append(market_prices[s+'ETH'])
		else :
			portfolio_eth.append(market_prices[s+'BTC']/market_prices['ETHBTC'])
		if s+'BTC' in market_prices :
			portfolio_btc.append(market_prices[s+'BTC'])


	portfolio['eth'] = portfolio['quantity'] * portfolio_eth
	portfolio['btc'] = portfolio['quantity'] * portfolio_btc
	portfolio['usd'] = portfolio['eth'] * market_prices['ETHUSDT']

	return portfolio

# def add_market_prices_to_portfolio_kucoin(portfolio, market_prices) :

# 	portfolio_usd = []
# 	portfolio_btc = []

# 	portfolio['quantity'] = portfolio['quantity'].apply(pd.to_numeric)

# 	for s in portfolio.index.values :
# 		if s in market_prices :
# 			portfolio_usd.append(market_prices[s])
# 			portfolio_btc.append(market_prices[s]/market_prices['BTC'])


# 	portfolio['btc'] = portfolio['quantity'] * portfolio_btc
# 	portfolio['usd'] = portfolio['quantity'] * portfolio_usd

# 	return portfolio

def show_portfolio(portfolio,dust) :

	print('\n---------- Portfolio ----')
	if 'eth' not in portfolio :
		portfolio['quantity'] = portfolio['quantity'].map(lambda x: '%2.3f' % x)
	else :
		portfolio['Percent'] = portfolio['eth']/ portfolio['eth'].sum()
		portfolio.loc['Total'] = portfolio.sum()

		portfolio['quantity'] = portfolio['quantity'].map(lambda x: '%2.3f' % x)
		portfolio['usd'] = portfolio['usd'].map(lambda x: '%2.2f' % x)
		portfolio['usd'] = portfolio['usd'].apply(pd.to_numeric)

		portfolio['Percent'] = pd.Series(["{0:.0f}%".format(val * 100) for val in portfolio['Percent']], index = portfolio.index)

	print(portfolio[(portfolio['usd'] > dust)])

# def show_portfolio_kucoin(portfolio,dust) :

# 	print('\n---------- Portfolio ----')
# 	#portfolio['quantity'] = portfolio['quantity'].map(lambda x: '%2.3f' % x)
# 	portfolio.loc['Total'] = portfolio.sum()
# 	# portfolio['Percent'] = pd.Series(["{0:.0f}%".format(val * 100) for val in portfolio['Percent']], index = portfolio.index)
# 	print(portfolio)
