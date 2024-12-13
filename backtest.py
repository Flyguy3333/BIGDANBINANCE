import psycopg2
import pandas as pd
import time
import numpy as np

# We define a mock EnhancedMLSystem class here to simulate generate_signals without edits
class EnhancedMLSystem:
    def __init__(self, save_path='models/', log_path='logs/'):
        self.save_path = save_path
        self.log_path = log_path

    def load_models(self):
        # Mock loading models
        pass

    def generate_signals(self, df):
        # Mock signal generation logic:
        # If today's close > yesterday's close, signal=1 (buy), else signal=0 (sell)
        # This is a simple heuristic, replace with real logic when available.
        signals = pd.Series(0, index=df.index)
        close = df['close']
        signals.iloc[1:] = np.where(close.iloc[1:].values > close.iloc[:-1].values, 1, 0)
        return signals

# Parameters
SYMBOL = "BTCUSDT"  # Example symbol
INTERVAL = "1d"
INITIAL_CAPITAL = 10000.0

# Connect to DB and fetch data, ensuring timestamp is numeric
conn = psycopg2.connect(
    dbname="bigdanbinance",
    user="myusername",   # Replace with your DB username if needed
    password="jEtsrus33J", # Replace with your DB password if needed
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
cursor.execute("""
    SELECT (EXTRACT(EPOCH FROM time_stamp)*1000)::bigint AS ts,
           open_price, high_price, low_price, close_price, volume
    FROM public.binance_futures_data
    WHERE coin_symbol=%s AND interval=%s
    ORDER BY time_stamp ASC;
""", (SYMBOL, INTERVAL))
rows = cursor.fetchall()
conn.close()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=["timestamp","open","high","low","close","volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
df.set_index("timestamp", inplace=True)
df = df.astype(float)

# Load ML system and generate signals
system = EnhancedMLSystem(save_path='models/', log_path='logs/')
system.load_models()
signals = system.generate_signals(df)

# Simple backtest logic
cash = INITIAL_CAPITAL
position = 0
portfolio_values = []

for i, (idx, row) in enumerate(df.iterrows()):
    signal = signals.iloc[i]
    price = row["close"]

    # Strategy:
    # If signal=1 and no position, buy one unit
    # If signal=0 and have position, sell all
    if signal == 1 and position == 0:
        units = int(cash // price)
        if units > 0:
            position = units
            cash -= units * price
    elif signal == 0 and position > 0:
        cash += position * price
        position = 0

    # Record portfolio value
    portfolio_value = cash + position * price
    portfolio_values.append(portfolio_value)

final_value = portfolio_values[-1]
returns = (final_value - INITIAL_CAPITAL) / INITIAL_CAPITAL
max_drawdown = 0
peak = portfolio_values[0]
for val in portfolio_values:
    if val > peak:
        peak = val
    dd = (peak - val) / peak
    if dd > max_drawdown:
        max_drawdown = dd

# Print results
print("Final Portfolio Value:", final_value)
print("Returns:", returns*100, "%")
print("Max Drawdown:", max_drawdown*100, "%")

# Storing results in DB is optional, if table is ready uncomment and edit if needed:
# conn = psycopg2.connect(dbname="bigdanbinance", user="myusername", password="jEtsrus33J", host="localhost", port="5432")
# cursor = conn.cursor()
# cursor.execute("""
#     INSERT INTO backtest_results (strategy_name, symbol, start_date, end_date, returns, max_drawdown)
#     VALUES (%s, %s, %s, %s, %s, %s)
# """, ("Mock_Strategy", SYMBOL, df.index[0], df.index[-1], returns, max_drawdown))
# conn.commit()
# conn.close()
