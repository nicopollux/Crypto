import time

import argparse
import pandas as pd
import numpy as np


import crypto

from binance.client import Client

parser = argparse.ArgumentParser()
parser.add_argument("--params", type=str, help="file.xml", required=True)
parser.add_argument("--pair", type=str, help="Pair to trade", required=True)
option = parser.parse_args()


if __name__ == "__main__":

	client = crypto.utils.get_binance_client(option.params)
	out_dir = crypto.utils.get_out_dir(option.params)

	loop_timer = 10

	# while True :
	crypto.klines.get_klines(client,option.pair)

		# time.sleep(loop_timer)

