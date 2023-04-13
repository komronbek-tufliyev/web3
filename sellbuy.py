from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *
import abis


provider = "https://bsc-dataseed.binance.org"
web3 = Web3(Web3.HTTPProvider(provider))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


class Sniper:
    def __init__(self, wallet_address, private_key, token_to_buy, token_to_sell, takeprofit, stoploss, liquidity, gas_limit, gas_price):
        self.wallet_address = web3.toChecksumAddress(wallet_address)
        self.private_key = private_key
        self.token_to_buy = web3.toChecksumAddress(token_to_buy)
        self.token_to_sell = web3.toChecksumAddress(token_to_sell)
        self.spend = token_to_sell
        self.takeprofit = takeprofit
        self.stoploss = stoploss
        self.liquidity = liquidity
        self.gas_limit = gas_limit
        self.gas_price = gas_price
        self.is_auto_buy_sell = False
        self.buy_amount = 0
        self.sell_amount = 0
        self.contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
        self.contract_sell = web3.eth.contract(address=self.token_to_sell, abi=abis.sellAbi)

    def calculate_profit(self):
        self.profit = 0

    def estimate_gas(self, txn, web3):
        self.gas = web3.eth.estimateGas(
            {
                "from": txn["from"],
                "to": txn["to"],
                "value": txn["value"],
                "data": txn["data"]
            }
        )
        self.gas = self.gas + (self.gas / 10)
        return self.gas

    def buy(self):
        logs = {
            'wallet_address': self.wallet_address,
            'private_key': self.private_key,
            'buy_token': self.token_to_buy,
            'sell_token': self.token_to_sell,
            'amount': self.buy_amount,
            'gas_limit': self.gas_limit,
            'gas_price': self.gas_price,
            'profit_percent': self.takeprofit,
            'stop_loss_percent': self.stoploss,
            'buy_auto_sell': self.is_auto_buy_sell,
        }
        print(logs)


