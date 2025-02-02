from flask import Flask, jsonify, request
import pandas as pd
from src.recommend import generate_recommendations
import os  

app = Flask(__name__)

# ✅ Load Historical Data
historical_df = pd.read_csv("data/historical_data.csv")

@app.route('/recommend', methods=['GET'])
def recommend():
    """API to return study recommendations based on `id`"""
    entry_id = request.args.get('id', type=str)  # ✅ Get `id` from the query parameter

    if entry_id:
        recommendations = generate_recommendations(entry_id, historical_df)
        return jsonify(recommendations)  # ✅ Return recommendations for `id`
    
    return jsonify({"error": "No ID provided"}), 400  # ✅ Fix error message

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get port from Render
    app.run(host="0.0.0.0", port=port, debug=True)  # ✅ Bind to 0.0.0.0
