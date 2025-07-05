from interfaces.api_server.session import redis_client

def increment_intent(intent: str):
    redis_client.hincrby("analytics:intent_counts", intent, 1)

def increment_fallback(intent: str):
    redis_client.hincrby("analytics:fallback_counts", intent, 1)

def increment_plugin_usage(plugin_name: str):
    redis_client.hincrby("analytics:plugin_usage", plugin_name, 1)

def set_session_count(count: int):
    redis_client.set("analytics:session_count", count)