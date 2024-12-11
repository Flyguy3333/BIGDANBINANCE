import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

def add_long_short_column():
    try:
        print("[DEBUG]: Connecting to the database...")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Add a column for long/short deals if it doesn't exist
        cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name='backtest_results' AND column_name='deal_type'
            ) THEN
                ALTER TABLE backtest_results ADD COLUMN deal_type CHAR(1);
            END IF;
        END $$;
        """)
        connection.commit()

        # Update the column with 'S' or 'L' randomly for demonstration (replace with real logic)
        cursor.execute("""
        UPDATE backtest_results
        SET deal_type = CASE 
            WHEN random() > 0.5 THEN 'L'
            ELSE 'S'
        END
        WHERE deal_type IS NULL;
        """)
        connection.commit()

        print("[DEBUG]: 'deal_type' column added and updated successfully.")
    except Exception as e:
        print(f"[ERROR]: Failed to add/update deal_type column - {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("[DEBUG]: Database connection closed.")

if __name__ == "__main__":
    add_long_short_column()
