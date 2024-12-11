import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

def display_top_20():
    try:
        print("[DEBUG]: Connecting to the database...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL query to fetch the top 20 coins by strategy score
        query = """
        SELECT coin_symbol, strategy_score, indicator_name, indicator_score
        FROM backtest_results
        WHERE strategy_score > 0
        ORDER BY strategy_score DESC, indicator_score DESC
        LIMIT 20;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Print results in a formatted table
        print("\nTop 20 Coins by Strategy Score:")
        print("+-------------+----------------+---------------------------+----------------+")
        print("| Coin Symbol | Strategy Score | Chosen Indicator         | Indicator Score|")
        print("+-------------+----------------+---------------------------+----------------+")
        for row in results:
            print(f"| {row[0]:<11} | {row[1]:<14.2f} | {row[2]:<25} | {row[3]:<14.2f} |")
        print("+-------------+----------------+---------------------------+----------------+")

    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    display_top_20()
