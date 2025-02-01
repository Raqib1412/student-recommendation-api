import json

HISTORICAL_JSON_FILE = "data/historical_data.json"

# ✅ Load historical data
with open(HISTORICAL_JSON_FILE, "r") as file:
    historical_data = json.load(file)

# ✅ Print all user IDs from historical JSON file
user_ids = [str(item["user_id"]) for item in historical_data if "user_id" in item]
print("\n👤 Users in historical_data.json:", user_ids)
