import joblib
import numpy as np
import xgboost as xgb
from flask import Flask, request, jsonify
import os

# Get absolute paths
model_path = os.path.abspath("xgboost_model.pkl")
scaler_path = os.path.abspath("scaler.pkl")  # Load the same scaler used in training

print(f"Loading model from: {model_path}")
print(f"Loading scaler from: {scaler_path}")

# Load model and scaler
model = joblib.load(model_path, mmap_mode="r")
scaler = joblib.load(scaler_path)  # Load the MinMaxScaler or StandardScaler

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask API for Stock Prediction is Running!"

@app.route("/predict", methods=["POST", "GET"])
def predict():
    try:
        if request.method == "GET":
            return jsonify({"message": "Use POST with JSON data to get the predictions "}), 200

        # Get JSON data from request
        data = request.get_json()

        # Ensure data is in correct format (list of feature values)
        features = np.array(data["features"]).reshape(1, -1)

        # Scale the input features before prediction
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)

        # Return prediction as JSON response
        return jsonify({"prediction": prediction.tolist()})
    
    except Exception as e:
        return jsonify({"error": str(e)})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
