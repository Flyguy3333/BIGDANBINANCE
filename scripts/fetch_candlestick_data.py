import requests
import psycopg2
from datetime import datetime
import pytz  # Add pytz for timezone support
import time

# Database connection details
DB_URI = "dbname=bigdanbinance user=postgres password=jEtsrus33J host=localhost port=5432"

# Binance API details
API_URL = "https://api.binance.com/api/v3/klines"

# Symbols and intervals to fetch
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
INTERVALS = ["1m", "5m"]

# Database connection
def connect_to_db():
    return psycopg2.connect(DB_URI)

# Fetch candlestick data from Binance
def fetch_candlestick_data(symbol, interval):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1000
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {symbol} at {interval}: {response.status_code}")
        return []

# Insert candlestick data into the database
def insert_candlestick_data(cursor, symbol, interval, data):
    for entry in data:
        try:
            open_time = datetime.utcfromtimestamp(entry[0] / 1000).replace(tzinfo=pytz.UTC)
            close_time = datetime.utcfromtimestamp(entry[6] / 1000).replace(tzinfo=pytz.UTC)

            cursor.execute("""
                INSERT INTO candlesticks (
                    symbol, interval, open_time, open, high, low, close, volume, close_time,
                    quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, interval, open_time) DO NOTHING;
            """, (
                symbol,
                interval,
                open_time,
                float(entry[1]),
                float(entry[2]),
                float(entry[3]),
                float(entry[4]),
                float(entry[5]),
                close_time,
                float(entry[7]),
                int(entry[8]),
                float(entry[9]),
                float(entry[10])
            ))
        except Exception as e:
            print(f"Error inserting data for {symbol} at {interval}: {e}")

# Main function to fetch and store data
def main():
    while True:
        try:
            connection = connect_to_db()
            cursor = connection.cursor()

            for symbol in SYMBOLS:
                for interval in INTERVALS:
                    print(f"Fetching data for {symbol} at {interval} interval...")
                    data = fetch_candlestick_data(symbol, interval)
                    if data:
                        print(f"Inserting {len(data)} records for {symbol} at {interval} interval.")
                        insert_candlestick_data(cursor, symbol, interval, data)
                        connection.commit()

            cursor.close()
            connection.close()

            print("Sleeping for 1 minute to respect API limits...")
            time.sleep(60)
        except KeyboardInterrupt:
            print("Process interrupted. Exiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
