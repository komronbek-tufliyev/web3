import ccxt
from datetime import datetime

start = datetime.now()

binance = ccxt.binance({
    'apiKey': 'bRaSz2tZ2Ui64BifEF0GdTYgCJtOlaw4Gd8CWNcYyGdvHnKCo92NywGJyg8Kx4RM',
    'secret': 'H9tTeSZoZvFM6vyMcROYdhgDHiawQC1tcu0XiuUshTnnJk6z97X0PXT0VM7eKgE6',
    'enableRateLimit': True,

})
binance.load_markets()

def get_balance():
    balance = binance.fetch_balance()['free']
    for key in balance:
        if balance[key] > 0:
            print(key, balance[key])
    # return balance

print(get_balance())
