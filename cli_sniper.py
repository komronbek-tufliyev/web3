import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *
import time
from datetime import datetime
from config import config
import abis
import asyncio
import logging
import decimal
import json

start = datetime.now()


web3 = Web3(Web3.HTTPProvider(config['provider']))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(web3.isConnected())

# WALLET AND TOKENS CONFIGURATION
wallet_address = web3.toChecksumAddress(config['wallet_address'])  # metamask wallet address
private_key = config['private_key']  #. metamask wallet private key
token_to_buy = web3.toChecksumAddress(config['busd'])  # The token that you want to buy (e.g. BUSD )
wbnb = web3.toChecksumAddress(config['wbnb'])  # The token that you spend (It's constant)
token_to_sell = token_to_buy  # another comment
# uniswap factory address and abi = pancakeswap factory 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f 
uniswap_factory = web3.toChecksumAddress('0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73')  #Testnet  #0x6725F303b657a9451d8BA641348b6761A6CC7a17
uniswap_factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)


# CONTRACTS
contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
contract_sell = web3.eth.contract(address=abis.pancakeswap_factory, abi=abis.sellAbi)
factoryContract = web3.eth.contract(address=abis.pancakeswap_factory, abi=abis.factory2_abi)
sellTokenContract = web3.eth.contract(address=token_to_buy, abi=abis.sellAbi)
balance = sellTokenContract.functions.balanceOf(wallet_address).call()
print(f"Balance: {balance}")
symbol = sellTokenContract.functions.symbol().call()
readable = web3.fromWei(balance, 'ether')
print(f"Balance: {readable} {symbol}")
tokenValue = balance
tokenValue2 = web3.fromWei(tokenValue, 'ether')
print(f"Balance of {wallet_address}: {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")


def buy():
    spend = wbnb
    sender_address = wallet_address
    try:
        pancakeswap_txn = contract_buy.functions.swapExactETHForTokens(
            0,
            [spend, token_to_buy],
            wallet_address,
            (int(time.time()) + 1000*60*5),
        ).buildTransaction({
            'from': sender_address,
            'value': web3.toWei(config['amount'], 'ether'),
            'gas': config['gas_limit'],
            'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
            'nonce': web3.eth.getTransactionCount(sender_address),
        })
        signed_txn = web3.eth.account.signTransaction(
            pancakeswap_txn,
            private_key=private_key
        )
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(3)
        print(signed_txn)
        print(f"Swapped {token_to_sell} for {token_to_buy}")
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        if tx_receipt.status == 1:
            print(f"Swapped {token_to_sell} for {token_to_buy}")
        else:
            print(f"Swap failed")
        print(tx_receipt)
    except InvalidTransaction as e:
        print(e)

# buy()

def estimateGas(txn):
    gas = web3.eth.estimateGas(
        {
            "from": txn["from"],
            "to": txn["to"],
            "value": txn["value"],
            "data": txn["data"],
        }
    )
    gas = gas + (gas / 10)
    return gas



def approve():
    txn = sellTokenContract.functions.approve(
            abis.pancake_router_address, tokenValue
    ).buildTransaction({
        'from': wallet_address,
        'gas': config['gas_limit'],
        'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
        'nonce': web3.eth.getTransactionCount(wallet_address),
        # 'value': 0,
    })
    txn.update({'gas': int(estimateGas(txn))})

    signed_txn = web3.eth.account.signTransaction(txn, private_key=private_key)
    print(signed_txn)
    tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(tx_token)
    print(f"Approved {token_to_sell} for ")

# approve()

def sell():
    approve()
    time.sleep(3)
    pancakeswap2_txn = contract_buy.functions.swapExactTokensForETH(
        tokenValue, 0,
        [token_to_buy, wbnb],
        wallet_address,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': wallet_address,
        'gas': config['gas_limit'],
        'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
        'nonce': web3.eth.getTransactionCount(wallet_address)+1,
        'value': 0,
    })
    pancakeswap2_txn.update({'gas': int(estimateGas(pancakeswap2_txn))})

    print(pancakeswap2_txn)
    signed_txn = web3.eth.account.signTransaction(pancakeswap2_txn, private_key=config['private_key'])
    print(signed_txn)
    tx_token_sell = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Swapped {token_to_sell} for {token_to_buy}")



def handle_event(event, intoken, outtoken):
    data = Web3.toJSON(event)
    print(data)
    token0 = str(Web3.toJSON(event['args']['token1']))
    token1 = str(Web3.toJSON(event['args']['token0']))
    # if token0 == token_to_sell and token1 == token_to_buy:
    print("Token0: " + token0)
    print("Token1: " + token1)
    try:
        pair_address = factoryContract.functions.getPair(intoken, outtoken).call()
        print(pair_address)
        pair_contract = web3.eth.contract(address=pair_address, abi=abis.lpAbi)
        reserves = pair_contract.functions.getReserves().call()
        print(reserves)
        pooled = reserves[1]/10**18
        print(pooled)
        if pooled >= 20:
            print("Pooled enough")
        else:
            fetch_liquidity()
    except Exception as e:
        print(e)
        print("Liquidity: 0")
     
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated, wbnb, token_to_buy)
        await asyncio.sleep(poll_interval)

def main():
    event_filter = contract.events.PairCreated.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter,2 )
            )
        )
    finally:
        loop.close()

def get_token_price(token):
    amountin = web3.toWei(1, 'ether')
    amountout = contract_buy.functions.getAmountsOut(amountin, [token, wbnb]).call()
    print(amountout)    # [0] is token0, [1] is token1
    print(web3.fromWei(amountout[1], 'ether'))
    

get_token_price(token_to_buy)

def fetch_liquidity(intoken, outtoken):
    try:
        pair_address = factoryContract.functions.getPair(intoken, outtoken).call()
        print(pair_address)
        pair_contract = web3.eth.contract(address=pair_address, abi=abis.lpAbi)
        reserves = pair_contract.functions.getReserves().call()
        print(reserves)
        pooled = reserves[1]/10**18
        print(pooled)
        if pooled >= 20:
            print("Pooled enough")
        else:
            fetch_liquidity()
    except Exception as e:
        print(e)
        print("Liquidity: 0")

# fetch_liquidity(wbnb, token_to_sell)

def reach_profit():
    

# main()
end = datetime.now()
print(f"Time: {end - start}")
print("DUNYO SENI TOG'ANGMAS YO AMAKIVACHCHANGMAS!!!")
