# File: client/interaction/user_state.py

user_preferences = {}

def set_assist_enabled(user_id: str, enabled: bool):
    if user_id not in user_preferences:
        user_preferences[user_id] = {}
    user_preferences[user_id]["auto_assist"] = enabled

def is_assist_enabled(user_id: str) -> bool:
    return user_preferences.get(user_id, {}).get("auto_assist", False)