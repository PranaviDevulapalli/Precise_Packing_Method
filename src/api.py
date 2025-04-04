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

import joblib
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API is working!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# Correct path for Render deployment
model_path = os.path.join(os.path.dirname(__file__), "models\packing_model.pkl")

# Load the model
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")


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
