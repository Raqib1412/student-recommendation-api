from flask import Flask, jsonify, request
import pandas as pd
from src.recommend import generate_recommendations
import os  

app = Flask(__name__)

# ✅ Load Historical Data
historical_df = pd.read_csv("data/historical_data.csv")

@app.route('/recommend', methods=['GET'])
def recommend():
    """API to return study recommendations for a quiz"""
    quiz_id = request.args.get('quiz_id', type=str)  # Get quiz_id from URL

    if quiz_id:
        recommendations = generate_recommendations(quiz_id, historical_df)
        return jsonify(recommendations)
    
    return jsonify({"error": "No quiz ID provided"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get port from Render
    app.run(host="0.0.0.0", port=port, debug=True)  # ✅ Fix: Bind to 0.0.0.0
