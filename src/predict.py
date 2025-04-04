import joblib
import pandas as pd

# Load trained model
model = joblib.load("F:/SaiU/semester 4/Sri/models/packing_model.pkl")

# Function to take user input and predict packaging
def predict_packaging():
    print("\n📦 Enter Product Details for Packaging Prediction:")
    
    weight = float(input("Enter Weight (kg): "))
    length = float(input("Enter Length (cm): "))
    width = float(input("Enter Width (cm): "))
    height = float(input("Enter Height (cm): "))

    # Compute volume
    volume = length * width * height

    # Create DataFrame for model
    input_data = pd.DataFrame([[weight, length, width, height, volume]],
                          columns=["Weight (kg)", "Length", "Width", "Height", "Volume"])


    # Predict packaging material
    prediction = model.predict(input_data)[0]
    
    print(f"\n✅ Recommended Packaging Material: {prediction}")

# Run the prediction function
if __name__ == "__main__":
    predict_packaging()
