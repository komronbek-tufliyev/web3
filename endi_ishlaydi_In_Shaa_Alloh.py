from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *
import time
# import tkinter as tk
# from tkinter import Tk, ttk, filedialog, messagebox, Widget, StringVar, IntVar, DoubleVar, BooleanVar, Text, Image
# from tkinter.font import Font
# from tkinter.messagebox import askyesno
# from tkinter.ttk import *
# import tkinter.scrolledtext as tkst
# from PIL import Image, ImageTk
from datetime import datetime
import asyncio
import threading
from config import config
import abis


start = datetime.now()

web3 = Web3(Web3.HTTPProvider(config['provider']))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# WALLET ADDRESS
wallet_address = web3.toChecksumAddress(config['wallet_address'])
# WALLET PRIVATE KEY
wallet_private_key = config['private_key']

# TOKEN ADDRESS TO BUY
token_to_buy = web3.toChecksumAddress(config['buy_token'])
# TOKEN ADDRESS TO SELL
token_to_sell = web3.toChecksumAddress(config['sell_token'])

# CONTRACT TO BUY
contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
# CONTRACT TO SELL
contract_sell = web3.eth.contract(address=abis.pancakeswap_factory, abi=abis.sellAbi)
# Token Contract Sell
SellTokenContract = web3.eth.contract(address=token_to_sell, abi=abis.sellAbi)


def calculate_profit(buy_price, sell_price):
    return (sell_price - buy_price) / buy_price

print(f"Balance of {wallet_address}: {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")


def buy():
    spend = token_to_sell
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
        signed_txn = web3.eth.account.signTransaction(pancakeswap_txn, private_key=wallet_private_key)
        # tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(3)
        print(signed_txn)
        print(f"Swapped {token_to_sell} for {token_to_buy}")
        # tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        # print(tx_receipt)
    except InvalidTransaction as e:
        print(e)


# buy()


def is_approve():
    Approve = contract_sell.functions.allowance(wallet_address, token_to_buy).call()
    Approved_quantity = contract_sell.functions.balanceOf(wallet_address).call()
    if Approve <= Approved_quantity:
        return False
    else:
        return True

"""
def approve():
    if is_approve():
        try:
            approve_txn = contract_sell.functions.approve(token_to_buy, web3.toWei(config['amount'], 'ether')).buildTransaction({
                'from': wallet_address,
                'gas': config['gas_limit'],
                'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
                'nonce': web3.eth.getTransactionCount(wallet_address),
                'value': 0,
            })
            signed_txn = web3.eth.account.signTransaction(approve_txn, private_key=wallet_private_key)
            tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            time.sleep(3)
            print(signed_txn)
            print(f"Approved {token_to_buy} for {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
            if tx_receipt.status == 1:
                print(f"Approved {token_to_buy} for {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")

        except InvalidTransaction as e:
            print(e)
"""


def sell():
    # token_to_buy = token_to_sell
    approve()
    try:
        balance = web3.fromWei(SellTokenContract.functions.balanceOf(wallet_address).call(), 'ether')
        print(f"Balance: {balance}")
        txn = not contract_sell.functions.fromTokenToETH(
            wallet_address, token_to_sell, int(contract_sell.functions.balanceOf(wallet_address).call()),
            (int(time.time()) + 1000 * 60 * 5)
        ).buildTransaction({
            'from': wallet_address,
            'gas': config['gas_limit'],
            'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
            'nonce': web3.eth.getTransactionCount(wallet_address),
            'value': 0,
        })
        signed_txn = web3.eth.account.signTransaction(txn, private_key=wallet_private_key)
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(3)
        print(signed_txn)
        print(f"Sold {token_to_sell} for {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        if tx_receipt.status == 1:
            print(f"Sold {token_to_sell} for {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")
        """pancakeswap_txn = contract_buy.functions.swapExactETHForTokens(
            0,
            [token_to_buy, token_to_sell],
            wallet_address,
            (int(time.time()) + 1000*60*5),
        ).buildTransaction({
            'from': wallet_address,
            'value': web3.toWei(balance, 'ether'),
            'gas': config['gas_limit'],
            'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
            'nonce': web3.eth.getTransactionCount(wallet_address),
        })

        signed_txn = web3.eth.account.signTransaction(pancakeswap_txn, private_key=wallet_private_key)
        # tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(3)
        print(signed_txn)
        print(f"Swapped {token_to_sell} for {token_to_buy}")
        # tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        # symbol = contract_sell.functions.symbol().call()
        # print(tx_receipt)"""
        print(f"Balance: {balance}")
        # print(f"Symbol: {symbol}")
    except InvalidTransaction as e:
        print(e)


# sell()
# def check_price():
#     try:
#         buy_price = web3.fromWei(contract_buy.functions.getPrice(token_to_buy).call(), 'ether')
#         sell_price = web3.fromWei(contract_sell.functions.getPrice(token_to_sell).call(), 'ether')
#         profit = calculate_profit(buy_price, sell_price)
#         print(f"Buy Price: {buy_price}")
#         print(f"Sell Price: {sell_price}")
#         print(f"Profit: {profit}")
#         return profit
#     except InvalidTransaction as e:
#         print(e)

contract_id = web3.toChecksumAddress(config['contract_id'])
contract = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)

sellTokenContract = web3.eth.contract(address=contract_id, abi=abis.sellAbi)

# Get token balance
balance = sellTokenContract.functions.balanceOf(wallet_address).call()
print(f"Balance: {balance}")
symbol = sellTokenContract.functions.symbol().call()
readable = web3.fromWei(balance, 'ether')
print(f"Balance: {readable} {symbol}")
tokenValue = web3.toWei(config['amount'], 'ether')
tokenValue2 = web3.fromWei(tokenValue, 'ether')

approve = sellTokenContract.functions.approve(abis.pancake_router_address, balance).buildTransaction({
    'from': wallet_address,
    'gas': config['gas_limit'],
    'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
    'nonce': web3.eth.getTransactionCount(wallet_address),
})


signed_txn = web3.eth.account.signTransaction(approve, private_key=config['private_key'])
print(signed_txn)
tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"Approved {token_to_sell} for ")
# """
pancakeswap2_txn = contract.functions.swapExactTokensForETH(
    tokenValue, 0, 
    [contract_id, web3.toChecksumAddress(config['buy_token'])],
    wallet_address,
    (int(time.time()) + 100000)
).buildTransaction({
    'from': wallet_address,
    'gas': config['gas_limit'],
    'gasPrice': web3.toWei(config['gas_price'], 'gwei'),
    'nonce': web3.eth.getTransactionCount(wallet_address),
})
print(pancakeswap2_txn)
signed_txn = web3.eth.account.signTransaction(pancakeswap2_txn, private_key=config['private_key'])
print(signed_txn)
tx_token_sell = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"Swapped {token_to_sell} for {token_to_buy}")
# """




