from flask import Flask, jsonify, request
import pandas as pd
from src.recommend import generate_recommendations

app = Flask(__name__)

# ✅ Load Historical Data
historical_df = pd.read_csv("data/historical_data.csv")

@app.route('/recommend', methods=['GET'])
def recommend():
    """API to return study recommendations for a student"""
    user_id = request.args.get('user_id', type=str)  # Get user_id from URL

    if user_id:
        recommendations = generate_recommendations(user_id, historical_df)
        return jsonify(recommendations)
    
    return jsonify({"error": "No user ID provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
