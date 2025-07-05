"""
Plugin Loader
Dynamically maps intents to plugin handlers and executes them safely via sandbox_runner.
Also provides per-user plugin enablement checks.
"""

import yaml
import os

# These should be imported or defined at the top level
try:
    from interfaces.api_server.session import redis_client as redis
    USE_REDIS = True
except ImportError:
    redis = None
    USE_REDIS = False

# In-memory fallback for plugin toggles
user_preferences = {}

from ai.plugins.sandbox_runner import run_plugin_safe

PLUGIN_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "plugin_config.yaml")

def load_plugin_mapping():
    with open(PLUGIN_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def is_plugin_enabled(user_id: str, plugin_name: str) -> bool:
    """
    Check if a plugin is enabled for a specific user.
    Uses Redis if available, otherwise falls back to in-memory.
    """
    key = f"plugin:{user_id}:{plugin_name}"
    if USE_REDIS and redis:
        val = redis.get(key)
        return bool(int(val)) if val else False
    return user_preferences.get(key, False)

def handle_with_plugin(intent: str, user_input: str, user_id: str) -> str:
    """
    Handles user input with the mapped plugin if enabled for the user.
    """
    plugin_map = load_plugin_mapping()
    plugin_name = plugin_map.get(intent)
    if not plugin_name:
        return f"❌ No plugin mapped for intent: {intent}"

    if not is_plugin_enabled(user_id, plugin_name):
        return f"🚫 Plugin '{plugin_name}' is disabled for this user."

    response = run_plugin_safe(plugin_name, user_input)
    return response