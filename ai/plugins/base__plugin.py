from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """
    Abstract base class for all plugins in the AI assistant system.
    All plugins must inherit from this class and implement the required methods.
    """

    @abstractmethod
    def meta(self) -> dict:
        """
        Return metadata about the plugin (name, author, version, etc).
        Example:
            return {
                "name": "MyPlugin",
                "version": "1.0",
                "author": "Your Name"
            }
        """
        raise NotImplementedError("Plugin must implement meta()")

    @abstractmethod
    def should_handle(self, intent: str) -> bool:
        """
        Decide whether this plugin should handle a given intent.
        Return True if this plugin is responsible for the intent.
        """
        raise NotImplementedError("Plugin must implement should_handle()")

    @abstractmethod
    def run(self, message: str, sender_id: str) -> str:
        """
        Run the plugin logic and return a text reply.
        """
        raise NotImplementedError("Plugin must implement run()")