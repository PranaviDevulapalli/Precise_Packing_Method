import joblib
import pandas as pd

# Load trained model
model = joblib.load("F:/SaiU/semester 4/Sri/models/packing_model.pkl")

# ✅ Check how many features the model expects
print(f"🔍 Model expects {model.n_features_in_} features.")

# Function to take user input and predict packaging
def predict_packaging():
    print("\n📦 Enter Product Details for Packaging Prediction:")
    
    weight = float(input("Enter Weight (kg): "))
    length = float(input("Enter Length (cm): "))
    width = float(input("Enter Width (cm): "))
    height = float(input("Enter Height (cm): "))
    
    # Compute volume
    volume = length * width * height

    # ✅ Ensure input matches the model’s expected feature count
    if model.n_features_in_ == 5:
        input_data = pd.DataFrame([[weight, length, width, height, volume]],
                                  columns=["Weight (kg)", "Length", "Width", "Height", "Volume"])
    elif model.n_features_in_ == 4:
        input_data = pd.DataFrame([[weight, length, width, height]],
                                  columns=["Weight (kg)", "Length", "Width", "Height"])
    else:
        raise ValueError(f"❌ Unexpected number of features: {model.n_features_in_}")

    # Predict packaging material
    prediction = model.predict(input_data)[0]
    
    print(f"\n✅ Recommended Packaging Material: {prediction}")

# Run the prediction function
if __name__ == "__main__":
    predict_packaging()
