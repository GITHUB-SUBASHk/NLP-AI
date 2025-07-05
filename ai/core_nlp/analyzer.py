import random
import json
import os
from textblob import TextBlob
from typing import Tuple

TONE_PATH = os.path.join("data", "tone_rules.json")

with open(TONE_PATH, "r") as f:
    tone_data = json.load(f)["tones"]

EMOTION_KEYWORDS = {
    "happy": ["yay", "awesome", "great", "glad"],
    "sad": ["sad", "unhappy", "depressed"],
    "angry": ["mad", "angry", "furious"],
    "curious": ["wonder", "curious", "question"]
}

def detect_tone(message: str) -> str:
    message_lower = message.lower()
    for tone, rules in tone_data.items():
        for keyword in rules["keywords"]:
            if keyword in message_lower:
                return tone
    return "neutral"

def analyze_tone(message: str) -> str:
    """Detect tone using TextBlob polarity."""
    polarity = TextBlob(message).sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.3:
        return "negative"
    else:
        return "neutral"

def detect_emotion(message: str) -> str:
    """Detect emotion based on keywords."""
    msg = message.lower()
    for emotion, words in EMOTION_KEYWORDS.items():
        if any(w in msg for w in words):
            return emotion
    return "neutral"

def detect_purpose(message: str) -> str:
    """Detect the purpose of a message (question, support, request, statement)."""
    msg = message.lower()
    if "?" in msg:
        return "question"
    elif any(w in msg for w in ["help", "issue", "support"]):
        return "support"
    elif msg.startswith("i want") or msg.startswith("can you"):
        return "request"
    return "statement"

def analyze_tone_and_purpose(message: str) -> Tuple[str, str]:
    """
    Analyze both tone and purpose for a message.
    Returns (tone, purpose).
    """
    tone = analyze_tone(message)
    purpose = detect_purpose(message)
    return tone, purpose

def get_response_tint(tone: str) -> str:
    """Get response tint from tone_rules.json if available."""
    if "tones" in tone_data and tone in tone_data["tones"]:
        return tone_data["tones"][tone].get("response_tint", "neutral")
    return "neutral"