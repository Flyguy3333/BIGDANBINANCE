import xgboost as xgb
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load sample dataset
data = load_boston()
X, y = data.data, data.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create DMatrix for XGBoost
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Set XGBoost parameters
params = {
    "objective": "reg:squarederror",  # Regression task
    "max_depth": 4,
    "eta": 0.1,  # Learning rate
    "verbosity": 1,
}

# Train the model
model = xgb.train(params, dtrain, num_boost_round=50)

# Predict on test data
y_pred = model.predict(dtest)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Root Mean Squared Error (RMSE): {rmse}")
