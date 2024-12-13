import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
from typing import Dict, Tuple, List, Any
import joblib
from datetime import datetime
import os

class EnhancedMLSystem:
    def __init__(self, save_path: str = 'models/', log_path: str = 'logs/'):
        """
        Initialize the enhanced ML system that combines XGBoost and RandomForest for short-term signals.
        
        Args:
            save_path: Directory to save trained models.
            log_path: Directory to save logs.
        """
        self.models = {
            'xgboost': None,
            'random_forest': None
        }
        self.weights = {
            'xgboost': 0.5,
            'random_forest': 0.5
        }
        self.save_path = save_path
        self.log_path = log_path
        
        # Ensure directories exist
        os.makedirs(self.save_path, exist_ok=True)
        os.makedirs(self.log_path, exist_ok=True)

        self.performance_history = {
            'xgboost': [],
            'random_forest': []
        }

        # Configure logging
        log_filename = os.path.join(self.log_path, f'ml_system_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("EnhancedMLSystem initialized.")

    def prepare_data(self, data: pd.DataFrame, target_col: str, feature_cols: List[str]) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for training or prediction.
        
        Args:
            data: DataFrame containing indicators and a target column.
            target_col: The column name of the target variable (e.g., 'future_up').
            feature_cols: List of indicator column names used as features.
        
        Returns:
            X: Feature matrix
            y: Target series
        """
        # Drop rows with missing values just to simplify
        data = data.dropna(subset=feature_cols + [target_col])
        X = data[feature_cols]
        y = data[target_col]
        return X, y

    def train_models(self, X: pd.DataFrame, y: pd.Series):
        """
        Train the XGBoost and RandomForest models.
        """
        logging.info("Starting model training...")
        
        # Simple train/test split for demonstration
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train XGBoost
        self.models['xgboost'] = xgb.XGBClassifier(
            use_label_encoder=False,
            eval_metric='logloss',
            random_state=42
        )
        self.models['xgboost'].fit(X_train, y_train)
        
        # Train RandomForest
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        self.models['random_forest'].fit(X_train, y_train)
        
        # Evaluate
        y_pred_xgb = self.models['xgboost'].predict(X_test)
        y_pred_rf = self.models['random_forest'].predict(X_test)
        
        acc_xgb = accuracy_score(y_test, y_pred_xgb)
        acc_rf = accuracy_score(y_test, y_pred_rf)

        self.performance_history['xgboost'].append(acc_xgb)
        self.performance_history['random_forest'].append(acc_rf)

        logging.info(f"XGBoost Accuracy: {acc_xgb:.4f}")
        logging.info(f"RandomForest Accuracy: {acc_rf:.4f}")

        # Save models
        joblib.dump(self.models['xgboost'], os.path.join(self.save_path, 'xgboost_model.joblib'))
        joblib.dump(self.models['random_forest'], os.path.join(self.save_path, 'random_forest_model.joblib'))
        logging.info("Models saved successfully.")

    def load_models(self):
        """
        Load pre-trained models from save_path if they exist.
        """
        xgb_path = os.path.join(self.save_path, 'xgboost_model.joblib')
        rf_path = os.path.join(self.save_path, 'random_forest_model.joblib')
        
        if os.path.exists(xgb_path):
            self.models['xgboost'] = joblib.load(xgb_path)
            logging.info("XGBoost model loaded.")
        if os.path.exists(rf_path):
            self.models['random_forest'] = joblib.load(rf_path)
            logging.info("RandomForest model loaded.")

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make ensemble predictions using both models and weighted averaging.
        
        Args:
            X: Feature matrix for prediction
        
        Returns:
            Probabilities or predictions as a numpy array
        """
        # Predict probabilities for better ranking of top 20 coins
        if self.models['xgboost'] is None or self.models['random_forest'] is None:
            logging.warning("Models not loaded or trained, returning zeros.")
            return np.zeros(len(X))
        
        xgb_probs = self.models['xgboost'].predict_proba(X)[:,1]
        rf_probs = self.models['random_forest'].predict_proba(X)[:,1]

        # Weighted average
        final_probs = self.weights['xgboost'] * xgb_probs + self.weights['random_forest'] * rf_probs
        return final_probs

    def select_top_20_coins(self, data: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
        """
        Given a set of current coin data and features, predict which will perform best and select the top 20.
        
        Args:
            data: DataFrame with at least coin_symbol and feature_cols.
            feature_cols: List of features for prediction.
        
        Returns:
            A DataFrame of the top 20 coins with their predicted probabilities.
        """
        # Clean data and drop missing features
        data = data.dropna(subset=feature_cols)
        
        if len(data) < 20:
            logging.warning("Less than 20 coins available, selecting all.")
            X = data[feature_cols]
            data['predicted_prob'] = self.predict(X)
            return data.sort_values('predicted_prob', ascending=False)
        
        X = data[feature_cols]
        data['predicted_prob'] = self.predict(X)
        top_20 = data.sort_values('predicted_prob', ascending=False).head(20)
        return top_20

    def backtest(self, historical_data: pd.DataFrame, feature_cols: List[str], target_col: str, initial_capital: float = 1000.0) -> float:
        """
        A simple backtest:
        - Assume we pick top 20 coins today based on predictions.
        - Equally allocate capital among them.
        - Evaluate performance after a given period (e.g., next day's close).
        
        This is a simplified example. In practice, you'd integrate more complex logic.
        
        Args:
            historical_data: DataFrame with historical data, including features and target. Must have:
                - 'coin_symbol'
                - 'close' price
                - 'time' or some datetime index
            feature_cols: Columns used for prediction.
            target_col: The column indicating if next period is profitable.
            initial_capital: Starting capital for the backtest.
        
        Returns:
            final_portfolio_value: The portfolio value after the holding period.
        """
        # For simplicity, let's pick a single "as-of" date (last row) to simulate decision-making
        # In reality, you'd run a loop over multiple periods.
        
        # Sort by time and pick the second to last row as 'decision point'
        historical_data = historical_data.sort_values('time')
        decision_data = historical_data.iloc[-2].time
        # Filter data for decision day
        decision_set = historical_data[historical_data['time'] == decision_data]
        
        # Select top 20 coins based on model predictions at decision time
        top_20 = self.select_top_20_coins(decision_set, feature_cols)
        
        # Allocate capital equally
        if len(top_20) == 0:
            logging.warning("No coins selected for backtest.")
            return initial_capital
        
        allocation_per_coin = initial_capital / len(top_20)
        
        # We assume the next row of data (the last row) represents the "outcome"
        outcome_data = historical_data.iloc[-1]
        outcome_time = outcome_data.time
        
        # We'll assume the closing price at 'outcome_time' is what we can sell at.
        final_portfolio_value = 0.0
        for idx, coin in top_20.iterrows():
            symbol = coin['coin_symbol']
            initial_price = coin['close']  # price at decision time
            # Find outcome price for this coin at outcome_time
            coin_outcome = historical_data[(historical_data['coin_symbol'] == symbol) & (historical_data['time'] == outcome_time)]
            if len(coin_outcome) > 0:
                final_price = coin_outcome['close'].values[0]
            else:
                # If no data at outcome time, assume price unchanged (very naive)
                final_price = initial_price
            
            # Calculate return
            shares = allocation_per_coin / initial_price
            final_portfolio_value += shares * final_price
        
        profit = final_portfolio_value - initial_capital
        roi = (final_portfolio_value / initial_capital - 1) * 100
        logging.info(f"Backtest completed. Initial capital: ${initial_capital:.2f}, Final capital: ${final_portfolio_value:.2f}, Profit: ${profit:.2f}, ROI: {roi:.2f}%")
        
        return final_portfolio_value

if __name__ == "__main__":
    # Example usage (this would be replaced by your actual data loading and pipeline steps)
    # Just a mock example.
    # NOTE: Replace this with your actual data loading logic.
    mock_data = pd.DataFrame({
        'coin_symbol': ['BTC', 'ETH', 'XRP', 'LTC'] * 30,
        'time': pd.date_range("2024-12-01", periods=120, freq='H'),
        'close': np.random.uniform(100, 200, 120),
        'indicator1': np.random.rand(120),
        'indicator2': np.random.rand(120),
        'future_up': np.random.randint(0, 2, 120)  # Random buy/sell signal for demo
    })

    feature_cols = ['indicator1', 'indicator2']
    target_col = 'future_up'
    
    system = EnhancedMLSystem()
    X, y = system.prepare_data(mock_data, target_col, feature_cols)
    system.train_models(X, y)
    system.load_models()
    final_value = system.backtest(mock_data, feature_cols, target_col, initial_capital=1000.0)
    print("Backtest final portfolio value:", final_value)
