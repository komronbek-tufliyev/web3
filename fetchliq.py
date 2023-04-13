from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *
from config import config
import abis

web3 = Web3(Web3.HTTPProvider(config['provider']))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(web3.isConnected())


token_to_sell = web3.toChecksumAddress(config['busd'])
spend = web3.toChecksumAddress(config['wbnb'])
token_to_buy = spend

wallet_address = web3.toChecksumAddress(config['wallet_address'])


# CONTRACT TO BUY
contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
    # CONTRACT TO SELL
contract_sell = web3.eth.contract(address=abis.pancakeswap_factory, abi=abis.sellAbi)
    # Token Contract Sell
    # SellTokenContract = web3.eth.contract(address=token_to_sell, abi=abis.sellAbi)
contract = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)

sellTokenContract = web3.eth.contract(address=token_to_sell, abi=abis.sellAbi)
liq = sellTokenContract.functions.getReserves().call()
print(f"Liqduity in BNB: {liq}")
    # Get token balance
balance = sellTokenContract.functions.balanceOf(wallet_address).call()
print(f"Balance: {balance}")
symbol = sellTokenContract.functions.symbol().call()
readable = web3.fromWei(balance, 'ether')
print(f"Balance: {readable} {symbol}")
