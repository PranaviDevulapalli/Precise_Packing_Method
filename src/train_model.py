import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Load the preprocessed data
df = pd.read_csv("data/processed_data.csv")

# 📋 Define features and target
features = ['length_inc', 'width_inc', 'height_inc', 'weight_kg']
target = 'volume_cm3'

# Split data into train and test sets
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/volume_predictor.pkl")

print("✅ Model training completed and saved to 'models/volume_predictor.pkl'")
