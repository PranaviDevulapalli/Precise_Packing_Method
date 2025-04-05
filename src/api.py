from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load("models/volume_predictor.pkl")

@app.route('/')
def index():
    return "📦 AI Packaging Optimization API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Required input features
        required_fields = ['length_inc', 'width_inc', 'height_inc', 'weight_kg']

        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f"Missing fields in request: {', '.join(missing_fields)}"
            }), 400

        # Extract feature values
        features = np.array([[ 
            float(data['length_inc']),
            float(data['width_inc']),
            float(data['height_inc']),
            float(data['weight_kg'])
        ]])

        # Make prediction
        predicted_volume = model.predict(features)[0]

        return jsonify({
            'predicted_volume_cm3': round(predicted_volume, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
