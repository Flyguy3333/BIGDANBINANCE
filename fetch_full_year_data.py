import ccxt
import psycopg2
from datetime import datetime, timedelta
import time

# --------------------- START OF CODE ---------------------

# This code fetches 1 year of 1-minute OHLCV data for BTC/USDT from Binance
# and inserts it into the market_data table in PostgreSQL.
#
# Assumptions:
# - PostgreSQL DB name: BIGDANBINANCE
# - User: postgres
# - Password: (empty)
# - Host: localhost
# - Table: market_data(symbol TEXT, time TIMESTAMP, open NUMERIC, high NUMERIC, low NUMERIC, close NUMERIC, volume NUMERIC, PRIMARY KEY(symbol, time))
# - Symbol: BTC/USDT
# - No editing required.

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="BIGDANBINANCE",
    user="postgres",
    password="",
    host="localhost"
)
cur = conn.cursor()

# Exchange setup
exchange = ccxt.binance({
    'enableRateLimit': True
})

symbol = 'BTC/USDT'
timeframe = '1m'  # 1-minute data
limit = 1000  # max candles per fetch
# Get one year ago timestamp in ms
one_year_ago = datetime.utcnow() - timedelta(days=365)
since_ms = int(one_year_ago.timestamp() * 1000)

# We'll paginate through historical data until we reach current time
# Insert data as we go.
#
# Data format from ccxt: [timestamp, open, high, low, close, volume]
# timestamp in ms
# Convert to UTC timestamp for database insertion
#

def insert_ohlcv(rows):
    # rows format: [[ts, o, h, l, c, v], ...]
    # Insert into market_data
    insert_query = """
    INSERT INTO market_data (symbol, time, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (symbol, time) DO NOTHING;
    """
    for r in rows:
        ts = r[0] / 1000.0
        # Convert to UTC datetime
        dt = datetime.utcfromtimestamp(ts)
        o = r[1]
        h = r[2]
        l = r[3]
        c = r[4]
        v = r[5]
        cur.execute(insert_query, (symbol, dt, o, h, l, c, v))
    conn.commit()

print("Fetching 1 year of 1m data for BTC/USDT from Binance...")

# Fetch loop
# We stop if we get no new data or we reach present
while True:
    print("Fetching batch since:", datetime.utcfromtimestamp(since_ms/1000.0))
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since_ms, limit=limit)
    if not ohlcv:
        # no more data
        print("No more data returned.")
        break
    insert_ohlcv(ohlcv)
    last_ts = ohlcv[-1][0]
    # Add 1 ms to avoid duplicates in next call
    since_ms = last_ts + 1
    # If we are close to now, break
    now_ms = int(time.time() * 1000)
    if since_ms >= now_ms - (60*1000):  # within last minute
        print("Reached current time.")
        break
    time.sleep(exchange.rateLimit / 1000.0)  # rate limit respect

print("Data fetch complete. Check DB for records.")

cur.close()
conn.close()

# ---------------------- END OF CODE ----------------------
