from client.privacy.anonymizer import anonymize

def enforce_privacy(message: str) -> str:
    """
    Apply anonymization rules to a message before storage or processing.
    """
    return anonymize(message)