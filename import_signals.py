import json
import psycopg2
import logging

# Setup logging
logging.basicConfig(
    filename='/root/BIGDANBINANCE/import_signals.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection
try:
    conn = psycopg2.connect(
        dbname="BIGDANBINANCE",
        user="trading_user",
        password="your_password",
        host="localhost"
    )
    cursor = conn.cursor()
    logging.info("Database connection successful!")
except Exception as e:
    logging.error(f"Failed to connect to database: {e}")
    raise

def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logging.info(f"Successfully loaded JSON file: {file_path}")
            return data
    except Exception as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        raise

def insert_signals(data, signal_type="buy"):
    """Insert signals into the database."""
    try:
        # If the data is a list, process it directly
        indicators = data if isinstance(data, list) else data.get(f"short_term_{signal_type}_indicators", [])
        for signal in indicators:
            if signal_type == "buy":
                cursor.execute(
                    """
                    INSERT INTO buy_signals (name, formula, buy_signal, adjustments, notes)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (signal['name'], signal['formula'], signal.get('buy_signal'), signal.get('adjustments'), signal.get('notes'))
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO sell_signals (name, formula, sell_signal, adjustments, notes)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (signal['name'], signal['formula'], signal.get('sell_signal'), signal.get('adjustments'), signal.get('notes'))
                )
            logging.info(f"Inserted {signal_type} signal: {signal['name']}")
    except Exception as e:
        logging.error(f"Error inserting {signal_type} signals: {e}")
        raise

try:
    # Load and insert buy signals
    buy_signals_data = load_json('/root/BIGDANBINANCE/buy_signals.json')
    insert_signals(buy_signals_data, signal_type="buy")

    # Load and insert sell signals
    sell_signals_data = load_json('/root/BIGDANBINANCE/7DECFINALSHORTSELL.json')
    insert_signals(sell_signals_data, signal_type="sell")

    # Commit changes
    conn.commit()
    logging.info("Data import completed successfully!")

except Exception as e:
    logging.error(f"An error occurred during import: {e}")
finally:
    # Close database connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    logging.info("Database connection closed.")
