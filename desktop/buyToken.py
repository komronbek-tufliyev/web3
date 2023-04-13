import time
from web3.exceptions import *


def buy(web3, wallet_address, private_key, contract_buy, token_to_sell, token_to_buy, amount, gas_price, gas_limit):
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
            'value': web3.toWei(amount, 'ether'),
            'gas': gas_limit,
            'gasPrice': web3.toWei(gas_price, 'gwei'),
            'nonce': web3.eth.getTransactionCount(sender_address),
        })
        signed_txn = web3.eth.account.signTransaction(pancakeswap_txn, private_key=private_key)
        # tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(3)
        print(signed_txn)
        print(f"Swapped {token_to_sell} for {token_to_buy}")
        # tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        # print(tx_receipt)
    except InvalidTransaction as e:
        print(e)
        