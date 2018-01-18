import os
import time

import xml.etree.ElementTree as ET

from binance.client import Client

# Time
current_milli_time = lambda: int(round(time.time() * 1000))

def get_binance_client(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	for service in settings.findall('service') :
		if service.get("name") == "binance" :
			api_key = service.find("api_key").text
			api_secret = service.find("api_secret").text

	return Client(api_key, api_secret)

def get_out_dir(file) :
	tree = ET.parse(file)
	settings = tree.getroot()

	out_dir = settings.find('output').text
	if not os.path.exists(out_dir): os.makedirs(out_dir)
	if not os.path.exists(out_dir+'/market'): os.makedirs(out_dir+'/market')
	return out_dir+'/market'
