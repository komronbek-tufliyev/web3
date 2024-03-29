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
from pprint import pprint

start = datetime.now()


web3 = Web3(Web3.HTTPProvider(config['provider']))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(web3.isConnected())

# WALLET AND TOKENS CONFIGURATION
wallet_address = web3.toChecksumAddress(config['wallet_address'])  # metamask wallet address
private_key = config['private_key']  #. metamask wallet private key
token_to_buy = web3.toChecksumAddress(config['busd'])  # The token that you want to buy (e.g. BUSD )
wbnb = web3.toChecksumAddress(config['wbnb'])  # The token that you spend (It's constant)
token_to_buy = token_to_buy  # another comment
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

prices = []


def buy(intoken, outtoken):
    spend = intoken
    sender_address = wallet_address
    price = get_token_price(intoken, outtoken)
    print(f"Price: {price}")
    global buy_price, expected_price
    buy_price = price
    expected_price = float(price) * (1 + float(config['takeprofit'])/100)
    print(price)
    try:
        pancakeswap_txn = contract_buy.functions.swapExactETHForTokens(
            0,
            [spend, outtoken],
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
        pprint(signed_txn)
        print(f"Swapped {intoken} for {outtoken}")
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        if tx_receipt.status == 1:
            print(f"Swapped {intoken} for {outtoken}")
            return True
        else:
            print(f"Swap failed")
        pprint(tx_receipt)
    except InvalidTransaction as e:
        print(e)
        return False


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
    try:
        txn = sellTokenContract.functions.approve(
            abis.pancake_router_address, tokenValue
        ).buildTransaction({
            'from': wallet_address,
            'gas': config['gas_limit'],
            'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
            'nonce': web3.eth.getTransactionCount(wallet_address),
        })
        txn.update({'gas': int(estimateGas(txn))})

        signed_txn = web3.eth.account.signTransaction(txn, private_key=private_key)
        pprint(signed_txn)
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(tx_token)
        print(f"Approved {token_to_buy} for ")
        # return True
    except InvalidTransaction as e:
        print(e)
        # return False
    


def sell(intoken, outtoken):
    
    try:
        approve()
        print("Sell function")
        time.sleep(1)
        sellTokenContract = web3.eth.contract(address=outtoken, abi=abis.sellAbi)
        tokenValue = sellTokenContract.functions.balanceOf(wallet_address).call()
        print(tokenValue)
        pancakeswap2_txn = contract_buy.functions.swapExactTokensForETH(
            tokenValue, 0,
            [outtoken, intoken],
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
        print(f"Swapped {outtoken} for {intoken}")
        return True
    except InvalidTransaction as e:
        print(e)
        return False

def calc_profit(amount, takeprofit):
    income = amount * takeprofit/100
    total = amount + income
    return total

def calc_loss(amount, stoploss):
    loss = amount * stoploss/100
    total = amount - loss
    return total



"""def handle_event(event, intoken, outtoken):
    data = Web3.toJSON(event)
    print(data)
    token0 = str(Web3.toJSON(event['args']['token1']))
    token1 = str(Web3.toJSON(event['args']['token0']))
    # if token0 == token_to_buy and token1 == token_to_buy:
    print("Token0: " + token0)
    print("Token1: " + token1)
    try:
        pair_address = factoryContract.functions.getPair(intoken, outtoken).call()
        print(pair_address)
    except Exception as e:
        print(e)
        print("Liquidity: 0")
     
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated, wbnb, token_to_buy)
        await asyncio.sleep(poll_interval)
"""

def main(intoken, outtoken):
    try:
            
        if check_pair(intoken, outtoken):
            print(f"Pair {intoken}/{outtoken} already exists")
            if fetch_liquidity(intoken, outtoken):
                print(f"Liquidity: ")
                if buy(intoken, outtoken):
                    print(f"Buy function: ")
                    if reach_profit(intoken, outtoken):
                        if sell(intoken, outtoken):
                            print("Sell")
                        else:
                            print("Sell failed")
                    else:
                        print("Reach profit failed")
                else:
                    print("Buy failed")
            else:
                print("Fetch liquidity failed")
                                
        else:
            print("Pair not found")
            return False
    except Exception as e:
        print(e)
        exit()

def get_token_price(intoken, outtoken):
    amountin = web3.toWei(1, 'ether')
    amountout = contract_buy.functions.getAmountsOut(amountin, [outtoken, intoken]).call()
    # print(amountout)    # [0] is token0, [1] is token1
    # print(web3.fromWei(amountout[1], 'ether'))
    return web3.fromWei(amountout[1], 'ether')

 
def check_pair(intoken, outtoken):
    try:
        pair_address = factoryContract.functions.getPair(intoken, outtoken).call()
        # print(pair_address)
        if pair_address != "0x0000000000000000000000000000000000000000":
            pair_contract = web3.eth.contract(address=pair_address, abi=abis.lpAbi)
            # print(pair_contract)
            return pair_contract
            # fetch_liquidity(intoken, outtoken, pair_contract)
        else:
            print("No pair")
            print(f"Intoken: {intoken}, Outtoken: {outtoken}")
            check_pair(intoken, outtoken)
    except Exception as e:
        print(e)
        return False


def check_pool(inToken, outToken):
    # This function is made to calculate Liquidity of a token
    pair_address = factoryContract.functions.getPair(inToken, outToken).call()
    balanceContract = web3.eth.contract(address=inToken, abi=abis.sellAbi)
    decimals = balanceContract.functions.decimals().call()
    DECIMALS = 10 ** decimals
    pair_contract = web3.eth.contract(address=pair_address, abi=abis.lpAbi)
    reserves = pair_contract.functions.getReserves().call()

    # print(reserves)
    # Tokens are ordered by the token contract address
    # The token contract address can be interpreted as a number
    # And the smallest one will be token0 internally
    
    ctnb1 = int(inToken, 16)
    ctnb2 = int(outToken, 16)

    if (ctnb1 < ctnb2):
        # print("reserves[0] is for token 0:")
        pooled = reserves[0] / DECIMALS
    else:
        # print("reserves[0] is for token 1:")
        pooled = reserves[1] / DECIMALS

    return pooled


def fetch_liquidity(intoken, outtoken):
    try:
        pooled = check_pool(intoken, outtoken)
        print(pooled)
        if pooled >= config['min_liquidity']:
            print("Pooled enough")
            return True
        else:
            print("Liquidity not enough")
            fetch_liquidity(intoken, outtoken)
    except Exception as e:
        print(e)
        print("Liquidity: 0")
        return False


def reach_profit(intoken, outtoken):
    try:
        current_price = float(get_token_price(intoken, outtoken))
        print(f"Current price: {current_price}")
        print(f"Expected price: {buy_price}")
        print(f"Profit percentage: {round((current_price/float(buy_price) - 1)*100, 5)}")
        if current_price >= expected_price:
            print("Reach profit")
            return True
        else:
            print("Not reach profit")
            time.sleep(3)
            reach_profit(intoken, outtoken)
    except Exception as e:
        print(e)
        print("Reach profit failed")
        return False

 
if __name__=="__main__":
    buy_price = get_token_price(wbnb, web3.toChecksumAddress('0xf20702BD4D8D1DDbe3c9a64fdb9E8132a4B1839D'))
    print(buy_price)
    expected_price = float(buy_price) * (1 + float(config['takeprofit'])/100)
    print(expected_price)
    # reach_profit(wbnb, web3.toChecksumAddress('0xf20702BD4D8D1DDbe3c9a64fdb9E8132a4B1839D'))
    # fetch_liquidity(wbnb, web3.toChecksumAddress('0xF952Fc3ca7325Cc27D15885d37117676d25BfdA6'))
    # main(wbnb, web3.toChecksumAddress('0xf20702BD4D8D1DDbe3c9a64fdb9E8132a4B1839D'))
    # print(f"Profit: {calc_profit(float(config['amount']), config['takeprofit'])}")
    # print(f"Loss: {calc_loss(float(config['amount']), config['stoploss'])}")
    # get_token_price(web3.toChecksumAddress('0xf952fc3ca7325cc27d15885d37117676d25bfda6'))
    # print(check_pool(wbnb, web3.toChecksumAddress('0xF952Fc3ca7325Cc27D15885d37117676d25BfdA6')))
    sell(wbnb, web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56'))
    end = datetime.now()
    print(f"Time: {end - start}")
    # print("DUNYO SENI TOG'ANGMAS YO AMAKIVACHCHANGMAS!!!")
