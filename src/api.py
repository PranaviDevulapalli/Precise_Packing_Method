# # Enhancing the AI Packaging Model by integrating a Flask API so we can:

# # ✅ Make predictions via a Web API
# # ✅ Send & receive packaging recommendations from other applications
# # ✅ Future-proof for web and mobile integration
# Set up a Flask API to handle packaging predictions

# Users can send product details via an API request

# API returns the recommended packaging material
from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load trained model
model = joblib.load("F:/SaiU/semester 4/Sri/models/packing_model.pkl")

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "AI Packaging Model API is running!"})

@app.route("/predict", methods=["POST"])

def predict():
    try:
        # Get JSON data from request
        data = request.json

        # Extract input values
        weight = float(data["weight"])
        length = float(data["length"])
        width = float(data["width"])
        height = float(data["height"])

        # Compute volume
        volume = length * width * height

        # Create DataFrame
        input_data = pd.DataFrame([[weight, length, width, height, volume]],
                                  columns=["Weight (kg)", "Length", "Width", "Height", "Volume"])

        # Predict packaging material
        prediction = model.predict(input_data)[0]

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
