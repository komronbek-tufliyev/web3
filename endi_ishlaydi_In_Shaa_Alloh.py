from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *
import time
from datetime import datetime
from config import config
import abis
import asyncio
import tkinter as tk
from tkinter import Tk, ttk, StringVar, IntVar, DoubleVar, BooleanVar

from tkinter.font import Font
from tkinter.messagebox import askyesno
from tkinter.ttk import *
import tkinter.scrolledtext as tkst
start = datetime.now()


web3 = Web3(Web3.HTTPProvider(config['provider']))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

width = 800
height = 500
app = Tk()
app.title('Sniper bot. @Web3devs')
app.geometry(f'{width}x{height}')
# app.resizable(False, False)
font = Font(family='Helvetica', size=14)
font2 = Font(family='Helvetica', size=12)
font3 = Font(family='Helvetica', size=10)
frame = ttk.Frame(app, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky='nsew')


wallet_address = StringVar()
wallet_private_key = StringVar()
balance = DoubleVar()
buy_token = StringVar()
liquidity = IntVar()
amount = DoubleVar()
gas_limit = IntVar()
gas_price = IntVar()
profit_percent = IntVar()
stop_loss_percent = IntVar()
buy_auto_sell = BooleanVar()
WalletAddressLabel = Label(app, text='Wallet Address:', font=font, width=20)
WalletAddressLabel.grid(row=0, column=0)
WalletAddressLabel.place(x=10, y=10)
WalletAddressLabel.size = (100, 100)

WalletAddress = Entry(app, font=font3, width=22, textvariable=wallet_address)
WalletAddress.grid(row=0, column=1, padx=10, pady=10)
WalletAddress.place(x=150, y=10)
WalletAddress.size = (200, 200)
PrivateKeylabel = Label(app, text='Private Key:', font=font, width=20)
PrivateKeylabel.grid(row=0, column=2)
PrivateKeylabel.place(x=420, y=10)
PrivateKeylabel.size = (100, 100)
PrivateKey = Entry(app, font=font3, width=22, textvariable=wallet_private_key)
PrivateKey.grid(row=0, column=3, padx=10, pady=10)
PrivateKey.place(x=530, y=10)
BuyTokenLabel = Label(app, text='Interact token:', font=font, width=20)
BuyTokenLabel.grid(row=1, column=0)
BuyTokenLabel.place(x=10, y=50)
BuyTokenLabel.size = (100, 100)
BuyToken = Entry(app, font=font3, width=22, textvariable=buy_token)
BuyToken.grid(row=1, column=1, padx=10, pady=10)
BuyToken.place(x=150, y=50)
BuyToken.size = (200, 200)
LiquidityLabel = Label(app, text='Liquidity: ', font=font, width=20)
LiquidityLabel.grid(row=1, column=2)
LiquidityLabel.place(x=420, y=50)
LiquidityLabel.size = (100, 100)
Liquidity = Entry(app, font=font3, width=22, textvariable=liquidity)
Liquidity.grid(row=1, column=3, padx=10, pady=10)
Liquidity.place(x=530, y=50)
"""class Logo(Widget):
    LogoLabel = Label(app, text='Sniper Bot', font=font, width=20)
    LogoLabel.grid(row=3, column=0)
    LogoLabel.place(x=10, y=450)
    LogoLabel.size = (100, 100)
    Logo = ImageTk.PhotoImage(Image.open('logo.png'), width=150, height=150)
    LogoLabel.configure(image=Logo)
"""
LogsLabel = Label(app, text='Logs:', font=font)
LogsLabel.grid(row=2, column=0)
LogsLabel.place(x=10, y=120)
LogsLabel.size = (100, 100)
Logs = tkst.ScrolledText(app, width=55, height=20, font=('Arial', 10), wrap=tk.WORD, bg='#1B2226', foreground='#f5f5f5', borderwidth=1)
Logs.grid(row=3, column=0)
Logs.place(x=10, y=150)
Logs.configure(foreground='#C8C8C8')
Logs.insert(tk.END, 'Logs\n')
SnipeButton = Button(app, text='Snipe')
SnipeButton.grid(row=1, column=4)
SnipeButton.place(x=440, y=height-50)
SnipeButton.size = (100, 100)

SellButton = Button(app, text='Sell All')
SellButton.grid(row=1, column=5)
SellButton.place(x=550, y=height-50)
SellButton.size = (100, 100)
try:
    SellButton.configure(command=lambda: Logs.insert(tk.END, 'Sell All\n'))
    print('Sell All button is working')
except Exception as e:
    print(e)
BalanceLabel = Label(app, text='Balance:', font=font, anchor='w', width=20)
BalanceLabel.grid(row=2, column=2)
BalanceLabel.place(x=420, y=150)
BalanceLabel.size = (100, 100)
Balance = Label(app, text='_______', font=('Arial', 10), anchor='w', width=20)
Balance.grid(row=2, column=3)
Balance.place(x=550, y=150)
Balance.size = (100, 100)
ProcessTime = Label(app, text='Process Time:', font=('Arial', 12), width=20)
ProcessTime.grid(row=2, column=4)
ProcessTime.place(x=420, y=180)
ProcessTime.size = (100, 100)
ProcessTimeValue = Label(app, text='______', font=('Arial', 12))
ProcessTimeValue.grid(row=2, column=5)
ProcessTimeValue.place(x=550, y=180)
ProcessTimeValue.size = (100, 100)
GasLimitLabel = Label(app, text='Gas:', font=font2, anchor='w', width=20)
GasLimitLabel.grid(row=2, column=3)
GasLimitLabel.place(x=420, y=210)
GasLimitLabel.size = (100, 100)
GasLimit = Spinbox(app, font=font2, width=10, from_=21000, textvariable=gas_limit)
GasLimit.grid(row=3, column=3)
GasLimit.place(x=550, y=210)
GasLimit.size = (200, 200)
GasPriceLabel = Label(app, text='Gas Price:', font=font2, width=10)
GasPriceLabel.grid(row=4, column=3)
GasPriceLabel.place(x=420, y=240)
GasPriceLabel.size = (100, 100)
GasPriceEntry = Spinbox(app, font=font2, from_=5, width=10, textvariable=gas_price)
GasPriceEntry.grid(row=5, column=3)
GasPriceEntry.place(x=550, y=240)
GasPriceEntry.size = (200, 200)
AmountLabel = Label(app, text='Amount:', font=font2, anchor='w', width=10)
AmountLabel.grid(row=2, column=7)
AmountLabel.place(x=420, y=270)
AmountLabel.size = (100, 100)
Amount = Spinbox(app, font=font2, width=10, from_=0, textvariable=amount)
Amount.grid(row=2, column=8)
Amount.place(x=550, y=270)
Amount.size = (200, 200)
TimeLabel = Label(app, text='Time:', font=font2, width=10)
TimeLabel.grid(row=2, column=9)
TimeLabel.place(x=420, y=300)
TimeLabel.size = (100, 100)
Time = Entry(app, font=font2, width=10)
Time.grid(row=2, column=10)
Time.place(x=550, y=300)
Time.size = (200, 200)
TakeProfitLabel = Label(app, text='Take Profit:', font=font2, width=10)
TakeProfitLabel.grid(row=2, column=9)
TakeProfitLabel.place(x=420, y=330)
TakeProfitLabel.size = (100, 100)
TakeProfit = Spinbox(app, font=font2, width=10, from_=0, textvariable=profit_percent)
TakeProfit.grid(row=2, column=10)
TakeProfit.place(x=550, y=330)
TakeProfit.size = (200, 200)
StopLossLabel = Label(app, text='Stop Loss:', font=font2, width=10)
StopLossLabel.grid(row=2, column=11)
StopLossLabel.place(x=420, y=360)
StopLossLabel.size = (100, 100)
StopLoss = Spinbox(app, font=font2, from_=0, to=10, width=10, textvariable=stop_loss_percent)
StopLoss.grid(row=2, column=12)
StopLoss.place(x=550, y=360)
StopLoss.size = (200, 200)
checkbox = Checkbutton(app, text='Auto sell', variable=buy_auto_sell)
checkbox.grid(row=2, column=13)
checkbox.place(x=420, y=400)
checkbox.size = (200, 200)
ExitButton = Button(app, text='Exit')
ExitButton.grid(row=1, column=6)
ExitButton.place(x=650, y=height-50)
ExitButton.size = (100, 100)
ExitButton.configure(command=lambda: exit() if askyesno(title='Confirmation', message='Are you sure that you want to quit? You may lost all entered data.') else None)


def calculate_profit(buy_price, sell_price):
    return (sell_price - buy_price) / buy_price


def buy(token_to_sell, contract_buy, token_to_buy, ):
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
            'value': web3.toWei(amount.get(), 'ether'),
            'gas': config['gas_limit'],
            'gasPrice': web3.toWei(gas_price.get(), 'gwei'),
            'nonce': web3.eth.getTransactionCount(sender_address),
        })
        signed_txn = web3.eth.account.signTransaction(pancakeswap_txn, private_key=wallet_private_key)
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(3)
        print(signed_txn)
        print(f"Swapped {token_to_sell} for {token_to_buy}")
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_token)
        if tx_receipt.status == 1:
            print(f"Swapped {token_to_sell} for {token_to_buy}")
            Logs.insert(tk.END, f"Swapped {token_to_sell} for {token_to_buy}" + '\n')
        else:
            print(f"Swap failed")
            Logs.insert(tk.END, f"Swap failed" + '\n')
        # Logs.insert(tk.END, f"Swapped {token_to_sell} for {token_to_buy}" + '\n')
        print(tx_receipt)
    except InvalidTransaction as e:
        print(e)


def is_approve(contract_sell, token_to_buy, wallet_address):
    Approve = contract_sell.functions.allowance(wallet_address, token_to_buy).call()
    Approved_quantity = contract_sell.functions.balanceOf(wallet_address).call()
    if Approve <= Approved_quantity:
        return False
    else:
        return True


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

# is_approve()


def approve(sellTokenContract, contract_sell, token_to_buy, wallet_address, token_to_sell):
    approve = sellTokenContract.functions.approve(abis.pancake_router_address, balance).buildTransaction({
        'from': wallet_address,
        'gas': gas_limit.get(),
        'gasPrice': web3.toWei(gas_price.get(), 'gwei'),
        'nonce': web3.eth.getTransactionCount(wallet_address),
    })

    signed_txn = web3.eth.account.signTransaction(approve, private_key=wallet_private_key)
    print(signed_txn)
    tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Approved {token_to_sell} for ")
    Logs.insert(tk.END, f"Approved {token_to_sell} for " + '\n')


def sell(contract,  tokenValue, token_to_buy, wallet_address, token_to_sell):
    pancakeswap2_txn = contract.functions.swapExactTokensForETH(
        tokenValue, 0,
        [token_to_buy, web3.toChecksumAddress(token_to_sell)],
        wallet_address,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': wallet_address,
        'gas': gas_limit.get(),
        'gasPrice': web3.toWei(gas_price.get(), 'gwei'),
        'nonce': web3.eth.getTransactionCount(wallet_address)+1,
    })

    print(pancakeswap2_txn)
    signed_txn = web3.eth.account.signTransaction(pancakeswap2_txn, private_key=config['private_key'])
    print(signed_txn)
    tx_token_sell = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Swapped {token_to_sell} for {token_to_buy}")


def get_variable_values():
    logs = {
        'wallet_address': wallet_address.get(),
        'private_key': wallet_private_key.get(),
        'buy_token': buy_token.get(),
        # 'sell_token': ,
        'amount': amount.get(),
        'gas_limit': gas_limit.get(),
        'gas_price': gas_price.get(),
        'profit_percent': profit_percent.get(),
        'stop_loss_percent': stop_loss_percent.get(),
        'buy_auto_sell': buy_auto_sell.get()
    }
    print(logs)
    Logs.insert(tk.END, 'Wallet Address: ' + logs['wallet_address'] + '\n')


def main():
    wallet_address = WalletAddress.get()
    wallet_private_key = PrivateKey.get()
    token_to_buy = BuyToken.get()
    amount = Amount.get()
    stoploss = StopLoss.get()
    takeprofit = TakeProfit.get()
    gas_limit = GasLimit.get()
    gas_price = GasPriceEntry.get()
    liquidity = Liquidity.get()

    sniper = Sniper(wallet_address, wallet_private_key, token_to_buy, amount, takeprofit, stoploss, liquidity,
                   gas_limit, gas_price)
    sniper.buy()

    # """# WALLET ADDRESS
    wallet_address = web3.toChecksumAddress(WalletAddress.get())
    # WALLET PRIVATE KEY
    wallet_private_key = str(PrivateKey.get())

    # TOKEN ADDRESS TO BUY
    token_to_buy = web3.toChecksumAddress(buy_token.get())
    # TOKEN ADDRESS TO SELL
    token_to_sell = token_to_buy
    # token_to_sell = web3.toChecksumAddress(SellToken.get())

    # CONTRACT TO BUY
    contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
    # CONTRACT TO SELL
    # Token Contract Sell
    # SellTokenContract = web3.eth.contract(address=token_to_sell, abi=abis.sellAbi)
    contract = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)

    sellTokenContract = web3.eth.contract(address=token_to_buy, abi=abis.sellAbi)
    contract.functions.fetchLiquidityETH(token_to_sell)
    # Get token balance
    balance = sellTokenContract.functions.balanceOf(wallet_address).call()
    print(f"Balance: {balance}")
    symbol = sellTokenContract.functions.symbol().call()
    readable = web3.fromWei(balance, 'ether')
    print(f"Balance: {readable} {symbol}")
    tokenValue = balance
    tokenValue2 = web3.fromWei(tokenValue, 'ether')
    print(f"Balance of {wallet_address}: {web3.fromWei(web3.eth.getBalance(wallet_address), 'ether')}")
    logs = {
        'wallet_address': wallet_address,
        'private_key': wallet_private_key,
        'buy_token': buy_token.get(),
        # 'sell_token': sell_token.get(),
        'amount': amount,
        'gas_limit': gas_limit,
        'gas_price': gas_price,
        'profit_percent': profit_percent.get(),
        'stop_loss_percent': stop_loss_percent.get(),
        'buy_auto_sell': buy_auto_sell.get()
    }
    print(logs)
    Logs.insert(tk.END, 'Wallet Address: ' + str(logs) + '\n')
    Logs.insert(tk.END, f"Balance: {readable} {symbol}" + '\n')
    Balance.configure(text=f"Balance: {readable} {symbol}")
    # """


class Sniper:
    def __init__(self, wallet_address, private_key, token_to_buy, buy_amount, takeprofit, stoploss, liquidity, gas_limit, gas_price):
        self.wallet_address = web3.toChecksumAddress(wallet_address)
        self.private_key = private_key
        self.token_to_buy = web3.toChecksumAddress(token_to_buy)
        self.takeprofit = takeprofit
        self.spend = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')  # wbnb token address
        self.token_to_sell = self.token_to_buy
        self.stoploss = stoploss
        self.liquidity = liquidity
        self.gas_limit = gas_limit
        self.gas_price = gas_price
        self.is_auto_buy_sell = False
        self.buy_amount = buy_amount
        # self.sell_amount = 0
        self.contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
        self.contract_sell = web3.eth.contract(address=self.token_to_buy, abi=abis.sellAbi)

    def calculate_profit(self):
        self.profit = 0

    def estimate_gas(self, txn):
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
            'amount': self.buy_amount,
            'gas_limit': self.gas_limit,
            'gas_price': self.gas_price,
            'profit_percent': self.takeprofit,
            'stop_loss_percent': self.stoploss,
            'buy_auto_sell': self.is_auto_buy_sell,
            "Contract_buy": self.contract_buy,
            "contract_sell": self.contract_sell,
        }
        print(logs)
        Logs.insert(tk.END, 'Wallet Address: ' + logs['wallet_address'] + '\n')

    def sell(self):
        logs = {
            'wallet_address': self.wallet_address,
            'private_key': self.private_key,
            'buy_token': self.token_to_buy,
            'amount': self.buy_amount,
            'gas_limit': self.gas_limit,
            'gas_price': self.gas_price,
            'profit_percent': self.takeprofit,
            'stop_loss_percent': self.stoploss,
            'buy_auto_sell': self.is_auto_buy_sell,
            "Contract_buy": self.contract_buy,
            "contract_sell": self.contract_sell,
        }
        print(logs)
        Logs.insert(tk.END, 'Wallet Address: ' + logs['wallet_address'] + '\n')


def handle_liquidity_event(event):
    pair = web3.toJSON(event)
    print(pair)


async def liquidity_log(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_liquidity_event(event)
        await asyncio.sleep(poll_interval)


def sell_main():
    try:
        wallet_address = WalletAddress.get()
        wallet_private_key = PrivateKey.get()
        token_to_buy = BuyToken.get()
        buy_amount = Amount.get()
        liquidity = Liquidity.get()
        stoploss = StopLoss.get()
        takeprofit = TakeProfit.get()
        gas_limit = GasLimit.get()
        gas_price = GasPriceEntry.get()
        sniper = Sniper(wallet_address, wallet_private_key, token_to_buy, buy_amount, takeprofit, stoploss, liquidity,
                    gas_limit, gas_price)
        sniper.sell()
    except Exception as e:
        print(e)
        Logs.insert(tk.END, 'Error: ' + str(e) + '\n')


SnipeButton.configure(command=lambda: Sniper(WalletAddress.get(), PrivateKey.get(), BuyToken.get(), Amount.get(), TakeProfit.get(), StopLoss.get(), Liquidity.get(), GasLimit.get(), GasPriceEntry.get(), ))
SellButton.configure(command=lambda: sell_main())
frame.pack()
end = datetime.now()
time = end - start
print(time)
loop = asyncio.get_event_loop()

if __name__ == '__main__':
    app.mainloop()


