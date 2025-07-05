# File: ai/plugins/plugin_manager.py

import os
import importlib.util
from ai.plugins.base_plugin import BasePlugin

PLUGIN_DIR = "ai/plugins/installed"

class PluginManager:
    def __init__(self):
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        """
        Dynamically load all plugins from the installed directory.
        Only loads classes named 'Plugin' that inherit from BasePlugin.
        """
        self.plugins.clear()  # Avoid duplicates on reload
        for filename in os.listdir(PLUGIN_DIR):
            if filename.endswith(".py"):
                path = os.path.join(PLUGIN_DIR, filename)
                plugin_name = filename[:-3]  # strip .py

                spec = importlib.util.spec_from_file_location(plugin_name, path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    plugin_class = getattr(module, "Plugin", None)
                    if plugin_class and issubclass(plugin_class, BasePlugin):
                        instance = plugin_class()
                        self.plugins.append(instance)
                        print(f"✅ Loaded plugin: {instance.meta().get('name', plugin_name)}")
                    else:
                        print(f"❌ {plugin_name} does not define a valid Plugin class")
                except Exception as e:
                    print(f"[Plugin Load Error] {plugin_name}: {e}")

    def get_plugin_for_intent(self, intent: str):
        """
        Return the first plugin instance that should handle the given intent.
        """
        for plugin in self.plugins:
            try:
                if plugin.should_handle(intent):
                    return plugin
            except Exception as e:
                print(f"[Plugin Error] {plugin.meta().get('name', 'unknown')}: {e}")
        return None

    def run_plugin(self, intent: str, message: str, sender_id: str) -> str:
        """
        Run the plugin for the given intent, if available.
        """
        plugin = self.get_plugin_for_intent(intent)
        if plugin:
            try:
                return plugin.run(message, sender_id)
            except Exception as e:
                print(f"[Plugin Run Error] {plugin.meta().get('name', 'unknown')}: {e}")
        return None

    def list_plugins(self) -> list:
        """
        Return a list of metadata dicts for all loaded plugins.
        """
        return [p.meta() for p in self.plugins]

    def reload_plugins(self):
        """
        Reload all plugins from the plugin directory.
        """
        self.load_plugins()