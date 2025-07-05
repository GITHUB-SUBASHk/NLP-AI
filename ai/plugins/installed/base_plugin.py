# File: ai/plugins/base_plugin.py

from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    Abstract base class for all AI assistant plugins.
    Each plugin must define how it handles specific intents and returns a response.
    """

    def __init__(self):
        """
        Optional setup logic for plugin initialization.
        Override in child classes if needed.
        """
        pass

    @abstractmethod
    def should_handle(self, intent: str) -> bool:
        """
        Returns True if this plugin should handle the given intent.
        """
        raise NotImplementedError("Plugin must implement should_handle()")

    @abstractmethod
    def run(self, message: str, sender_id: str) -> str:
        """
        Execute plugin logic and return a response string.
        """
        raise NotImplementedError("Plugin must implement run()")

    @abstractmethod
    def meta(self) -> dict:
        """
        Returns metadata about the plugin (name, description, version, etc).
        """
        raise NotImplementedError("Plugin must implement meta()")