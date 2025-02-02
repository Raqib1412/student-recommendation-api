import pandas as pd
import ast  # For handling JSON-like data

def extract_topic_title(quiz_data):
    """Extracts the topic title from the nested 'quiz' column"""
    try:
        quiz_dict = ast.literal_eval(quiz_data)  # Convert string to dictionary
        return quiz_dict.get("title", "Unknown")  # Extract topic title
    except (ValueError, SyntaxError):
        return "Unknown"  # Return default if there's an issue

def generate_recommendations(quiz_id, history_df):
    """Generate personalized study recommendations for a given quiz"""
    
    # ✅ Convert quiz_id column to string for accurate filtering
    history_df["quiz_id"] = history_df["quiz_id"].astype(str)
    quiz_id = str(quiz_id)  # Ensure it's a string for matching

    # ✅ Extract topic titles if 'quiz' column exists
    if "quiz" in history_df.columns:
        history_df["topic_title"] = history_df["quiz"].apply(extract_topic_title)
    else:
        print("⚠️ ERROR: 'quiz' column is missing!")
        return {"error": "Quiz column missing", "focus_topics": [], "suggested_resources": []}

    # ✅ Filter data for the given quiz_id
    quiz_history = history_df[history_df["quiz_id"] == quiz_id]

    # ✅ Print data for debugging
    print(f"\n📊 Data for Quiz {quiz_id}:")
    print(quiz_history[["topic_title", "score"]])

    # ✅ Identify weak topics (score < 50)
    weak_topics = quiz_history.groupby("topic_title")["score"].mean()
    weak_topics = weak_topics[weak_topics < 50].index.tolist()

    recommendations = {
        "focus_topics": weak_topics,
        "suggested_resources": ["Concept videos", "Mock tests", "Topic-wise quizzes"]
    }
    
    return recommendations

# ✅ Load historical data
historical_df = pd.read_csv("data/historical_data.csv")

# ✅ Test with a valid quiz_id
valid_quiz_id = "43"  # Replace with a correct quiz_id from historical_data.csv

quiz_recommendations = generate_recommendations(valid_quiz_id, historical_df)

# ✅ Print recommendations
print(f"\n📌 Study Recommendations for Quiz {valid_quiz_id}: {quiz_recommendations}")
