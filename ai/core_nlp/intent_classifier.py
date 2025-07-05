import json
import random
from difflib import get_close_matches
from typing import List, Dict

INTENTS_PATH = "data/intents.json"

def load_intents(path: str = INTENTS_PATH) -> List[Dict]:
    """Load intent patterns and responses from a JSON file."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

intent_db = load_intents()

def classify_intent(message: str) -> str:
    """
    Classify the intent of a message using pattern matching.
    Returns the intent tag or 'unknown'.
    """
    msg = message.strip().lower()
    for intent in intent_db:
        patterns = [p.lower() for p in intent.get("patterns", [])]
        if get_close_matches(msg, patterns, cutoff=0.7):
            return intent.get("tag", "unknown")
    return "unknown"

def get_intent_response(intent: str) -> str:
    """
    Get a random response for a given intent tag.
    """
    for item in intent_db:
        if item.get("tag") == intent:
            responses = item.get("responses", [])
            if responses:
                return random.choice(responses)
    return "Sorry, I didn’t get that."
