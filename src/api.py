import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Define model path correctly
model_path = os.path.join(os.path.dirname(__file__), "models", "packing_model.pkl")
model_path = os.path.abspath(model_path)

# ✅ Ensure the model file exists before loading
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found: {model_path}")

# ✅ Load the model safely
try:
    model = joblib.load(model_path)
    print("✅ Model loaded successfully!")
    print(f"🔍 Model expects {model.n_features_in_} features.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None  # Prevent crashes if model loading fails

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Packing Prediction API!"})

# ✅ Rename function to avoid conflict
@app.route("/predict", methods=["POST"])
def predict_material():
    if model is None:
        return jsonify({"error": "Model is not loaded properly."}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        required_fields = ["weight", "length", "width", "height"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

        # ✅ Compute Volume
        volume = data["length"] * data["width"] * data["height"]

        # ✅ Ensure input matches model's expected feature count
        if model.n_features_in_ == 5:
            features = [[data["weight"], data["length"], data["width"], data["height"], volume]]
        elif model.n_features_in_ == 4:
            features = [[data["weight"], data["length"], data["width"], data["height"]]]
        else:
            return jsonify({"error": f"Unexpected number of features: {model.n_features_in_}"}), 500

        prediction = model.predict(features)[0]

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
