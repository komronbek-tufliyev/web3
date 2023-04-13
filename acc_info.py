import web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *

from datetime import datetime
from config import config

web3 = web3.Web3(web3.HTTPProvider(config['provider']))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(web3.is_connected())

wallet_address = web3.to_checksum_address(config['wallet_address']) # check wallet addres to metamask or not
private_key = config['private_key']


def get_account_info():
    balance = web3.eth.get_balance(wallet_address)
    print('Balance: ', web3.from_wei(balance, 'ether'), 'BNB')
    print('Wallet address: ', wallet_address)
    print('Private key: ', private_key)
    # print(web3.eth.)


print('Account info: ', get_account_info())


