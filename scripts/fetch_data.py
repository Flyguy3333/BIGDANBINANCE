import pandas as pd
import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

def fetch_data():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = """
        SELECT coin_symbol, indicator_name, strategy_score, indicator_score, deal_type
        FROM backtest_results
        WHERE deal_type IN ('L', 'S')
        ORDER BY coin_symbol, strategy_score DESC;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        columns = ['coin_symbol', 'indicator_name', 'strategy_score', 'indicator_score', 'deal_type']
        df = pd.DataFrame(data, columns=columns)
        connection.close()
        return df
    except Exception as e:
        print(f"[ERROR]: Failed to fetch data - {e}")
        return pd.DataFrame()

# Fetch the data and print it
if __name__ == "__main__":
    df = fetch_data()
    if not df.empty:
        print(df.head())  # Prints the first few rows of the dataframe
    else:
        print("No data fetched.")
