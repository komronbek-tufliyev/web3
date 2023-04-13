import requests
page=requests.get("https://coinmarketcap.com/currencies/binance-coin/")
pagetext=page.text
pos=pagetext.find('<div class="priceValue___11gHJ">')
print(pos)
# price=float(pagetext[pos+33:pos+39])