from msilib.schema import CheckBox
import time
import tkinter as tk            # Import tkinter
from tkinter import ttk # ttk is a themed tkinter
from tkinter import Tk, StringVar, Label, Entry, Button, Frame, Canvas, Scrollbar, Listbox, Menu, messagebox, filedialog, simpledialog
from tkinter import Image, PhotoImage
from tkinter.font import Font     # font
from tkinter import scrolledtext as tkst   # scrolled text
from tkinter import IntVar, BooleanVar, DoubleVar, StringVar, Spinbox, Checkbutton
from tkinter.scrolledtext import ScrolledText 
# import askyesno 
from tkinter.messagebox import askyesno
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import *
import json
from pprint import pprint
from datetime import datetime
import abis

start = datetime.now()

provider = 'https://bsc-dataseed.binance.org'
web3 = Web3(Web3.HTTPProvider(provider))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(web3.isConnected())

"""class App(tk.Frame):
    def __init__(self, app):
        width = 800
        height = 500
        # app = Tk()
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
        WalletAddressLabel.place(x=0, y=10)
        WalletAddressLabel.size = (100, 100)
        
        WalletAddress = Entry(app, font=font3, width=27, textvariable=wallet_address)
        WalletAddress.grid(row=0, column=1, padx=10, pady=10)
        WalletAddress.place(x=150, y=10)
        WalletAddress.size = (200, 200)
        PrivateKeylabel = Label(app, text='Private Key:', font=font, width=20)
        PrivateKeylabel.grid(row=0, column=2)
        PrivateKeylabel.place(x=370, y=10)
        PrivateKeylabel.size = (100, 100)
        PrivateKey = Entry(app, font=font3, width=25, textvariable=wallet_private_key)
        PrivateKey.grid(row=0, column=3, padx=10, pady=10)
        PrivateKey.place(x=530, y=10)
        BuyTokenLabel = Label(app, text='Interact token:', font=font, width=20)
        BuyTokenLabel.grid(row=1, column=0)
        BuyTokenLabel.place(x=0, y=50)
        BuyTokenLabel.size = (100, 100)
        BuyToken = Entry(app, font=font3, width=25, textvariable=buy_token)
        BuyToken.grid(row=1, column=1, padx=10, pady=10)
        BuyToken.place(x=150, y=50)
        BuyToken.size = (200, 200)
        LiquidityLabel = Label(app, text='Min liquidity BNB): ', font=font, width=20)
        LiquidityLabel.grid(row=1, column=2)
        LiquidityLabel.place(x=380, y=50)
        LiquidityLabel.size = (100, 100)
        Liquidity = Spinbox(app, font=font3, width=20, from_=1, to=100, increment=1, textvariable=liquidity)
        Liquidity.grid(row=1, column=3, padx=10, pady=10)
        Liquidity.place(x=570, y=50)
        "class Logo(Widget):
            LogoLabel = Label(app, text='Sniper Bot', font=font, width=20)
            LogoLabel.grid(row=3, column=0)
            LogoLabel.place(x=10, y=450)
            LogoLabel.size = (100, 100)
            Logo = ImageTk.PhotoImage(Image.open('logo.png'), width=150, height=150)
            LogoLabel.configure(image=Logo)
        "
        LogsLabel = Label(app, text='Logs:', font=font)
        LogsLabel.grid(row=2, column=0)
        LogsLabel.place(x=10, y=120)
        LogsLabel.size = (100, 100)
        Logs = tkst.ScrolledText(app, width=55, height=20, font=('Arial', 10), wrap=tk.WORD, bg='#1B2226', foreground='#f5f5f5', borderwidth=1)
        Logs.grid(row=3, column=0)
        Logs.place(x=20, y=150)
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
        GasLimit = Spinbox(app, font=font2, width=10, from_=21000, increment=1000, to=99999999999, textvariable=gas_limit)
        GasLimit.grid(row=3, column=3)
        GasLimit.place(x=550, y=210)
        GasLimit.size = (200, 200)
        GasPriceLabel = Label(app, text='Gas Price:', font=font2, width=10)
        GasPriceLabel.grid(row=4, column=3)
        GasPriceLabel.place(x=420, y=240)
        GasPriceLabel.size = (100, 100)
        GasPriceEntry = Spinbox(app, font=font2, from_=5, width=10, increment=1, to=1000, textvariable=gas_price)
        GasPriceEntry.grid(row=5, column=3)
        GasPriceEntry.place(x=550, y=240)
        GasPriceEntry.size = (200, 200)
        AmountLabel = Label(app, text='Amount:', font=font2, anchor='w', width=10)
        AmountLabel.grid(row=2, column=7)
        AmountLabel.place(x=420, y=270)
        AmountLabel.size = (100, 100)
        Amount = Spinbox(app, font=font2, width=10, from_ = 0, increment=0.001, to=1000, textvariable=amount)
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
        TakeProfit = Spinbox(app, font=font2, width=10, from_=10, increment=1, to=1000, textvariable=profit_percent)
        TakeProfit.grid(row=2, column=10)
        TakeProfit.place(x=550, y=330)
        TakeProfit.size = (200, 200)
        StopLossLabel = Label(app, text='Stop Loss:', font=font2, width=10)
        StopLossLabel.grid(row=2, column=11)
        StopLossLabel.place(x=420, y=360)
        StopLossLabel.size = (100, 100)
        StopLoss = Spinbox(app, font=font2, from_=10, to=50, increment=1, width=10, textvariable=stop_loss_percent)
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
   """     
        
font0 = ('Arial', 8)
font = ('Arial', 10)
font2 = ('Arial', 12)
font3 = ('Arial', 14)
font4 = ('Arial', 16)
font5 = ('Arial', 18)

class Sniper(object):
    def __init__(self, master):
        self.master = master
        self.master.title('Sniper')
        self.master.geometry('800x600')
        self.master.resizable(False, False)
        self.master.configure(background='#2F4F4F')
        # self.master.iconbitmap('logo.png')
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.bind('<Control-q>', lambda e: self.master.destroy())
        self.buy_price = 0
        self.expected_price = 0
        # self.create_menu()

        self.create_wallet()
        self.create_token_labels()
        self.create_liquidity()
        self.show_infos()
        self.show_logs()
        self.create_gas_gui()
        self.create_buttons()

        self.logo = PhotoImage(file='logo.png')
        self.master.style = ttk.Style()
        self.master.iconphoto(False, self.logo)
        self.start()

    def start(self):
        self.master.mainloop()

    def setup_vars(self):
        self.WALLET_ADDRESS = self.wallet_address.get()
        self.PRIVATE_KEY = self.wallet_private_key.get()
        self.INTERACT_TOKEN = self.interact_token.get()
        self.LIQUIDITY_POOL = int(self.liquidity.get())
        self.AMOUNT = float(self.amount.get())
        self.GAS_LIMIT = int(self.gas_limit.get())
        self.GAS_PRICE = int(self.gas_price.get())
        self.TAKEPROFIT = float(self.takeprofit.get())
        self.STOPLOSS = float(self.stoploss.get())
        self.BUY_AUTO_SELL = self.is_auto_sell_var.get()
        configs = {
            'WALLET_ADDRESS': self.WALLET_ADDRESS,
            'PRIVATE_KEY': self.PRIVATE_KEY,
            'INTERACT_TOKEN': self.INTERACT_TOKEN,
            'LIQUIDITY_POOL': int(self.LIQUIDITY_POOL),
            'AMOUNT': float(self.AMOUNT),
            'GAS_LIMIT': int(self.GAS_LIMIT),
            'GAS_PRICE': int(self.GAS_PRICE),
            'TAKEPROFIT': int(self.TAKEPROFIT),
            'STOPLOSS': int(self.STOPLOSS),
            'BUY_AUTO_SELL': self.BUY_AUTO_SELL
        }
        print(configs)
        self.log.config(state='normal')
        self.log.insert(tk.END, "Configs inserted successfully!\n")
        self.log.config(state='disabled')
        # self.log.insert(tk.END, 'Configs: ' + str(configs) + '\n')
        self.log.see(tk.END)
        # print("Log inserted!")
        # self.log.insert(tk.END, "Log inserted!\n")

    def setup(self):

        # if len(self.WALLET_ADDRESS) and self.PRIVATE_KEY and self.INTERACT_TOKEN and self.LIQUIDITY_POOL
        try:
            self.setup_vars()
            # self.log.insert(tk.END, 'Configs: ' + str(self.WALLET_ADDRESS) + '\n')
            self.wallet_address_var = web3.toChecksumAddress(self.WALLET_ADDRESS)
            self.interact_token_var = web3.toChecksumAddress(self.INTERACT_TOKEN)
            self.wbnb = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c') # WBNB token address
            uniswap_factory = web3.toChecksumAddress(abis.uniswap_factory)
            self.contract = web3.eth.contract(address=uniswap_factory, abi=abis.uniswap_factory_abi)

            self.contract_buy = web3.eth.contract(address=abis.pancake_router_address, abi=abis.pancake_router_abi)
            self.contract_sell = web3.eth.contract(address=abis.pancakeswap_factory, abi=abis.sellAbi)
            self.factoryContract = web3.eth.contract(address=abis.pancakeswap_factory, abi=abis.pancakeswap_factory_abi)
            self.sellTokenContract = web3.eth.contract(address=self.interact_token_var, abi=abis.sellAbi)
            balance = self.sellTokenContract.functions.balanceOf(self.wallet_address_var).call()
            bnb_balance = web3.eth.get_balance(self.wallet_address_var)
            print(f"Balance {balance}")
            self.symbol = self.sellTokenContract.functions.symbol().call()
            print(f"Balance {balance/10**18} {self.symbol}")
            self.balance.configure(text=f"{round(bnb_balance/10**18, 4)} BNB")
            self.log.config(state='normal')
            self.log.insert(tk.END, f"Balance {balance/10**18} {self.symbol}\n")
            self.log.config(state='disabled')
            self.log.see(tk.END)
        except Exception as e:
            print(e)
            self.log.config(state='normal')
            self.log.insert(tk.END, str(e) + '\n')
            self.log.see(tk.END)
            self.log.config(state='disabled')
        



    def create_menu(self):
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Exit', command=lambda: self.master.destroy())

    def create_wallet(self):
        self.wallet_address_label = Label(self.master, text='Wallet Address:', font=font2, width=15)
        self.wallet_address_label.grid(row=0, column=0)
        self.wallet_address_label.place(x=10, y=10)
        self.wallet_address_label.size = (100, 100)
        self.wallet_address = Entry(self.master, font=font, width=30)
        self.wallet_address.grid(row=0, column=1)
        self.wallet_address.place(x=155, y=10)
        self.wallet_address.size = (200, 200)
        self.wallet_private_key_label = Label(self.master, text='Private Key:', font=font2, width=13)
        self.wallet_private_key_label.grid(row=0, column=2)
        self.wallet_private_key_label.place(x=400, y=10)
        self.wallet_private_key = Entry(self.master, font=font, width=30)
        self.wallet_private_key.grid(row=0, column=3)
        self.wallet_private_key.place(x=530, y=10)
        self.wallet_private_key.size = (200, 200)

    def create_token_labels(self):
        self.interact_token_label = Label(self.master, text='Interact Token:', font=font2, width=15)
        self.interact_token_label.grid(row=1, column=0)
        self.interact_token_label.place(x=10, y=50)
        self.interact_token_label.size = (200, 200)
        self.interact_token = Entry(self.master, font=font, width=30)
        self.interact_token.grid(row=1, column=1)
        self.interact_token.place(x=155, y=50)
        self.interact_token.size = (200, 200)

    def create_liquidity(self):
        self.liquidity_label = Label(self.master, text='Liquidity: ', font=font2, width=13)
        self.liquidity_label.grid(row=1, column=3)
        self.liquidity_label.place(x=400, y=50)
        self.liquidity_label.size = (200, 200)
        self.liquidity = Spinbox(self.master, font=font, width=25, from_=0, to=1000, increment=1)
        self.liquidity.grid(row=1, column=4)
        self.liquidity.place(x=530, y=50)
        self.liquidity.size = (200, 200)
    
    def show_infos(self):
        self.balanace_label = Label(self.master, text='Your Balance in BNB: ', font=font2, width=20)
        self.balanace_label.grid(row=2, column=0)
        self.balanace_label.place(x=200, y=110)
        self.balanace_label.size = (200, 200)
        self.balance = Label(self.master, text='0', font=font2, width=10)
        self.balance.grid(row=2, column=2)
        self.balance.place(x=400, y=110)
        self.balance.size = (200, 200)
        self.setup_button = Button(self.master, text='Setup', font=font2, width=10, command=self.setup)
        self.setup_button.grid(row=2, column=3)
        self.setup_button.place(x=530, y=110)
        self.setup_button.size = (200, 200)


    def show_logs(self):
        self.log_label = Label(self.master, text='Logs: ', font=font2, width=10)
        self.log_label.grid(row=3, column=0)
        self.log_label.place(x=10, y=160)
        self.log_label.size = (200, 200)
        self.log = ScrolledText(self.master, font=('Arial', 8), width=55, height=25, bg='#1B2226', foreground='#f5f5f5', borderwidth=1)
        self.log.grid(row=3, column=0)
        self.log.place(x=10, y=200)
        self.log.size = (200, 200)
        self.log.configure(state='disabled')

    def clear_log(self):
        self.log.config(state='normal')
        self.log.delete(1.0, tk.END)
        self.log.config(state='disabled')
        

    def create_buttons(self):
        self.snipe_button = Button(self.master, text='Snipe', font=font2, width=10)
        self.snipe_button.grid(row=4, column=1)
        self.snipe_button.place(x=400, y=530)
        self.snipe_button.size = (200, 200)
        self.snipe_button.configure(command=self.snipe)
        self.sell_button = Button(self.master, text='Sell', font=font2, width=10)
        self.sell_button.grid(row=4, column=2)
        self.sell_button.place(x=530, y=530)
        self.sell_button.size = (200, 200)
        self.sell_button.configure(command=self.sell)
        self.clear_log_btn = Button(self.master, text='Clear log', font=font2, width=10)
        self.clear_log_btn.grid(row=4, column=3)
        self.clear_log_btn.place(x=660, y=530)
        self.clear_log_btn.configure(command=self.clear_log)
        """self.buy_button = Button(self.master, text='Buy', font=font2, width=10)
        self.buy_button.grid(row=4, column=1)
        self.buy_button.place(x=560, y=530)
        self.buy_button.size = (200, 200)
        self.buy_button.configure(command=self.buy)
        self.exit_button = Button(self.master, text='Exit', font=font2, width=10)
        self.exit_button.grid(row=5, column=7)
        self.exit_button.place(x=680, y=530)
        self.exit_button.size = (200, 200)
        self.exit_button.configure(command=lambda: self.master.destroy() if askyesno('Exit', 'Are you sure?') else None)
"""
    
    def create_gas_gui(self):
        self.gas_limit_label = Label(self.master, text='Gas Limit: ', font=font2, width=13)
        self.gas_limit_label.grid(row=4, column=1)
        self.gas_limit_label.place(x=400, y=200)
        self.gas_limit_label.size = (200, 200)
        self.gas_limit = Spinbox(self.master, font=font2, width=20, from_=21000, to=999999999999999999, increment=1000)
        self.gas_limit.grid(row=4, column=2)
        self.gas_limit.place(x=530, y=200)
        self.gas_limit.size = (200, 200)
        self.gas_price_label = Label(self.master, text='Gas Price: ', font=font2, width=13)
        self.gas_price_label.grid(row=4, column=3)
        self.gas_price_label.place(x=400, y=240)
        self.gas_price_label.size = (200, 200)
        self.gas_price = Spinbox(self.master, font=font2, width=20, from_=5, to=999999999999999999, increment=1)
        self.gas_price.grid(row=4, column=4)
        self.gas_price.place(x=530, y=240)
        self.gas_price.size = (200, 200)
        self.amount_label = Label(self.master, text='Amount: ', font=font2, width=13)
        self.amount_label.grid(row=5, column=1)
        self.amount_label.place(x=400, y=280)
        self.amount_label.size = (200, 200)
        self.amount = Spinbox(self.master, font=font2, width=20, from_=0.001, to=999999999999999999, increment=0.001)
        self.amount.grid(row=5, column=2)
        self.amount.place(x=530, y=280)
        self.amount.size = (200, 200)
        self.takeprofit_label = Label(self.master, text='Take Profit: ', font=font2, width=13)
        self.takeprofit_label.grid(row=5, column=3)
        self.takeprofit_label.place(x=400, y=320)
        self.takeprofit_label.size = (200, 200)
        self.takeprofit = Spinbox(self.master, font=font2, width=20, from_=1, to=1000, increment=1)
        self.takeprofit.grid(row=5, column=4)
        self.takeprofit.place(x=530, y=320)
        self.takeprofit.size = (200, 200)
        self.stoploss_label = Label(self.master, text='Stop Loss: ', font=font2, width=13)
        self.stoploss_label.grid(row=5, column=5)
        self.stoploss_label.place(x=400, y=360)
        self.stoploss_label.size = (200, 200)
        self.stoploss = Spinbox(self.master, font=font2, width=20, from_=1, to=100, increment=1)
        self.stoploss.grid(row=5, column=6)
        self.stoploss.place(x=530, y=360)
        self.stoploss.size = (200, 200)
        self.is_auto_sell_var = BooleanVar()
        self.is_auto_sell = Checkbutton(self.master, font=font2, width=15, text='Auto Sell', variable=self.is_auto_sell_var)
        self.is_auto_sell.grid(row=5, column=8)
        self.is_auto_sell.place(x=400, y=400)
        self.is_auto_sell.size = (200, 200)
            

    # def create_

    def snipe(self):
        self.log.config(state='normal')
        self.log.insert(tk.END, 'Snipe\n')
        self.log.config(state='disabled')
        self.log.see(tk.END)
        self.liquidity.configure(state='disabled')
        self.snipe_button.configure(state='disabled')
        self.sell_button.configure(state='disabled')
        self.wallet_address.configure(state='disabled')
        self.wallet_private_key.configure(state='disabled')
        self.interact_token.configure(state='disabled')
        self.gas_limit.configure(state='disabled')
        self.gas_price.configure(state='disabled')
        self.amount.configure(state='disabled')
        self.takeprofit.configure(state='disabled')
        self.stoploss.configure(state='disabled')
        self.is_auto_sell.configure(state='disabled')
        self.setup_button.configure(state='disabled')
        self.master.update()
        self.master.update_idletasks()
        time.sleep(1*30)
        self.liquidity.configure(state='normal')
        self.snipe_button.configure(state='normal')
        self.sell_button.configure(state='normal')
        self.wallet_address.configure(state='normal')
        self.wallet_private_key.configure(state='normal')
        self.interact_token.configure(state='normal')
        self.gas_limit.configure(state='normal')
        self.gas_price.configure(state='normal')
        self.amount.configure(state='normal')
        self.takeprofit.configure(state='normal')
        self.stoploss.configure(state='normal')
        self.is_auto_sell.configure(state='normal')
        self.setup_button.configure(state='normal')
        self.master.update()
        self.master.update_idletasks()
        

    def sell(self):
        self.log.config(state='normal')
        self.log.insert(tk.END, 'Sell\n')
        self.log.config(state='disabled')
        self.log.see(tk.END)

    def buy(self):
        self.log.config(state='normal')
        self.log.insert(tk.END, 'Buy\n')
        self.log.config(state='disabled')
        self.log.see(tk.END)

    def get_token_price(self, intoken, outtoken):
        amountin = web3.toWei(1, 'ether')
        amountout = self.contract_buy.functions.getAmountsOut(amountin, [outtoken, intoken]).call()
        # print(amountout)    # [0] is token0, [1] is token1
        # print(web3.fromWei(amountout[1], 'ether'))
        return web3.fromWei(amountout[1], 'ether')

    def check_pair(self, intoken, outtoken):
        try:
            pair_address = self.factoryContract.functions.getPair(intoken, outtoken).call()
            # print(pair_address)
            if pair_address != "0x0000000000000000000000000000000000000000":
                pair_contract = web3.eth.contract(address=pair_address, abi=abis.lpAbi)
                # print(pair_contract)
                return pair_contract
            # fetch_liquidity(intoken, outtoken, pair_contract)
            else:
                print("No pair")
                print(f"Intoken: {intoken}, Outtoken: {outtoken}")
                self.check_pair(intoken, outtoken)
        except Exception as e:
            print(e)
            return False
    
    def check_pool(self, inToken, outToken):
        # This function is made to calculate Liquidity of a token
        pair_address = self.factoryContract.functions.getPair(inToken, outToken).call()
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
            self.lp = reserves[0] / DECIMALS
        else:
            # print("reserves[0] is for token 1:")
            self.lp = reserves[1] / DECIMALS
    
        return self.lp
    
    def fetch_liquidity(self, intoken, outtoken):
        try:
            pooled = self.check_pool(intoken, outtoken)
            print(pooled)
            if pooled >= self.LIQUIDITY_POOL:
                print("Pooled enough")
                return True
            else:
                print("Liquidity not enough")
                self.fetch_liquidity(intoken, outtoken)
        except Exception as e:
            print(e)
            print("Liquidity: 0")
            return False


    def reach_profit(self, intoken, outtoken):
        try:
            current_price = float(self.get_token_price(intoken, outtoken))
            print(f"Current price: {current_price}")
            print(f"Expected price: {self.buy_price}")
            print(f"Profit percentage: {round((current_price/float(self.buy_price) - 1)*100, 5)}")
            if current_price >= self.expected_price:
                print("Reach profit")
                return True
            else:
                print("Not reach profit")
                time.sleep(3)
                self.reach_profit(intoken, outtoken)
        except Exception as e:
            print(e)
            print("Reach profit failed")
            return False


    def buy_func(self, intoken, outtoken):
        spend = intoken
        sender_address = self.WALLET_ADDRESS
        price = self.get_token_price(intoken, outtoken)
        print(f"Price: {price}")
        global buy_price, expected_price
        buy_price = price
        expected_price = float(price) * (1 + self.TAKEPROFIT/100)
        print(price)
        try:
            pancakeswap_txn = self.contract_buy.functions.swapExactETHForTokens(
                0,
                [spend, outtoken],
                sender_address,
                (int(time.time()) + 1000*60*5),
            ).buildTransaction({
                'from': sender_address,
                'value': web3.toWei(self.AMOUNT, 'ether'),
                'gas': self.GAS_LIMIT,
                'gasPrice': web3.toWei(self.GAS_PRICE, 'gwei'),
                'nonce': web3.eth.getTransactionCount(sender_address),
            })
            signed_txn = web3.eth.account.signTransaction(
                pancakeswap_txn,
                private_key=self.PRIVATE_KEY
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
    

    def estimateGas(self, txn):
        gas = web3.eth.estimateGas(
            {
                "from": txn["from"],
                "to": txn["to"],
                "value": txn["value"],
                "data": txn["data"],
            }
        )
        self.gas = gas + (gas / 10)
        return self.gas


    def approve(self, tokenValue):
        try:
            txn = self.sellTokenContract.functions.approve(
                abis.pancake_router_address, tokenValue
            ).buildTransaction({
                'from': self.WALLET_ADDRESS,
                'gas': self.GAS_LIMIT,
                'gasPrice': web3.toWei(self.GAS_PRICE, 'gwei'),
                'nonce': web3.eth.getTransactionCount(self.WALLET_ADDRESS),
            })
            txn.update({'gas': int(self.estimateGas(txn))})
    
            signed_txn = web3.eth.account.signTransaction(txn, private_key=self.PRIVATE_KEY)
            pprint(signed_txn)
            tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print(tx_token)
            print(f"Approved {self.INTERACT_TOKEN} for ")
            # return True
        except InvalidTransaction as e:
            print(e)
            # return False
    


    def sell_func(self, intoken, outtoken):
        
        try:
            wallet_address = self.WALLET_ADDRESS
            self.approve()
            print("Sell function")
            time.sleep(1)
            sellTokenContract = web3.eth.contract(address=outtoken, abi=abis.sellAbi)
            tokenValue = sellTokenContract.functions.balanceOf(wallet_address).call()
            print(tokenValue)
            pancakeswap2_txn = self.contract_buy.functions.swapExactTokensForETH(
                tokenValue, 0,
                [outtoken, intoken],
                wallet_address,
                (int(time.time()) + 1000000)
            ).buildTransaction({
                'from': wallet_address,
                'gas': self.GAS_LIMIT,
                'gasPrice': web3.toWei(self.GAS_PRICE, 'gwei'),
                'nonce': web3.eth.getTransactionCount(wallet_address)+1,
                'value': 0,
            })
            pancakeswap2_txn.update({'gas': int(self.estimateGas(pancakeswap2_txn))})
        
            print(pancakeswap2_txn)
            signed_txn = web3.eth.account.signTransaction(pancakeswap2_txn, private_key=self.PRIVATE_KEY)
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
    
    
if __name__ == "__main__":
    root = Tk()
    Sniper(root)
    exit()