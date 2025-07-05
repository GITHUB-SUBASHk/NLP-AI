import os
import requests
from ai.core_nlp.analyzer import detect_tone
from ai.core_nlp.intent_classifier import classify_intent
from ai.assistant_engine.reply_generator import generate_local_reply
from ai.memory.session_context import get_context, update_context
from ai.memory.learning_memory import add_fact
from client.privacy.privacy_guard import enforce_privacy
from ai.rag.rag_search import search_documents
from ai.llm_fallback import call_llm
from ai.plugins.loader import plugin_manager, handle_with_plugin, load_plugin_mapping
from interfaces.api_server.routes.admin import is_plugin_enabled_for_user
from interfaces.api_server.utils import log_fallback_source

RASA_ENABLED = os.getenv("RASA_ENABLED", "false").lower() == "true"
RASA_API_URL = os.getenv("RASA_API_URL", "http://localhost:5005")

async def route_message(message: str, sender_id: str, receiver_id: str) -> str:
    """
    Routes message using sender's context/memory/tone.
    Executes plugin if mapped, otherwise routes via RASA → RAG → LLM → Plugins → Local fallback.
    Logs which engine handled the reply.
    """
    try:
        # 1. Enforce privacy
        sanitized_msg = enforce_privacy(message)

        # 2. Analyze sender's tone/intent
        sender_tone = detect_tone(sanitized_msg)
        sender_intent = classify_intent(sanitized_msg)

        # 3. Update sender's session/memory
        update_context(sender_id, "last_intent", sender_intent)
        update_context(sender_id, "last_tone", sender_tone)
        add_fact(sender_id, sanitized_msg)

        # 4. Optionally analyze receiver's tone for learning (not used in reply)
        if receiver_id:
            receiver_context = get_context(receiver_id)
            receiver_tone = detect_tone(receiver_context.get("last_message", "")) if receiver_context.get("last_message") else None

        # 5. Plugin mapping (preferred path)
        plugin_map = load_plugin_mapping()
        if sender_intent in plugin_map:
            if is_plugin_enabled_for_user(sender_id, plugin_map[sender_intent]):
                try:
                    plugin_reply = handle_with_plugin(sender_intent, sanitized_msg, sender_id)
                    if plugin_reply:
                        log_fallback_source(sender_id, "PLUGIN")
                        return plugin_reply
                except Exception as e:
                    print(f"[PLUGIN ERROR] {e}")

        # 6. RASA fallback
        use_rasa = RASA_ENABLED and sender_intent not in ["greeting", "chitchat", "out_of_scope"]
        if use_rasa:
            try:
                reply = await query_rasa(sanitized_msg, sender_id)
                if reply and not reply.startswith("⚠️"):
                    log_fallback_source(sender_id, "RASA")
                    return reply
            except Exception as rasa_error:
                print(f"[RASA ERROR] {rasa_error}")

        # 7. RAG fallback
        try:
            rag_reply = search_documents(sanitized_msg)
            if rag_reply:
                log_fallback_source(sender_id, "RAG")
                return rag_reply
        except Exception as rag_error:
            print(f"[RAG ERROR] {rag_error}")

        # 8. LLM fallback
        try:
            llm_reply = call_llm(sanitized_msg)
            if llm_reply:
                log_fallback_source(sender_id, "LLM")
                return llm_reply
        except Exception as llm_error:
            print(f"[LLM ERROR] {llm_error}")

        # 9. Plugin fallback (legacy, if not mapped above)
        for plugin in getattr(plugin_manager, "plugins", []):
            try:
                if plugin.should_handle(sender_intent) and is_plugin_enabled_for_user(sender_id, plugin.meta()["name"]):
                    plugin_reply = plugin.run(sanitized_msg, sender_id)
                    if plugin_reply:
                        log_fallback_source(sender_id, "PLUGIN")
                        return plugin_reply
            except Exception as plugin_err:
                print(f"[PLUGIN ERROR] {getattr(plugin.meta(), 'name', 'unknown')}: {plugin_err}")

        # 10. Local fallback
        log_fallback_source(sender_id, "LOCAL")
        return generate_local_reply(sanitized_msg, sender_intent, sender_tone, sender_id)

    except Exception as err:
        print(f"[route_message ERROR] {err}")
        return "🤖 Sorry, an internal error occurred while processing your message."

async def query_rasa(message: str, sender_id: str) -> str:
    payload = {"sender": sender_id, "message": message}
    try:
        res = requests.post(f"{RASA_API_URL}/webhooks/rest/webhook", json=payload, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data and isinstance(data, list) and "text" in data[0]:
                return data[0]["text"]
            return "⚠️ No Rasa response."
        return f"⚠️ Rasa error ({res.status_code})"
    except Exception as e:
        return f"⚠️ Rasa error: {str(e)}"