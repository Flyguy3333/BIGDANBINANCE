import psycopg2

# Database connection configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

def fetch_top_10():
    try:
        print("[DEBUG]: Connecting to the database...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = """
        SELECT
            coin_symbol,
            MAX(strategy_score) AS max_score
        FROM backtest_results
        WHERE strategy_score > 0.0
        GROUP BY coin_symbol
        ORDER BY max_score DESC
        LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("\nTop 10 Coins by Strategy Score:")
        print("+-------------+----------------+")
        print("| Coin Symbol | Strategy Score |")
        print("+-------------+----------------+")
        for row in results:
            print(f"| {row[0]:<11} | {row[1]:<14.2f} |")
        print("+-------------+----------------+")

    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("[DEBUG]: Database connection closed.")

if __name__ == "__main__":
    fetch_top_10()
