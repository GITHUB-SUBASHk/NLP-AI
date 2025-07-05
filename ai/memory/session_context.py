from collections import defaultdict
import time
from typing import Any, Dict

# Thread-safe for dev; swap for Redis/DB in prod
session_store = defaultdict(dict)

def get_context(user_id: str) -> Dict[str, Any]:
    return session_store[user_id]

def update_context(user_id: str, key: str, value: Any):
    session_store[user_id][key] = value
    session_store[user_id]["last_updated"] = time.time()

def clear_context(user_id: str):
    if user_id in session_store:
        del session_store[user_id]