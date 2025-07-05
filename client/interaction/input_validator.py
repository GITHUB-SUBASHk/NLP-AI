import re

def sanitize_input(message: str) -> str:
    """
    Sanitize input message by stripping harmful content and reducing noise.
    """
    message = re.sub(r"<.*?>", "", message)  # Remove HTML tags
    message = message.strip()
    return message

def is_valid_message(message: str) -> bool:
    """
    Basic check for valid user input.
    """
    return bool(message) and len(message) > 1