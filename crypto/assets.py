import crypto

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient
from poloniex import Poloniex as poloClient

def get_deposit_address(client,coin) :
	if type(client) is binanceClient or client == 'binance' :
		return binanceClient.get_deposit_address(asset=coin)
	elif type(client) is kucoinClient or client == 'kucoin':
		print(coin)
		return kucoinClient.get_deposit_address(coin)

