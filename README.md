# Crypto
Crypto and Altcoins stuff

Some python code dedicated to Altcoins.

## General

Based on python-binance api - https://github.com/sammchardy/python-binance

- Generate API credits using https://www.binance.com/userCenter/createApi.html
('Read info' parameter is enough for that)
- Add API credits in example.xml file and rename it to something else.
- Install dependancies : `pip install python-binance`

## Portfolio

Show a status of your finance portfolio in real-time, with pending transactions

- Launch : `python portfolio_watch.py yourfile.xml`

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

Record Binance market price in a csv file for further analysis

- Update output line in your conf file
- Launch : `python market_watch.py yourfile.xml`

