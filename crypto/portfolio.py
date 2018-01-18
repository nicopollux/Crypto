import pandas as pd
import numpy as np

def get_portfolio(client) :
	info = client.get_account()

	df = pd.DataFrame(info['balances'])
	df['free'] = df['free'].apply(pd.to_numeric)
	df = df.drop('locked', 1)
	df.columns = ['symbol', 'quantity']
	df.index =  df['symbol']
	df = df.drop('symbol', 1)

	return df[(df['quantity'] > 0 )]

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

def show_portfolio(portfolio) :

	print('\n---------- Portfolio ----')
	if 'eth' not in portfolio :
		portfolio['quantity'] = portfolio['quantity'].map(lambda x: '%2.3f' % x)
	else :
		portfolio['Percent'] = portfolio['eth']/ portfolio['eth'].sum()
		portfolio.loc['Total'] = portfolio.sum()

		portfolio['quantity'] = portfolio['quantity'].map(lambda x: '%2.3f' % x)
		portfolio['usd'] = portfolio['usd'].map(lambda x: '%2.2f' % x)

		portfolio['Percent'] = pd.Series(["{0:.0f}%".format(val * 100) for val in portfolio['Percent']], index = portfolio.index)

	print(portfolio)
