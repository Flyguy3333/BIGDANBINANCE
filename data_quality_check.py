import psycopg2
import pandas as pd
from datetime import timedelta

# --------------------- START OF CODE ---------------------
# This script:
# - Connects to 'bigdanbinance' DB
# - Fetches 1-minute data for BTC/USDT from market_data
# - Checks daily counts of rows (should be ~1440 per day)
# - Flags days with <1300 rows as missing intervals
# - Checks for outliers in price (e.g., jump more than 50% in one minute)
# No edits required.

conn = psycopg2.connect(
    dbname="bigdanbinance",
    user="postgres",
    password="jEtsrus33J",
    host="localhost"
)
cur = conn.cursor()

symbol = 'BTC/USDT'

# Fetch all 1m data
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

# Check daily counts
df['date'] = df.index.date
daily_counts = df.groupby('date').size()
for date, count in daily_counts.items():
    if count < 1300:
        print(f"Data Quality Issue: {symbol} on {date} only has {count} rows, expected ~1440.")

# Check for price outliers
# Let's define an outlier as close > 1.5 * previous close or close < 0.5 * previous close
# This is arbitrary for demo purposes.
df['prev_close'] = df['close'].shift(1)
df['ratio'] = df['close'] / df['prev_close']
outliers = df[(df['ratio'] > 1.5) | (df['ratio'] < 0.5)]
if not outliers.empty:
    for idx, row in outliers.iterrows():
        print(f"Data Quality Issue: Price outlier at {idx}, close={row['close']}, prev_close={row['prev_close']}, ratio={row['ratio']:.2f}")

# Remove the extra columns after checks (optional)
df.drop(columns=['date','prev_close','ratio'], inplace=True, errors='ignore')

print("Data quality checks completed.")

cur.close()
conn.close()
# ---------------------- END OF CODE ---------------------
