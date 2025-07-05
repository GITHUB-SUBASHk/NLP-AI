import re

def anonymize(message: str) -> str:
    """
    Anonymizes personal identifiers in the message.
    """
    message = re.sub(r"\b\d{10}\b", "[PHONE]", message)
    message = re.sub(r"\b\w+@\w+\.\w+\b", "[EMAIL]", message)
    return message