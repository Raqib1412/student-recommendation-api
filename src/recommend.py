import pandas as pd
import ast  # For handling JSON-like data

def extract_topic_title(quiz_data):
    """Extracts the topic title from the nested 'quiz' column"""
    try:
        quiz_dict = ast.literal_eval(quiz_data)  # Convert string to dictionary
        return quiz_dict.get("title", "Unknown")  # Extract topic title
    except (ValueError, SyntaxError):
        return "Unknown"  # Return default if there's an issue

def generate_recommendations(entry_id, history_df):
    """Generate personalized study recommendations based on `id`"""
    
    # ✅ Convert `id` column to string for accurate filtering
    history_df["id"] = history_df["id"].astype(str)
    entry_id = str(entry_id)  # Ensure it's a string for matching

    # ✅ Extract topic titles if 'quiz' column exists
    if "quiz" in history_df.columns:
        history_df["topic_title"] = history_df["quiz"].apply(extract_topic_title)
    else:
        print("⚠️ ERROR: 'quiz' column is missing!")
        return {"error": "Quiz column missing", "focus_topics": [], "suggested_resources": []}

    # ✅ Filter data for the given `id`
    entry_history = history_df[history_df["id"] == entry_id]

    # 🔍 **Debugging Print Statements**
    print("\n🔍 Debug: Entry History for ID:", entry_id)
    print(entry_history[["topic_title", "score"]])

    if entry_history.empty:
        print("❌ ERROR: ID not found in historical data!")
        return {"error": "ID not found in historical data", "focus_topics": [], "suggested_resources": []}

    # ✅ Identify weak topics (score < 50)
    weak_topics = entry_history.groupby("topic_title")["score"].mean()
    weak_topics = weak_topics[weak_topics < 50].index.tolist()

    print("\n✅ Weak Topics Identified:", weak_topics)  # 🔍 Debugging Output

    recommendations = {
        "focus_topics": weak_topics,
        "suggested_resources": ["Concept videos", "Mock tests", "Topic-wise quizzes"]
    }
    
    return recommendations

# ✅ Load historical data
historical_df = pd.read_csv("data/historical_data.csv")

# ✅ Test with a valid `id`
valid_entry_id = "336497"  # Replace with a correct `id` from historical_data.csv

entry_recommendations = generate_recommendations(valid_entry_id, historical_df)

# ✅ Print recommendations
print(f"\n📌 Study Recommendations for Entry ID {valid_entry_id}: {entry_recommendations}")
