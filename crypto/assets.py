import crypto

def get_deposit_address(client,coin) :
	if type(client) is crypto.binanceClient :
		return client.get_deposit_address(asset=coin)['address']
	elif type(client) is crypto.kucoinClient :
		try :
			return client.get_deposit_address(coin)['address']
		except :
			return None

	return None

def get_withdrawal_fees(client,url) :
	return None

# infouser = client.get_user()
# Test if can withdraw
# print(infouser['credentialStatus'])
