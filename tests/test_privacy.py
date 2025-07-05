from client.privacy.privacy_guard import is_safe
from client.privacy.anonymizer import anonymize

def test_is_safe_true():
    safe_text = "Hello, how are you?"
    assert is_safe(safe_text) is True

def test_is_safe_false():
    unsafe_text = "Here is my credit card number 1234-5678-9012-3456"
    assert is_safe(unsafe_text) is False

def test_anonymize():
    input_text = "My email is test@example.com and phone 9876543210"
    output = anonymize(input_text)
    assert "[email]" in output or "[phone]" in output

def test_email_anonymization():
    text = "My email is john@example.com"
    clean = anonymize(text)
    assert "john@example.com" not in clean
    assert "[email]" in clean or "@" not in clean

def test_name_anonymization():
    text = "My name is John"
    clean = anonymize(text)
    assert "John" not in clean