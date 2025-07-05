from collections import defaultdict

# In-memory user style/behavior learning (pseudo-learning)
user_memory = defaultdict(lambda: {
    "preferred_tone": "neutral",
    "response_style": "direct",
    "known_facts": []
})

def get_user_profile(user_id: str) -> dict:
    """Retrieve the user's profile dictionary."""
    return user_memory[user_id]

def update_user_profile(user_id: str, key: str, value):
    """Update a specific key in the user's profile."""
    user_memory[user_id][key] = value

def add_fact(user_id: str, fact: str):
    """Add a new fact to the user's known facts if not already present."""
    if fact not in user_memory[user_id]["known_facts"]:
        user_memory[user_id]["known_facts"].append(fact)

def clear_user_profile(user_id: str):
    """Remove the user's profile from memory."""
    if user_id in user_memory:
        del user_memory[user_id]