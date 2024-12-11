import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from celery import Celery
import pandas_ta as ta

# Database Connection
DATABASE_URL = "postgresql://postgres:jEtsrus33J@localhost:5432/bigdanbinance"
engine = create_engine(DATABASE_URL)

# Initialize Celery App
app = Celery('backtesting_pipeline', broker='redis://localhost:6379/0')

# Fetch Historical Data
@app.task
def fetch_historical_data(coin_symbol):
    query = f"""
    SELECT open_time, open, high, low, close, volume
    FROM candlesticks
    WHERE symbol = '{coin_symbol}'
    ORDER BY open_time;
    """
    return pd.read_sql(query, engine)

# Compute Indicators
def compute_indicator(data, indicator_config):
    try:
        name = indicator_config['name']
        if "RSI" in name:
            lookback = int(indicator_config['adjustments'].split('period')[0].strip().split()[-1]) if 'period' in indicator_config['adjustments'] else 14
            return data.ta.rsi(length=lookback)
        elif "Bollinger" in name:
            return data.ta.bbands(length=20)
        # Add other indicators as needed
        return None
    except Exception as e:
        print(f"Error computing {name}: {str(e)}")
        return None

# Backtest Single Indicator
@app.task
def backtest_indicator(coin_symbol, indicator_config):
    try:
        data = fetch_historical_data(coin_symbol)
        indicator_values = compute_indicator(data, indicator_config)
        if indicator_values is None:
            return None
        
        # Simple backtesting logic
        signals = indicator_values < 30  # Example: Buy signal if indicator < 30
        data['profit'] = np.where(signals, data['close'].shift(-1) - data['close'], 0)
        profit = data['profit'].sum()

        return {
            'coin': coin_symbol,
            'indicator': indicator_config['name'],
            'profit': profit
        }
    except Exception as e:
        print(f"Error backtesting {coin_symbol}: {str(e)}")
        return None

# Example Task for Testing
@app.task
def example_task():
    return "Task executed successfully!"
