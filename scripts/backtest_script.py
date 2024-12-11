import psycopg2
import json
import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Database configuration
DB_CONFIG = {
    "dbname": "bigdanbinance",
    "user": "postgres",
    "password": "jEtsrus33J",
    "host": "127.0.0.1",
    "port": 5432
}

# Paths to indicators
BUY_INDICATORS_PATH = "/root/BIGDANBINANCE/indicators/short_term_buy.json"
SELL_INDICATORS_PATH = "/root/BIGDANBINANCE/indicators/short_term_sell.json"

# Fetch historical data from the database
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
    df['trade_decision'] = df['deal_type'].apply(lambda x: 1 if x == 'L' else 0)
    
    # Drop any rows with missing data
    df_cleaned = df.dropna()
    
    # Features and labels
    X = df_cleaned[['strategy_score', 'indicator_score']]  # Use strategy_score and indicator_score as features
    y = df_cleaned['trade_decision']  # Labels: Buy or Sell (1 or 0)
    
    return X, y

# Train Random Forest and XGBoost models
def train_models(X, y):
    """Train Random Forest and XGBoost models on the data"""
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Apply SMOTE to balance the dataset
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    
    # Initialize Random Forest and XGBoost classifiers
    rf_model = RandomForestClassifier(random_state=42)
    xgb_model = XGBClassifier(random_state=42)
    
    # Hyperparameter grids for GridSearchCV
    rf_params = {
        'n_estimators': [50, 100],  # Reduce the number of trees
        'max_depth': [10, 20],  # Limit max depth
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    xgb_params = {
        'n_estimators': [50, 100],  # Reduce the number of trees
        'max_depth': [3, 6],  # Limit max depth
        'learning_rate': [0.1, 0.2],  # Decrease learning rate
        'subsample': [0.8, 1.0]  # Reduce subsample rate
    }
    
    # Initialize GridSearchCV
    rf_grid_search = GridSearchCV(rf_model, rf_params, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
    xgb_grid_search = GridSearchCV(xgb_model, xgb_params, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
    
    # Fit models to the balanced data
    print("[DEBUG]: Training Random Forest model...")
    rf_grid_search.fit(X_res, y_res)
    
    print("[DEBUG]: Training XGBoost model...")
    xgb_grid_search.fit(X_res, y_res)
    
    return rf_grid_search, xgb_grid_search, X_test, y_test

# Evaluate models and display results
def evaluate_models(rf_grid_search, xgb_grid_search, X_test, y_test):
    """Evaluate Random Forest and XGBoost models"""
    rf_pred = rf_grid_search.best_estimator_.predict(X_test)
    xgb_pred = xgb_grid_search.best_estimator_.predict(X_test)
    
    print(f"Random Forest Accuracy: {accuracy_score(y_test, rf_pred) * 100:.2f}%")
    print(f"XGBoost Accuracy: {accuracy_score(y_test, xgb_pred) * 100:.2f}%")
    
    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, rf_pred))
    
    print("\nXGBoost Classification Report:")
    print(classification_report(y_test, xgb_pred))

# Main function to run the backtesting analysis
def main():
    print("[DEBUG]: Starting the backtesting script...")
    
    # Fetch data from the database
    df = fetch_data()
    
    if df.empty:
        print("[ERROR]: No data to process.")
        return
    
    # Prepare the data
    X, y = prepare_data(df)
    
    # Train models
    rf_grid_search, xgb_grid_search, X_test, y_test = train_models(X, y)
    
    # Evaluate models
    evaluate_models(rf_grid_search, xgb_grid_search, X_test, y_test)
    
    print("[DEBUG]: Backtesting completed.")

# Run the script
if __name__ == "__main__":
    main()
