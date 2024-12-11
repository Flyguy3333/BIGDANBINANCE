import pandas as pd
import talib
from datetime import datetime, timezone
from sqlalchemy import create_engine
from psycopg2 import connect

# Database connection URI
DB_URI = "postgresql://postgres:jEtsrus33J@localhost:5432/bigdanbinance"

# Supported indicators
INDICATORS = {
    "relative_strength_index_(rsi)_signal": lambda data: talib.RSI(data['close'], timeperiod=14),
    # Add more indicators as needed
}

# Fetch candlestick data from the database
def fetch_candlestick_data(symbol, interval):
    try:
        engine = create_engine(DB_URI)
        query = f"""
            SELECT open_time, open, high, low, close, volume
            FROM candlesticks
            WHERE symbol = %s AND interval = %s
            ORDER BY open_time;
        """
        df = pd.read_sql(query, engine, params=(symbol, interval))
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol} at {interval}: {e}")
        return pd.DataFrame()

# Store indicator results in the database
def store_indicator_results(symbol, interval, indicator_name, values):
    try:
        connection = connect(DB_URI)
        cursor = connection.cursor()
        for idx, value in enumerate(values):
            if pd.isnull(value):
                continue  # Skip null values
            cursor.execute("""
                INSERT INTO indicators (
                    symbol, interval, indicator_name, indicator_value, calculated_at
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (
                symbol,
                interval,
                indicator_name,
                float(value),
                datetime.now(timezone.utc)
            ))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error storing data for {symbol} at {interval}: {e}")

# Main function to process indicators
def process_indicators(symbol, interval):
    print(f"Processing {symbol} at {interval} interval...")
    data = fetch_candlestick_data(symbol, interval)

    if data.empty or 'close' not in data.columns:
        print(f"No data available for {symbol} at {interval}")
        return

    for indicator_name, func in INDICATORS.items():
        try:
            print(f"Calculating {indicator_name} for {symbol} at {interval}...")
            values = func(data)
            print(f"Storing results for {indicator_name}...")
            store_indicator_results(symbol, interval, indicator_name, values)
        except Exception as e:
            print(f"Error calculating {indicator_name} for {symbol} at {interval}: {e}")

# Main entry point
if __name__ == "__main__":
    SYMBOLS = ["BTCUSDT", "ETHUSDT"]
    INTERVALS = ["1m", "5m"]

    for symbol in SYMBOLS:
        for interval in INTERVALS:
            process_indicators(symbol, interval)
