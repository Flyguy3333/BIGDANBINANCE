import pandas as pd
import psycopg2
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Database configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

# Fetch data from the database
def fetch_data():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = """
        SELECT coin_symbol, indicator_name, strategy_score, indicator_score, deal_type
        FROM backtest_results
        WHERE deal_type IN ('L', 'S')
        ORDER BY coin_symbol, strategy_score DESC;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        columns = ['coin_symbol', 'indicator_name', 'strategy_score', 'indicator_score', 'deal_type']
        df = pd.DataFrame(data, columns=columns)
        connection.close()
        return df
    except Exception as e:
        print(f"[ERROR]: Failed to fetch data - {e}")
        return pd.DataFrame()

# Prepare data for machine learning (features and labels)
def prepare_data(df):
    """Prepare data for machine learning (features and labels)"""
    df['trade_decision'] = df['deal_type'].apply(lambda x: 1 if x == 'L' else 0)  # 1 = buy, 0 = sell
    df = df.dropna()  # Remove any rows with NaN values

    # Convert strategy_score and indicator_score to numeric, forcing errors to NaN
    df['strategy_score'] = pd.to_numeric(df['strategy_score'], errors='coerce')
    df['indicator_score'] = pd.to_numeric(df['indicator_score'], errors='coerce')

    # Drop rows with NaN values in 'strategy_score' or 'indicator_score' after conversion
    df = df.dropna(subset=['strategy_score', 'indicator_score'])

    # Select features and labels
    features = ['strategy_score', 'indicator_score']
    X = df[features]
    y = df['trade_decision']
    
    return X, y

# Train both Random Forest and XGBoost models
def train_models(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)

    # XGBoost model
    xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)

    # Calculate the accuracy of both models
    rf_accuracy = accuracy_score(y_test, rf_preds)
    xgb_accuracy = accuracy_score(y_test, xgb_preds)

    # Print the classification reports for both models
    print(f"Random Forest Accuracy: {rf_accuracy * 100:.2f}%")
    print(f"XGBoost Accuracy: {xgb_accuracy * 100:.2f}%")

    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, rf_preds))
    print("\nXGBoost Classification Report:")
    print(classification_report(y_test, xgb_preds))

    return rf_preds, xgb_preds, y_test

# Main function to execute the analysis
def main():
    print("[DEBUG]: Starting the backtesting script...")

    # Fetch the data from the database
    df = fetch_data()

    # If no data is found, exit
    if df.empty:
        print("[ERROR]: No data found. Exiting...")
        return

    # Prepare the data for training
    X, y = prepare_data(df)

    # Train the models and display results
    rf_preds, xgb_preds, y_test = train_models(X, y)

if __name__ == "__main__":
    main()
