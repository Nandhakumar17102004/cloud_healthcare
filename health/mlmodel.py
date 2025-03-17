import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify

# Load the kidney disease model
with open("kidney_model.pkl", "rb") as file:
    kidney_model = pickle.load(file)

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Kidney Disease Prediction API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from the request
        data = request.get_json()
        input_features = np.array(data["features"]).reshape(1, -1)  # Expecting a list of features

        # Make prediction
        prediction = kidney_model.predict(input_features)
        result = int(prediction[0])  # Convert output to an integer

        # Define result labels
        disease_labels = {0: "No Kidney Disease", 1: "Chronic Kidney Disease"}

        return jsonify({
            "disease": "kidney",
            "prediction": disease_labels.get(result, "Unknown Result")
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
