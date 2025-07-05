# Optional for future real-time tracking of active sessions, events, presence, etc.

user_sessions = {}

def track_event(user_id: str, event: str):
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    user_sessions[user_id].append(event)

def get_events(user_id: str):
    return user_sessions.get(user_id, [])