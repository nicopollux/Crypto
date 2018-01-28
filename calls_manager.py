import argparse

import crypto

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--loop", type=int, help="Loop time in sec (0 one shot)", default=0)
option = parser.parse_args()

if __name__ == "__main__":

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	# Call :
	# buy under value
	# sell objectifs : [value;amount]
	#crypto.calls.addcall('ETHBTC','')
