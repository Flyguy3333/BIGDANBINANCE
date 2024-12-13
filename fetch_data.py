import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas_ta as ta

# Database credentials
DB_USERNAME = "postgres"
DB_PASSWORD = "jEtsrus33J"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bigdanbinance"

# Database connection string
db_uri = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQL query to fetch data from the candlesticks table
query = """
SELECT open_time, open, high, low, close, volume
FROM candlesticks
WHERE interval = '1m' AND open_time >= NOW() - INTERVAL '180 days';
"""

# Create a database engine
try:
    engine = create_engine(db_uri)
    data = pd.read_sql(query, engine)
except Exception as e:
    print("Error connecting to the database or fetching data.")
    print(e)
    exit()

# Convert open_time to datetime
data['open_time'] = pd.to_datetime(data['open_time'])

# Data overview
print(data.info())
print(data.describe())

# Generate technical indicators using pandas_ta
data['rsi'] = ta.rsi(data['close'], length=14)  # Relative Strength Index
data['ema50'] = ta.ema(data['close'], length=50)  # 50-period EMA
data['macd'], data['macd_signal'], data['macd_hist'] = ta.macd(data['close'])

# Plot closing prices
plt.figure(figsize=(12, 6))
plt.plot(data['open_time'], data['close'], label='Closing Price')
plt.title('BTCUSDT Closing Prices (Last 180 Days)')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid()
plt.show()

# Plot RSI
plt.figure(figsize=(12, 6))
plt.plot(data['open_time'], data['rsi'], label='RSI', color='orange')
plt.axhline(70, color='red', linestyle='--', label='Overbought')
plt.axhline(30, color='green', linestyle='--', label='Oversold')
plt.title('Relative Strength Index (RSI)')
plt.xlabel('Time')
plt.ylabel('RSI Value')
plt.legend()
plt.grid()
plt.show()

# Save enriched data to a CSV
data.to_csv("candlesticks_with_indicators.csv", index=False)
print("Candlestick data with indicators saved to 'candlesticks_with_indicators.csv'.")
