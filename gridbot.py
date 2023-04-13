import ccxt, time, json
from datetime import datetime
import pandas as pd

exchange = ccxt.binance({
    'apiKey': 'bRaSz2tZ2Ui64BifEF0GdTYgCJtOlaw4Gd8CWNcYyGdvHnKCo92NywGJyg8Kx4RM',
    'secret': 'H9tTeSZoZvFM6vyMcROYdhgDHiawQC1tcu0XiuUshTnnJk6z97X0PXT0VM7eKgE6',
    'enableRateLimit': True,
})

markets = exchange.load_markets()

def get_balance():
    balance = exchange.fetch_balance()['free']
    for key in balance:
        if balance[key] > 0:
            print(key, balance[key])
    # return balance


def get_symbols():
    return exchange.symbols


def get_price(symbol):
    return exchange.fetch_ticker(symbol)['last']

def get_order_book(symbol):
    return exchange.fetch_order_book(symbol)

def get_trades(symbol):
    return exchange.fetch_trades(symbol)

def get_my_trades(symbol):
    return exchange.fetch_my_trades(symbol)

def get_usdt_symbols():
    return [symbol for symbol in exchange.symbols if 'USDT' in symbol]


if __name__ == "__main__":
    print(get_balance())
    # print(get_order_book('BTC/USDT'))
    # print(get_trades('BTC/USDT'))
    # print(get_my_trades('BTC/USDT'))
    # print(get_price('BTC/USDT'))
    # df = pd.DataFrame(get_trades('BTC/USDT'))
    usdt_symbols = get_usdt_symbols()
    prices = []
    binance_prices = {
        'usdt_symbols': usdt_symbols,
        'prices': prices
    }
    for symbol in usdt_symbols:
        price = get_price(symbol)
        prices.append(price)
        print(symbol, price )
    df = pd.DataFrame(binance_prices, columns=['symbol', 'price'])
    df.to_excel('binance_prices.xlsx')

    # print(get_symbols())
    print(get_price('BUSD/USDT'))

