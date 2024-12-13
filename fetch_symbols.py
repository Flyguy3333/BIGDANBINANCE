import requests

url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
response = requests.get(url)
data = response.json()

usdt_symbols = []
for s in data["symbols"]:
    if s["quoteAsset"] == "USDT" and s["contractType"] == "PERPETUAL":
        usdt_symbols.append(s["symbol"])

print("Total USDT futures pairs:", len(usdt_symbols))
print(usdt_symbols)
