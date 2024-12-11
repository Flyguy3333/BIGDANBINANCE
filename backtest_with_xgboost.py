import pandas as pd
import numpy as np
from ta import momentum, trend, volatility
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb

# Load your data
data = pd.read_csv('buy_signals.csv')  # Replace with your actual dataset path

# Example function to calculate indicators
def calculate_indicators(df):
    df['rsi'] = momentum.RSIIndicator(close=df['close'], window=14).rsi()
    macd = trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()
    bollinger = volatility.BollingerBands(close=df['close'], window=20)
    df['bollinger_upper'] = bollinger.bollinger_hband()
    df['bollinger_lower'] = bollinger.bollinger_lband()
    return df

# Add indicators to data
data = calculate_indicators(data)
data = data.dropna()  # Drop rows with NaN values

# Prepare data for backtesting
data['buy_signal'] = (data['close'] > data['bollinger_upper']).astype(int)
data['sell_signal'] = (data['close'] < data['bollinger_lower']).astype(int)

# Features and target selection
X = data[['rsi', 'macd', 'macd_diff']]  # Example features
y_buy = data['buy_signal']
y_sell = data['sell_signal']

# Split data into train and test sets
X_train, X_test, y_train_buy, y_test_buy = train_test_split(X, y_buy, test_size=0.3, random_state=42)
X_train, X_test, y_train_sell, y_test_sell = train_test_split(X, y_sell, test_size=0.3, random_state=42)

# Initialize and train XGBoost model for buy signals
model_buy = xgb.XGBClassifier()
model_buy.fit(X_train, y_train_buy)

# Predict and evaluate buy signals
y_pred_buy = model_buy.predict(X_test)
accuracy_buy = accuracy_score(y_test_buy, y_pred_buy)
print(f'Buy Signal Model Accuracy: {accuracy_buy:.2f}')

# Initialize and train XGBoost model for sell signals
model_sell = xgb.XGBClassifier()
model_sell.fit(X_train, y_train_sell)

# Predict and evaluate sell signals
y_pred_sell = model_sell.predict(X_test)
accuracy_sell = accuracy_score(y_test_sell, y_pred_sell)
print(f'Sell Signal Model Accuracy: {accuracy_sell:.2f}')
