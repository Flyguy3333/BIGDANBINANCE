import requests
import psycopg2
from datetime import datetime

def fetch_usdt_futures_coins():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"  # Binance Futures API endpoint
    response = requests.get(url)

    if response.status_code == 200:
        symbols = response.json()["symbols"]
        usdt_futures = [
            (symbol["symbol"], symbol["baseAsset"])
            for symbol in symbols
            if symbol["quoteAsset"] == "USDT" and symbol["status"] == "TRADING"
        ]
        return usdt_futures
    else:
        print("Failed to fetch data from Binance API")
        return []

def insert_usdt_futures_coins(coins):
    try:
        connection = psycopg2.connect(
            dbname="bigdanbinance",  # Corrected database name
            user="postgres",
            password="jEtsrus33J",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        for coin in coins:
            cursor.execute(
                "INSERT INTO coins (coin_symbol, coin_name, added_on) "
                "VALUES (%s, %s, %s) ON CONFLICT (coin_symbol) DO NOTHING;",
                (coin[0], coin[1], datetime.now())
            )

        connection.commit()
        print(f"{len(coins)} USDT Futures coins added successfully!")
    except Exception as e:
        print(f"Error inserting coins: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    usdt_futures_coins = fetch_usdt_futures_coins()
    if usdt_futures_coins:
        insert_usdt_futures_coins(usdt_futures_coins)
