from ai.core_nlp.analyzer import analyze_tone_and_purpose
from ai.core_nlp.intent_classifier import detect_intent
from ai.memory.session_context import SessionContext
from ai.memory.learning_memory import LearningMemory

class ReplyGenerator:
    def __init__(self):
        self.session = SessionContext()
        self.learner = LearningMemory()

    def generate(self, user_id: str, message: str) -> str:
        # Analyze message
        tone, purpose = analyze_tone_and_purpose(message)
        intent = detect_intent(message)

        # Update memory context
        self.session.update_context(user_id, message, intent, tone)
        self.learner.learn_from_message(user_id, message)

        # Generate reply based on intent
        if intent == "greeting":
            return "Hello! How can I assist you today?"
        elif intent == "help_request":
            return "Sure, I'm here to help. Please explain what you need."
        elif intent == "farewell":
            return "Goodbye! Feel free to reach out anytime."
        elif intent == "emotion":
            return f"I sense you're feeling {tone}. Want to talk about it?"
        else:
            return "I’m processing your message. Let me think..."

# Example usage:
# reply_gen = ReplyGenerator()
# response = reply_gen.generate(user_id="user123", message="I need help with a project")
