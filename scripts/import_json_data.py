import json
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="BIGDANBINANCE",
    user="postgres",
    password="yourpassword",  # Replace with your actual password
    host="localhost"
)

cursor = conn.cursor()

# Path to the JSON file
json_file_path = '/root/BIGDANBINANCE/data/short_term_buy_indicators.json'

# Load the JSON data
with open(json_file_path) as file:
    data = json.load(file)

# Insert data into the table
for entry in data:
    symbol = entry['symbol']
    indicator_name = entry['indicator_name']
    indicator_value = entry['indicator_value']
    
    cursor.execute("""
        INSERT INTO short_term_buy_indicators (symbol, indicator_name, indicator_value)
        VALUES (%s, %s, %s)
    """, (symbol, indicator_name, indicator_value))

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data imported successfully!")
