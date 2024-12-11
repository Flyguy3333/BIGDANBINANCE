import requests
import psycopg2
import time

# Database connection
conn = psycopg2.connect(
    dbname="BIGDANBINANCE",
    user="postgres",
    password="jEtsrus33J",  # Replace with your actual password
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Binance API endpoint
BASE_URL = "https://api.binance.com/api/v3/klines"

# List of symbols
SYMBOLS = ["BTCUSDT", "ETHUSDT"]  # Add more symbols as needed
INTERVALS = ["1d"]  # Start with "1d" (daily interval) for testing

# Function to fetch and insert data
def fetch_and_insert(symbol, interval):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1000  # Binance API max limit
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for record in data:
                timestamp, open_, high, low, close, volume = record[0], record[1], record[2], record[3], record[4], record[5]
                cursor.execute("""
                    INSERT INTO public.binance_futures_data (coin_symbol, interval, timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, TO_TIMESTAMP(%s / 1000), %s, %s, %s, %s, %s)
                """, (symbol, interval, timestamp, open_, high, low, close, volume))
            conn.commit()
            print(f"Inserted data for {symbol} - {interval}")
        elif response.status_code == 429:
            print("Rate limit exceeded. Retrying in 60 seconds...")
            time.sleep(60)
            fetch_and_insert(symbol, interval)
        else:
            print(f"Error fetching {symbol} - {interval}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Main loop
for symbol in SYMBOLS:
    for interval in INTERVALS:
        print(f"Fetching {symbol} - {interval}")
        fetch_and_insert(symbol, interval)
        time.sleep(1)  # Delay between requests to avoid rate limits

# Close connection
cursor.close()
conn.close()
