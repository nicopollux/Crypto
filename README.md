# Crypto
Crypto and Altcoins stuff

Some python code dedicated to Altcoins.

## General

Based on python-binance api - https://github.com/sammchardy/python-binance

- Generate API credits using https://www.binance.com/userCenter/createApi.html
('Read info' parameter is enough for that)
- Add API credits in example.xml file and rename it to something else.
- Install dependancies :
`pip install -r requirements.txt`

## Portfolio

Show a status of your finance portfolio in real-time, with pending transactions

- Launch : `python portfolio_watch.py --params ../crypto.xml`
To see dust assets (< 5 usd), use --dust`

```
    ---------- Portfolio ----
          quantity       eth       btc     usd Percent
    BNB      0.869  0.012123  0.001111   12.64      2%
    BTC      0.016  0.172864  0.015832  180.25     22%
    ...

    ---------- Active Trades ----
           quantity    target     price  side   type
    symbol
    OMGBTC    2.500  0.001915  0.001613  SELL  LIMIT
    ...

```

## Market watch

Record Binance real time market price in a csv file for further analysis

- Update output line in your conf file
- Launch : `python market_watch.py --params ../crypto.xml --loop 10`
- File is updated every 10sec

# Market history

Record Binance 5 minutes candles for further analysis (and model training)
On first launch, save historical data since Binance opening (14/07/2017)
Relaunch and update since last time

- Launch : `python get_historical_klines.py --params ../crypto.xml --pair ETHBTC`

Can launch with 'ALL' for every pair available (300Mb data).

```
$ head -n 3 crypto/history_BNBBTC.csv
time,Open,High,Low,Close,Volume
2017-07-14 04:00:00,5e-05,5.3e-05,1e-05,3.615e-05,1469912.0
2017-07-14 04:05:00,3.9e-05,4e-05,3.655e-05,4e-05,1031546.0
```
