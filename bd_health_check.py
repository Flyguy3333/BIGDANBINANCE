#!/usr/bin/env python3

import psycopg2
import traceback

# Database connection parameters
DB_HOST = "138.197.180.191"  # Replace with your server IP
DB_NAME = "BIGDANBINANCE"
DB_USER = "postgres"  # Replace with your username
DB_PASSWORD = "jEtsrus33J"  # Replace with your password

try:
    print("Running health check...")
    
    # Connect to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Connected to database successfully.")
    
    # Fetch and print all tables
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(f" - {table[0]}")
    
    # Check if 'signals' table exists
    cursor.execute("""
        SELECT *
        FROM information_schema.tables
        WHERE table_name = 'signals';
    """)
    signals_table = cursor.fetchone()
    if signals_table:
        print("✅ 'signals' table exists.")
    else:
        print("❌ 'signals' table is missing.")

except Exception as e:
    print("Error during health check:")
    traceback.print_exc()
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Database connection closed.")
