import psycopg2
import pandas as pd

# This code:
# - Connects to 'bigdanbinance' database
# - Fetches 1-minute BTC/USDT data from market_data
# - Resamples to 5m, 15m, 1h, 1d
# - Inserts into market_data_5m, market_data_15m, market_data_1h, market_data_1d
# No edits required.

conn = psycopg2.connect(
    dbname="bigdanbinance",
    user="postgres",
    password="jEtsrus33J",
    host="localhost"
)
cur = conn.cursor()

symbol = 'BTC/USDT'

cur.execute("""
SELECT symbol, time, open, high, low, close, volume
FROM market_data
WHERE symbol = %s
ORDER BY time ASC;
""", (symbol,))

rows = cur.fetchall()
if not rows:
    print("No data found for", symbol)
    cur.close()
    conn.close()
    exit()

df = pd.DataFrame(rows, columns=['symbol','time','open','high','low','close','volume'])
df.set_index('time', inplace=True)
df = df.sort_index()

def resample_ohlcv(df, rule):
    df_agg = df.resample(rule).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    df_agg = df_agg.dropna(subset=['open','close'])
    return df_agg

df_5m = resample_ohlcv(df[['open','high','low','close','volume']], '5min')
df_15m = resample_ohlcv(df[['open','high','low','close','volume']], '15min')
df_1h = resample_ohlcv(df[['open','high','low','close','volume']], '1H')
df_1d = resample_ohlcv(df[['open','high','low','close','volume']], '1D')

def insert_data(table_name, df_in):
    insert_query = f"""
    INSERT INTO {table_name} (symbol, time, open, high, low, close, volume)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (symbol, time) DO NOTHING;
    """
    batch = []
    for idx, row in df_in.iterrows():
        batch.append((symbol, idx.to_pydatetime(), row['open'], row['high'], row['low'], row['close'], row['volume']))
    cur.executemany(insert_query, batch)
    conn.commit()

insert_data('market_data_5m', df_5m)
print("Inserted 5m data")

insert_data('market_data_15m', df_15m)
print("Inserted 15m data")

insert_data('market_data_1h', df_1h)
print("Inserted 1h data")

insert_data('market_data_1d', df_1d)
print("Inserted 1d data")

cur.close()
conn.close()
print("All aggregations inserted.")
