import pandas as pd
import ast  # For converting string representation of dictionaries
import matplotlib.pyplot as plt
import seaborn as sns

# Load historical quiz data
historical_df = pd.read_csv("data/historical_data.csv")

# ✅ Print available columns
print("\n📂 Available columns in historical_data.csv:")
print(historical_df.columns.tolist())

# ✅ Convert the 'quiz' column from string to dictionary (if necessary)
def extract_topic_title(quiz_data):
    """Extracts the topic title from the nested 'quiz' column"""
    try:
        quiz_dict = ast.literal_eval(quiz_data)  # Convert string to dictionary
        return quiz_dict.get("title", "Unknown")  # Extract topic title
    except (ValueError, SyntaxError):
        return "Unknown"  # Return default if there's an issue

# Apply the function to extract topic titles
historical_df["topic_title"] = historical_df["quiz"].apply(extract_topic_title)

# ✅ Print updated DataFrame
print("\n📝 Updated Data with Extracted Topics:")
print(historical_df[["user_id", "score", "topic_title"]].head())

# 📊 Analyze average performance per topic
topic_performance = historical_df.groupby("topic_title")["score"].mean()

# 📊 Plot Performance
plt.figure(figsize=(10, 5))
sns.barplot(x=topic_performance.index, y=topic_performance.values)
plt.title("📊 Average Score per Topic")
plt.xlabel("Topic Title")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.show()

# Identify weak topics (score < 50%)
weak_topics = topic_performance[topic_performance < 50].index.tolist()
print("🚨 Weak Topics (Needs Improvement):", weak_topics)
