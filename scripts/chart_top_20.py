import psycopg2
from tabulate import tabulate

# Database connection configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

# Debug function
def debug_log(message):
    print(f"[DEBUG]: {message}")

try:
    # Connect to the database
    debug_log("Connecting to the database...")
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Query to fetch top 20 unique coins by strategy score
    query = """
        SELECT coin_symbol, MAX(strategy_score) AS max_score
        FROM backtest_results
        GROUP BY coin_symbol
        ORDER BY max_score DESC
        LIMIT 20;
    """
    debug_log("Executing query...")
    cursor.execute(query)
    results = cursor.fetchall()
    debug_log(f"Query executed successfully. Retrieved {len(results)} rows.")

    # Format results
    headers = ["Coin Symbol", "Strategy Score"]
    table = tabulate(results, headers, tablefmt="pretty")

    # Display results in the terminal
    print("\nTop 20 Unique Coins by Strategy Score:")
    print(table)

except Exception as e:
    print(f"[ERROR]: {e}")
finally:
    # Close the connection
    if 'connection' in locals() and connection:
        debug_log("Closing the database connection.")
        connection.close()
