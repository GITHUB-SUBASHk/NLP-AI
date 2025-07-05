#File: actions/actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import time
import json
import redis

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.Redis.from_url(redis_url)

class ActionHandleHelp(Action):
    def name(self) -> Text:
        return "action_handle_help"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Responds to help requests. Extend this method to integrate external APIs or business logic.
        """
        dispatcher.utter_message(text="Sure! I'm here to assist you. Could you describe the issue?")
        # Example: You could add API calls or escalation logic here
        return []

class ActionSetToneProfile(Action):
    def name(self) -> Text:
        return "action_set_tone_profile"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract preferred tone from user message or context (stub: always 'friendly')
        preferred_tone = "friendly"
        dispatcher.utter_message(text=f"Got it! I'll keep my tone {preferred_tone} for you.")
        print(f"[LOG] User {tracker.sender_id} set preferred_tone: {preferred_tone}")
        return [SlotSet("preferred_tone", preferred_tone)]

class ActionDynamicReply(Action):
    def name(self) -> Text:
        return "action_dynamic_reply"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Pull last 3 messages and last intent for memory learning
        last_messages = [e.get("text") for e in tracker.events if e.get("event") == "user" and e.get("text")]
        last_messages = last_messages[-3:]
        last_intent = tracker.latest_message.get("intent", {}).get("name")
        confidence = tracker.latest_message.get("intent", {}).get("confidence", 0.0)
        sender_id = tracker.sender_id
        fallback_triggered = False

        # Example fallback detection (customize as needed)
        if last_intent == "fallback" or confidence < 0.4:
            fallback_triggered = True
            log_entry = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "sender_id": sender_id,
                "event": "fallback",
                "intent": last_intent,
                "confidence": confidence,
                "message": last_messages[-1] if last_messages else "",
                "last_3_messages": last_messages
            }
            redis_client.lpush(f"fallbacks:{sender_id}", json.dumps(log_entry))
            redis_client.ltrim(f"fallbacks:{sender_id}", 0, 49)

        # ... your dynamic reply logic ...
        dispatcher.utter_message(text="Here's a dynamic response based on your recent activity.")
        return [SlotSet("last_intent", last_intent), SlotSet("last_message", last_messages[-1] if last_messages else "")]

# Best practices:
# - Use clear, snake_case action names.
# - Add docstrings to methods.
# - Keep actions stateless; use tracker for context.
# - Return a list of events if you want to set slots or trigger follow-ups.
# - Add more