from flask import Flask, request, jsonify
import pandas as pd
import pickle
import joblib
import numpy as np # Added for numerical operations
import datetime # Added for date/time operations if needed for week_segment/season

app = Flask(__name__)

# --- Load your model and pipeline ---
# Ensure these files are copied into your Docker image (via Dockerfile)
# and the paths are correct relative to where app.py runs inside the container.
try:
    with open("bank_marketing_k-nearest_neighbors.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    pipeline = joblib.load("bank_marketing_prep_pipeline.joblib")
    print("Model and pipeline loaded successfully.")
except Exception as e:
    print(f"Error loading model or pipeline: {e}")
    model = None
    pipeline = None

@app.route("/")
def index():
    return "Bank Marketing Prediction REST API is running."

@app.route("/predict", methods=["POST"])
def predict():
    if not model or not pipeline:
        return jsonify({"error": "Server initialization error: Model or pipeline not loaded."}), 500

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Convert input JSON into DataFrame
    # Ensure it's a list containing the dictionary if you're expecting a single prediction
    df = pd.DataFrame([data])

    # --- FEATURE ENGINEERING (Replicate from your ml_ops.py) ---
    # This is the crucial part you need to fill in accurately.
    # The examples below are educated guesses based on feature names.
    # Replace these with your actual logic from ml_ops.py.

    # Example: is_risk_group (based on age and default)
    # Assuming 'default' is 'yes' or 'no'
    df['is_risk_group'] = ((df['age'] < 25) | (df['default'] == 'yes')).astype(int)

    # Example: economic_pressure_index (based on emp.var.rate and cons.price.idx)
    df['economic_pressure_index'] = df['emp.var.rate'] * df['cons.price.idx']

    # Example: week_segment and season_category (based on month and day_of_week)
    # This requires more complex logic to map month/day_of_week to segments/seasons.
    # You will need to bring in your exact mapping/logic from ml_ops.py.
    # For now, let's use dummy values or basic derivation if not precisely known.
    # You might have a specific mapping (e.g., 'may' -> Q2, 'mon' -> weekday segment)
    month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
                 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    df['month_numeric'] = df['month'].map(month_map)

    def get_week_segment(day_of_week):
        # Example: Simple classification. Replace with your actual logic.
        if day_of_week in ['mon', 'tue', 'wed', 'thu', 'fri']:
            return 'weekday'
        else:
            return 'weekend'
    df['week_segment'] = df['day_of_week'].apply(get_week_segment)

    def get_season_category(month_num):
        # Example: Simple classification. Replace with your actual logic.
        if month_num in [12, 1, 2]: return 'winter'
        elif month_num in [3, 4, 5]: return 'spring'
        elif month_num in [6, 7, 8]: return 'summer'
        else: return 'autumn'
    df['season_category'] = df['month_numeric'].apply(get_season_category)
    df = df.drop(columns=['month_numeric']) # Drop temporary column if created

    # Example: recently_contacted (based on pdays or previous)
    # Assuming pdays == 999 means not previously contacted
    df['recently_contacted'] = (df['pdays'] != 999).astype(int)

    # Example: is_employed (based on job)
    # Assuming 'unemployed' and 'student' are not employed. Adjust based on your definition.
    df['is_employed'] = (~df['job'].isin(['unemployed', 'student'])).astype(int)

    # --- END FEATURE ENGINEERING ---

    # Now, transform the data with the loaded pipeline (which expects all these columns)
    try:
        X_clean = pipeline.transform(df)
    except Exception as e:
        return jsonify({"error": f"Error during pipeline transformation: {e}"}), 500

    # Make prediction
    try:
        pred = model.predict(X_clean)[0]
        # For classification, also return probabilities for more insight
        pred_proba = model.predict_proba(X_clean)[0]
        prediction_no = pred_proba[0] # Probability of "no"
        prediction_yes = pred_proba[1] # Probability of "yes"

        return jsonify({
            "prediction": int(pred),
            "prediction_proba_no": float(prediction_no),
            "prediction_proba_yes": float(prediction_yes)
        })
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {e}"}), 500

if __name__ == "__main__":
    # Ensure debug=False for production environments
    app.run(host="0.0.0.0", port=5000, debug=False)