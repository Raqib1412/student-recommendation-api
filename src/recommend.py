import pandas as pd
import ast  # For handling nested JSON

def extract_topic_title(quiz_data):
    """Extracts the topic title from the nested 'quiz' column"""
    try:
        quiz_dict = ast.literal_eval(quiz_data)  # Convert string to dictionary
        return quiz_dict.get("title", "Unknown")  # Extract topic title
    except (ValueError, SyntaxError):
        return "Unknown"  # Return default if there's an issue

def generate_recommendations(user_id, history_df):
    """Generate personalized study recommendations for a student"""
    
    # ✅ Convert user_id column to string for accurate filtering
    history_df["user_id"] = history_df["user_id"].astype(str)
    user_id = str(user_id)  # Ensure it's a string for matching

    # ✅ Extract topic titles if 'quiz' column exists
    if "quiz" in history_df.columns:
        history_df["topic_title"] = history_df["quiz"].apply(extract_topic_title)
    else:
        print("⚠️ ERROR: 'quiz' column is missing!")
        return {"error": "Quiz column missing", "focus_topics": [], "suggested_resources": []}

    # ✅ Filter data for the given user
    user_history = history_df[history_df["user_id"] == user_id]

    # ✅ Print user data for debugging
    print(f"\n👤 Full Data for User {user_id}:")
    print(user_history[["topic_title", "score"]])

    # ✅ Identify weak topics (score < 50)
    weak_topics = user_history.groupby("topic_title")["score"].mean()
    weak_topics = weak_topics[weak_topics < 50].index.tolist()

    recommendations = {
        "focus_topics": weak_topics,
        "suggested_resources": ["Concept videos", "Mock tests", "Topic-wise quizzes"]
    }
    
    return recommendations

# ✅ Load historical data
historical_df = pd.read_csv("data/historical_data.csv")

# ✅ Use the verified user ID
valid_user_id = "YcDFSO4ZukTJnnFMgRNVwZTE4j42"  # Replace with the confirmed correct user ID

# ✅ Run the recommendation function
user_recommendations = generate_recommendations(valid_user_id, historical_df)

# ✅ Print recommendations
print(f"\n📌 Study Recommendations for User {valid_user_id}: {user_recommendations}")
