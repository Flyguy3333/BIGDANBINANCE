import psycopg2
import pandas as pd
import numpy as np
import time

# Define your SYMBOLS and INDICATORS lists:
# For demonstration, we mock them with fewer entries. Replace these with your full lists (e.g. 303 symbols and 160 indicators).
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Replace with your full list of ~303 symbols
INDICATORS = ["indicator1", "indicator2", "indicator3"]  # Replace with your full list of 160 indicators

# Database connection info
DB_NAME = "bigdanbinance"
DB_USER = "myusername"   # replace if needed
DB_PASS = "jEtsrus33J"   # replace if needed
DB_HOST = "localhost"
DB_PORT = "5432"

def fetch_data(symbol, interval="1d"):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    # Ensure timestamp cast to bigint to avoid ValueError
    cursor.execute("""
        SELECT (EXTRACT(EPOCH FROM time_stamp)*1000)::bigint AS ts,
               open_price, high_price, low_price, close_price, volume
        FROM public.binance_futures_data
        WHERE coin_symbol=%s AND interval=%s
        ORDER BY time_stamp ASC;
    """, (symbol, interval))
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df

def compute_signals(df, indicator_name):
    # Mock signal generation for demonstration:
    # In reality, you'd compute the indicator based on df and produce signals
    # 1 = buy signal, 0 = sell signal.
    # Here we just generate random signals.
    signals = pd.Series(np.where(np.random.rand(len(df))>0.7, 1, 0), index=df.index)
    return signals

def run_backtest(df, signals, initial_capital=10000.0):
    cash = initial_capital
    position = 0
    portfolio_values = []

    for i, (idx, row) in enumerate(df.iterrows()):
        signal = signals.iloc[i]
        price = row["close"]

        # Simple strategy: if signal=1 and no position, buy one unit; if signal=0 and have position, sell all.
        if signal == 1 and position == 0:
            units = int(cash // price)
            if units > 0:
                position = units
                cash -= units * price
        elif signal == 0 and position > 0:
            cash += position * price
            position = 0

        portfolio_value = cash + position * price
        portfolio_values.append(portfolio_value)

    final_value = portfolio_values[-1] if portfolio_values else initial_capital
    returns = (final_value - initial_capital) / initial_capital
    max_drawdown = 0
    peak = portfolio_values[0] if portfolio_values else initial_capital
    for val in portfolio_values:
        if val > peak:
            peak = val
        dd = (peak - val) / peak
        if dd > max_drawdown:
            max_drawdown = dd

    return returns, max_drawdown, df.index[0] if len(df)>0 else None, df.index[-1] if len(df)>0 else None

def store_results(strategy_name, symbol, indicator_name, start_date, end_date, returns, max_dd):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backtest_results (strategy_name, symbol, indicator_name, start_date, end_date, returns, max_drawdown)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (strategy_name, symbol, indicator_name, start_date, end_date, returns, max_dd))
    conn.commit()
    conn.close()

# Main loop: For each symbol and each indicator, run backtest and store results
for symbol in SYMBOLS:
    df = fetch_data(symbol)
    if df.empty:
        print(f"No data for {symbol}, skipping.")
        continue

    for indicator in INDICATORS:
        signals = compute_signals(df, indicator)
        returns, max_dd, start_date, end_date = run_backtest(df, signals)
        store_results("ML_Enhanced_Strategy", symbol, indicator, start_date, end_date, returns, max_dd)
        print(f"Processed {symbol} with {indicator}: Returns={returns*100:.2f}%, MaxDD={max_dd*100:.2f}%")

print("All done.")
