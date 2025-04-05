import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/packing_model.pkl")

def predict_custom():
    print("📦 Enter product dimensions for package class prediction:")

    # User input
    weight = float(input("Weight (kg): "))
    length = float(input("Length (inc): "))
    width = float(input("Width (inc): "))
    height = float(input("Height (inc): "))

    # Feature engineering
    volume_cm3 = length * width * height
    density = weight / volume_cm3 if volume_cm3 != 0 else 0

    # Input DataFrame
    input_data = pd.DataFrame([{
        'weight': weight,
        'length': length,
        'width': width,
        'height': height,
        'volume_cm3': volume_cm3,
        'density': density
    }])

    # Predict
    prediction = model.predict(input_data)[0]
    print(f"\n✅ Predicted Package Class: **{prediction}**")

if __name__ == "__main__":
    predict_custom()
