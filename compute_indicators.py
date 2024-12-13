import psycopg2
import pandas as pd
import numpy as np

# --------------------- START OF CODE ---------------------
# This code:
# - Connects to 'bigdanbinance' database
# - Fetches 1-minute BTC/USDT data from market_data
# - Computes RSI(14) and MACD(12,26,9) manually
# - Inserts results into indicator_values table

conn = psycopg2.connect(
    dbname="bigdanbinance",
    user="postgres",
    password="jEtsrus33J",
    host="localhost"
)
cur = conn.cursor()

symbol = 'BTC/USDT'

# Fetch data
cur.execute("""
SELECT time, open, high, low, close, volume
FROM market_data
WHERE symbol = %s
ORDER BY time ASC;
""", (symbol,))

rows = cur.fetchall()
if not rows:
    print("No data found for", symbol, "in market_data.")
    cur.close()
    conn.close()
    exit()

df = pd.DataFrame(rows, columns=['time','open','high','low','close','volume'])
df.set_index('time', inplace=True)
df = df.sort_index()

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1/period, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/period, adjust=False).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

rsi_14 = compute_rsi(df['close'], 14)

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

ema12 = ema(df['close'], 12)
ema26 = ema(df['close'], 26)
macd = ema12 - ema26
signal = macd.ewm(span=9, adjust=False).mean()
macd_hist = macd - signal

insert_query = """
INSERT INTO indicator_values (symbol, time, indicator_name, value)
VALUES (%s, %s, %s, %s)
ON CONFLICT (symbol, time, indicator_name) DO NOTHING;
"""

# Insert RSI values
batch_rsi = []
for idx, val in rsi_14.dropna().items():  # using items() instead of iteritems()
    batch_rsi.append((symbol, idx.to_pydatetime(), 'RSI_14', float(val)))
cur.executemany(insert_query, batch_rsi)
conn.commit()
print("Inserted RSI_14 values:", len(batch_rsi))

# Insert MACD values (MACD, MACD_SIGNAL, MACD_HIST)
batch_macd = []
for idx in macd.index:
    if pd.notna(macd.loc[idx]) and pd.notna(signal.loc[idx]) and pd.notna(macd_hist.loc[idx]):
        batch_macd.append((symbol, idx.to_pydatetime(), 'MACD', float(macd.loc[idx])))
        batch_macd.append((symbol, idx.to_pydatetime(), 'MACD_SIGNAL', float(signal.loc[idx])))
        batch_macd.append((symbol, idx.to_pydatetime(), 'MACD_HIST', float(macd_hist.loc[idx])))

cur.executemany(insert_query, batch_macd)
conn.commit()
print("Inserted MACD values:", len(batch_macd))

cur.close()
conn.close()
print("Indicators computed and inserted.")
# ---------------------- END OF CODE ---------------------
