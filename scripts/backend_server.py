from flask import Flask, jsonify
import psycopg2

# Flask app
app = Flask(__name__)

# Database connection config
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

# API Endpoint to get Top 20 Coins
@app.route('/api/top_20_coins', methods=['GET'])
def get_top_20_coins():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM top_20_coins ORDER BY rank LIMIT 20;")
        results = cursor.fetchall()
        connection.close()

        # Return as JSON
        coins = [
            {
                "rank": row[0],
                "coin_symbol": row[1],
                "strategy_score": row[2],
                "buy_accuracy": row[3],
                "sell_accuracy": row[4],
                "last_updated": row[5]
            }
            for row in results
        ]
        return jsonify(coins)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
