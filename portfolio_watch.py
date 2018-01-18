import sys

import xml.etree.ElementTree as ET

from binance.client import Client

import pandas as pd
import numpy as np

def get_market_prices(client) :
	market_prices = {}
	prices = client.get_all_tickers()
	for price in prices :
		market_prices[price['symbol']] = float(price['price'])
		# print('[{0}] {1}'.format(price['symbol'],price['price']))

	market_prices['ETHETH'] = 1
	market_prices['BTCBTC'] = 1
	market_prices['BTCETH'] = 1 / market_prices['ETHBTC']
	market_prices['USDTETH'] = 1 / market_prices['ETHUSDT']
	market_prices['USDTBTC'] = 1 / market_prices['BTCUSDT']

	return market_prices

def get_portfolio(client) :
	info = client.get_account()

	df = pd.DataFrame(info['balances'])
	df['free'] = df['free'].apply(pd.to_numeric)
	df = df.drop('locked', 1)
	df.columns = ['symbol', 'quantity']
	df.index =  df['symbol']
	df = df.drop('symbol', 1)

	return df[(df['quantity'] > 0 )]

def add_values_to_portfolio(portfolio, market_prices) :
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

def rchop(thestring):
	if thestring.endswith('ETH') :
		return thestring[:-len('ETH')]
	elif thestring.endswith('BTC') :
		return thestring[:-len('BTC')]
	elif thestring.endswith('USDT') :
		return thestring[:-len('USDT')]
	else :
		return thestring

def unit(thestring):
	if thestring.endswith('ETH') :
		return 'ETH'
	elif thestring.endswith('BTC') :
		return 'BTC'
	elif thestring.endswith('USDT') :
		return 'USDT'
	else :
		return thestring

def add_active_trades_to_portfolio(portfolio, trades) :

	if trades.empty :
		return portfolio

	trades['clean'] = trades.index.map(lambda x: rchop(x))
	trades['unit'] = trades.index.map(lambda x: unit(x))

	# If we buy, we still have needed btc/eth/usdt
	# If we sell, we still have the alt
	trades['portfolio'] = np.where(trades['side']=='BUY', trades['unit'], trades['clean'])
	trades['amount'] = np.where(trades['side']=='BUY', trades['quantity']*trades['target'], trades['quantity'])

	df = trades[['portfolio','amount']]
	df.index = trades['portfolio']
	df = df.drop('portfolio', 1)

	df.rename(columns={'amount':'quantity'}, inplace=True)
	df['quantity'] = df['quantity'].apply(pd.to_numeric)
	portfolio['quantity'] = portfolio['quantity'].apply(pd.to_numeric)

	res = pd.concat([portfolio, df])
	res = res.groupby(res.index).sum()

	return res

def get_trades(client,s,source) :
	try :
		mytrades = client.get_my_trades(symbol=s+source)
		t = pd.DataFrame(mytrades)
		t['source'] = source
		t['symbol'] = s
		t.index = t['symbol']
		return t
	except :
		return pd.DataFrame()

def get_all_trades(client,symbol) :
	res = pd.DataFrame()
	for source in ['ETH','BTC','USDT'] :
		t = get_trades(client,symbol,source)
		if not t.empty :
			res = pd.concat([res,t])

	return res

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

def get_active_trades(client,market_prices) :
	trades = client.get_open_orders()

	if len(trades) == 0 :
		return pd.DataFrame()

	df = pd.DataFrame(trades)
	df = df.drop('clientOrderId', 1)
	df = df.drop('executedQty', 1)
	df = df.drop('icebergQty', 1)
	df = df.drop('isWorking', 1)
	df = df.drop('orderId', 1)
	df = df.drop('status', 1)
	df = df.drop('timeInForce', 1)
	df.index =  df['symbol']
	df = df.drop('symbol', 1)

	df.rename(columns={'origQty':'quantity'}, inplace=True)
	df.rename(columns={'price':'target'}, inplace=True)

	df['quantity'] = df['quantity'].apply(pd.to_numeric)
	df['target'] = df['target'].apply(pd.to_numeric)
	df['stopPrice'] = df['stopPrice'].apply(pd.to_numeric)

	df['time'] = pd.to_datetime(df['time'], unit='ms')

	actual_price = []
	for s in df.index.values :
		actual_price.append(market_prices[s])
	df['price'] = actual_price
	df['distance'] = df['target'] - df['price']
	return df

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

def show_trades(trades) :

	if trades.empty :
		print('\n---------- No Actives Trades ----')
		return

	print('\n---------- Active Trades ----')
	trades['quantity'] = trades['quantity'].map(lambda x: '%2.3f' % x)
	# portfolio.loc['Total'] = portfolio.sum()

	# remove stopPrice if not set
	if not 0 in trades['stopPrice'].values :
		print(trades[['quantity','target','price','stopPrice','side','type']])
		# print(trades[['quantity','target','price','distance','stopPrice','type','side']])
	else :
		# print(trades[['quantity','target','price','distance','type','side']])
		print(trades[['quantity','target','price','side','type']])

	# Remove column with only null values
	# trades.loc[:, (trades != 0).any(axis=0)]

if __name__ == "__main__":

	if len(sys.argv) < 2 :
		print(u"Please use # python {} settings.xml".format(sys.argv[0]))
		sys.exit(1)
	else :
		tree = ET.parse(sys.argv[1])
		settings = tree.getroot()

		for service in settings.findall('service') :
			if service.get("name") == "binance" :
				api_key = service.find("api_key").text
				api_secret = service.find("api_secret").text

	client = Client(api_key, api_secret)

	# Get prices
	market_prices = get_market_prices(client)

	# Get portfolio and add equivalent values
	portfolio = get_portfolio(client)

	# Get active trading position
	trades = get_active_trades(client,market_prices)

	# add active trades to portfolio
	portfolio = add_active_trades_to_portfolio(portfolio, trades)

	# add current prices (eth, btc, usd)
	portfolio = add_values_to_portfolio(portfolio,market_prices)

	show_portfolio(portfolio)
	show_trades(trades)

	# In progress :

	# depth = client.get_order_book(symbol='ETHBTC')
	# candles = client.get_klines(symbol='ETHBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
	# print(candles)

	# add buy price for each
	# get_original_buy_transactions(client,portfolio)



