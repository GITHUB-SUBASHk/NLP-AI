from ai.plugins.base_plugin import BasePlugin

class Plugin(BasePlugin):
    def meta(self):
        return {
            "name": "HelloPlugin",
            "version": "1.0",
            "author": "Subash"
        }

    def should_handle(self, intent: str) -> bool:
        return intent == "greet"

    def run(self, message: str, sender_id: str) -> str:
        return f"👋 Hello, {sender_id}! Plugin says hi."