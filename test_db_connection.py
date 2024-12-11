import psycopg2

try:
    connection = psycopg2.connect(
        dbname="bigdanbinance",
        user="postgres",
        password="jEtsrus33J",
        host="localhost",
        port="5432"
    )
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")
