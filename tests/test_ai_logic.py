from ai.core_nlp.analyzer import analyze_tone
from ai.assistant_engine.ai_router import route_message

def test_analyze_tone_positive():
    assert analyze_tone("Wow I love this!") in ("positive", "happy")

def test_analyze_tone_negative():
    assert analyze_tone("I am very sad today") in ("negative", "sad")

def test_route_message_returns_string():
    reply = route_message("Tell me a joke", user_id="test_user")
    assert isinstance(reply, str)
    assert reply  # Should not be empty