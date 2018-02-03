import os
import time, datetime

import xml.etree.ElementTree as ET

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient

def percent_change(old_price, new_price) :
	return (((new_price - old_price) / old_price) * 100)

def get_clients(file) :
	clients = []
	tree = ET.parse(file)
	settings = tree.getroot()

	for service in settings.findall('service') :
		client = None
		name = service.get("name")

		if service.get("name") == "binance" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text
			client = binanceClient(api_key, api_secret)
		elif service.get("name") == "kucoin" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text
			client = kucoinClient(api_key, api_secret)
			print(client)

		if verify_time(client) :
			clients.append(client)
		else :
			print('Client {} not available'.format(name))

	return clients

def get_ethereum_balances(file) :
	balances = {}
	tree = ET.parse(file)
	settings = tree.getroot()

	for service in settings.findall('service') :
		if service.get("name") == "etherscan" :
			api_key = service.find("api_key").text
			for wallet in service.findall('addresses') :
				print(wallet)
				# ad = account.get('add').text
				# print(ad)

def get_out_dir(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	out_dir = settings.find('output').text
	if not os.path.exists(out_dir): os.makedirs(out_dir)
	if not os.path.exists(out_dir+'/market'): os.makedirs(out_dir+'/market')
	return out_dir


# Time
current_milli_time = lambda: int(round(time.time() * 1000))

def dateparse(time_in_secs):
	return datetime.datetime.fromtimestamp(int(time_in_secs)/1000).strftime('%d/%m/%Y %H:%M:%S')

def convert_to_paris_time(client,row):
    return pd.to_datetime(row.datetime_local).tz_convert('Europe/Paris')

def verify_time(client) :
	if not client :
		return False

	if type(client) is binanceClient :
		timestamp = client.get_server_time()['serverTime']
	elif type(client) is kucoinClient :
		currencies = client.get_currencies()
		print(currencies)
		timestamp = client.get_last_timestamp()
		print(timestamp)
		# no output here ! Fake timestamp for now
		timestamp = 1517501261679

	if not timestamp :
		return False

	time_ser = int(int(timestamp)/1000)
	time_loc = int(time.time())

	# print(time_ser)
	# print(time_loc)

	dtime_ser = datetime.datetime.fromtimestamp(time_ser).strftime('%Y-%m-%d %H:%M:%S')
	dtime_loc = datetime.datetime.fromtimestamp(time_loc).strftime('%Y-%m-%d %H:%M:%S')
	# print('Server time is {0}ms {1}'.format(time_ser, dtime_ser))
	# print(' Local time is {0}ms {1}'.format(time_loc, dtime_loc))
	# print(' Delta is {}'.format(time_loc-time_ser))
	if time_loc - time_ser < 1000 :
		return True
