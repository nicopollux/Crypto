import os
import time, datetime

import xml.etree.ElementTree as ET

from binance.client import Client as binanceClient
from kucoin.client import Client as kucoinClient

# Time
current_milli_time = lambda: int(round(time.time() * 1000))

def dateparse(time_in_secs):
	return datetime.datetime.fromtimestamp(int(time_in_secs)/1000).strftime('%d/%m/%Y %H:%M:%S')

def convert_to_paris_time(client,row):
    return pd.to_datetime(row.datetime_local).tz_convert('Europe/Paris')

def percent_change(old_price, new_price) :
	return (((new_price - old_price) / old_price) * 100)

def get_clients(file) :

	clients = []
	tree = ET.parse(file)
	settings = tree.getroot()

	for service in settings.findall('service') :
		if service.get("name") == "binance" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text
			clients.append(binanceClient(api_key, api_secret))
		if service.get("name") == "kucoin" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text
			clients.append(kucoinClient(api_key, api_secret))

	return clients

def get_out_dir(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	out_dir = settings.find('output').text
	if not os.path.exists(out_dir): os.makedirs(out_dir)
	if not os.path.exists(out_dir+'/market'): os.makedirs(out_dir+'/market')
	return out_dir
