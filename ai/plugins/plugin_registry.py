"""
Plugin Registry for AI Assistant

- Register which intents are handled by which plugin.
- Enable/disable plugins per user.
- Query enabled plugins for a user.
"""

from collections import defaultdict

# In-memory intent-to-plugin mapping
_intent_plugin_map = defaultdict(set)  # intent -> set of plugin names

# In-memory per-user plugin enablement
_user_plugin_enabled = defaultdict(set)  # user_id -> set of enabled plugin names

def register_plugin_intents(plugin_name: str, intents: list[str]):
    """
    Register a plugin as handling a list of intents.
    """
    for intent in intents:
        _intent_plugin_map[intent].add(plugin_name)

def get_plugins_for_intent(intent: str) -> list[str]:
    """
    Return list of plugin names that handle a given intent.
    """
    return list(_intent_plugin_map.get(intent, []))

def is_plugin_enabled(user_id: str, plugin_name: str) -> bool:
    """
    Check if a plugin is enabled for a user.
    """
    return plugin_name in _user_plugin_enabled[user_id]

def enable_plugin(user_id: str, plugin_name: str):
    """
    Enable a plugin for a user.
    """
    _user_plugin_enabled[user_id].add(plugin_name)

def disable_plugin(user_id: str, plugin_name: str):
    """
    Disable a plugin for a user.
    """
    _user_plugin_enabled[user_id].discard(plugin_name)

def list_enabled_plugins(user_id: str) -> list[str]:
    """
    List all enabled plugins for a user.
    """
    return list(_user_plugin_enabled[user_id])