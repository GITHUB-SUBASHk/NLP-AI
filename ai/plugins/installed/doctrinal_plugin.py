# File: ai/plugins/installed/doctrinal_plugin.py

from ai.plugins.base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Plugin to handle religious or philosophical questions.
    """

    def should_handle(self, intent: str) -> bool:
        return intent.lower() in {"doctrine_query", "religion", "spirituality"}

    def run(self, message: str, sender_id: str) -> str:
        return (
            "🕊️ As per many teachings, clarity comes from within. "
            "Meditate on your question and seek wisdom through reflection and study."
        )

    def meta(self) -> dict:
        return {
            "name": "DoctrinalPlugin",
            "description": "Answers philosophical and religious queries",
            "version": "1.0",
            "author": "System"
        }