import psycopg2

def test_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="bigdanbinance",  # Correct database name
            user="postgres",        # PostgreSQL superuser
            password="jEtsrus33J",  # Database password
            host="localhost",       # Localhost
            port="5432"             # Default PostgreSQL port
        )
        print("Database connection successful")
        connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_db_connection()
