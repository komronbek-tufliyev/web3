
import asyncio
import tkinter as tk
from tkinter import Tk, ttk, filedialog, messagebox, Widget, StringVar, IntVar, DoubleVar, BooleanVar, Text, Image

from tkinter.font import Font
from tkinter.messagebox import askyesno
from tkinter.ttk import *
import tkinter.scrolledtext as tkst
from PIL import Image, ImageTk
from datetime import datetime
start = datetime.now()
width = 800
height = 500
app = Tk()
app.title('Sniper bot. @Web3devs')
app.geometry(f'{width}x{height}')
# app.resizable(False, False)
font = Font(family='Helvetica', size=14)
font2 = Font(family='Helvetica', size=12)
frame = ttk.Frame(app, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky='nsew')


async def get_current_time_loop():
    while True:
        await asyncio.sleep(1)
        current_time = datetime.now()
        time_delta = (current_time - start).total_seconds()
        time_format = f"{int(time_delta // 60):02} min :{int(time_delta % 60):02} seconds "

        return time_format
        # current_time_label.config(text=current_time_str)




# class SnipeWidget(Widget):
wallet_address = StringVar()
wallet_private_key = StringVar()
balance = DoubleVar()
buy_token = StringVar()
sell_token = StringVar()
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

WalletAddress = Entry(app, font=font, width=22, textvariable=wallet_address)
WalletAddress.grid(row=0, column=1)
WalletAddress.place(x=150, y=10)
WalletAddress.size = (200, 200)
PrivateKeylabel = Label(app, text='Private Key:', font=font, width=20)
PrivateKeylabel.grid(row=0, column=2)
PrivateKeylabel.place(x=420, y=10)
PrivateKeylabel.size = (100, 100)
PrivateKey = Entry(app, font=font, width=22, textvariable=wallet_private_key)
PrivateKey.grid(row=0, column=3)
PrivateKey.place(x=530, y=10)
BuyTokenLabel = Label(app, text='Buy Token:', font=font, width=20)
BuyTokenLabel.grid(row=1, column=0)
BuyTokenLabel.place(x=10, y=50)
BuyTokenLabel.size = (100, 100)
BuyToken = Entry(app, font=font, width=22, textvariable=buy_token)
BuyToken.grid(row=1, column=1)
BuyToken.place(x=150, y=50)
BuyToken.size = (200, 200)
SellTokenLabel = Label(app, text='Sell Token:', font=font, width=20)
SellTokenLabel.grid(row=1, column=2)
SellTokenLabel.place(x=420, y=50)
SellTokenLabel.size = (100, 100)
SellToken = Entry(app, font=font, width=22, textvariable=sell_token)
SellToken.grid(row=1, column=3)
SellToken.place(x=530, y=50)
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
Logs.configure(foreground='#FFFFFF')
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
Balance = Label(app, text='0.984660994', font=font2)
Balance.grid(row=2, column=3)
Balance.place(x=550, y=150)
Balance.size = (100, 100)
ProcessTime = Label(app, text='Process Time:', font=('Arial', 12), width=20)
ProcessTime.grid(row=2, column=4)
ProcessTime.place(x=420, y=180)
ProcessTime.size = (100, 100)
ProcessTimeValue = Label(app, text='0.984660994', font=('Arial', 12))
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
TakeProfit = Label(app, text='Take Profit:', font=font2, width=10)
TakeProfit.grid(row=2, column=9)
TakeProfit.place(x=420, y=330)
TakeProfit.size = (100, 100)
TakeProfitEntry = Spinbox(app, font=font2, width=10, from_=0, textvariable=profit_percent)
TakeProfitEntry.grid(row=2, column=10)
TakeProfitEntry.place(x=550, y=330)
TakeProfitEntry.size = (200, 200)
StopLoss = Label(app, text='Stop Loss:', font=font2, width=10)
StopLoss.grid(row=2, column=11)
StopLoss.place(x=420, y=360)
StopLoss.size = (100, 100)
StopLossEntry = Spinbox(app, font=font2, from_=0, to=10, width=10, textvariable=stop_loss_percent)
StopLossEntry.grid(row=2, column=12)
StopLossEntry.place(x=550, y=360)
StopLossEntry.size = (200, 200)
checkbox = Checkbutton(app, text='Auto sell', variable=buy_auto_sell)
checkbox.grid(row=2, column=13) 
checkbox.place(x=420, y=400)
checkbox.size = (200, 200)
ExitButton = Button(app, text='Exit')
ExitButton.grid(row=1, column=6)
ExitButton.place(x=650, y=height-50)
ExitButton.size = (100, 100)
ExitButton.configure(command=lambda: exit() if askyesno(title='Confirmation', message='Are you sure that you want to quit?') else None)

def get_variable_values():
    logs = {
        'wallet_address': wallet_address.get(),
        'private_key': wallet_private_key.get(),
        'buy_token': buy_token.get(),
        'sell_token': sell_token.get(),
        'amount': amount.get(),
        'gas_limit': gas_limit.get(),
        'gas_price': gas_price.get(),
        'profit_percent': profit_percent.get(),
        'stop_loss_percent': stop_loss_percent.get(),
        'buy_auto_sell': buy_auto_sell.get()
    }
    print(logs)
    Logs.insert(tk.END, 'Wallet Address: ' + logs['wallet_address'] + '\n')

SnipeButton.configure(command=lambda: get_variable_values())
frame.pack()
end = datetime.now()
time = end - start
print(time)
loop = asyncio.get_event_loop()
loop.run_until_complete(get_current_time_loop())
loop.close()

if __name__ == '__main__':
    app.mainloop()

