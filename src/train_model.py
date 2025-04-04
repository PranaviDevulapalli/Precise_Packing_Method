import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load preprocessed data
df = pd.read_csv("F:/SaiU/semester 4/Sri/data/processed_data.csv")

# Select features for model training
features = ["Weight (kg)", "Length", "Width", "Height", "Volume"]
target = "Material Properties"  # Change this if needed

# Drop rows with missing values
df.dropna(subset=features + [target], inplace=True)

# Split dataset into train and test sets
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save trained model
joblib.dump(model, "F:/SaiU/semester 4/Sri/models/packing_model.pkl")
print("Model saved successfully!")
