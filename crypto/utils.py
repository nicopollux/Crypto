import os
import time, datetime

import xml.etree.ElementTree as ET

from binance.client import Client as binanceClient

# Time
current_milli_time = lambda: int(round(time.time() * 1000))

def dateparse(time_in_secs):
	return datetime.datetime.fromtimestamp(int(time_in_secs)/1000).strftime('%d/%m/%Y %H:%M:%S')

def convert_to_paris_time(client,row):
    return pd.to_datetime(row.datetime_local).tz_convert('Europe/Paris')

# Misc

def percent_change(old_price, new_price) :
	return (((new_price - old_price) / old_price) * 100)

def get_binance_client(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	for service in settings.findall('service') :
		if service.get("name") == "binance" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text

	return binanceClient(api_key, api_secret)

# def get_kucoin_client(file) :
# 	tree = ET.parse(file)
# 	settings = tree.getroot()

# 	for service in settings.findall('service') :
# 		if service.get("name") == "kucoin" :
# 			api_key = service.find("api_key").text
# 			api_secret = service.find("api_secret").text

# 	return Client(api_key, api_secret)

def get_out_dir(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	out_dir = settings.find('output').text
	if not os.path.exists(out_dir): os.makedirs(out_dir)
	if not os.path.exists(out_dir+'/market'): os.makedirs(out_dir+'/market')
	return out_dir
