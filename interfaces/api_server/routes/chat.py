# File: interfaces/api_server/routes/chat.py

from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from ai.assistant_engine.ai_router import route_message
from ai.rasa.query import query_rasa
from ai.local.generate import generate_local_reply
from ai.rag.rag_search import search_documents
from ai.llm_fallback import call_llm
from interfaces.api_server.auth import get_current_user
from slowapi.util import get_remote_address
from interfaces.api_server.main import limiter
from interfaces.api_server.routes.admin import is_assist_enabled
from utils.privacy import mask_sensitive_data
from utils.context import detect_intent, detect_tone, log_conversation

router = APIRouter()

class MessageRequest(BaseModel):
    sender_id: str
    receiver_id: Optional[str] = "bot"
    message: str

@router.post("/generate-reply")
@limiter.limit("10/minute")
async def generate_reply(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    """
    Generate an AI reply for a one-on-one chat.
    Requires: sender_id, receiver_id, message in payload.
    Enforces JWT authentication and sender identity.
    """
    payload = await request.json()
    sender_id = payload.get("sender_id")
    receiver_id = payload.get("receiver_id")
    message = payload.get("message")

    if not all([sender_id, receiver_id, message]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sender_id, receiver_id, and message are required."
        )

    if current_user and sender_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sender ID does not match authenticated user."
        )

    # Fallback for dev: allow anonymous if no JWT
    if not current_user:
        sender_id = sender_id or "anonymous"

    # Check if assistant is enabled for this user
    if not is_assist_enabled(sender_id):
        return {"reply": "Assistant mode is currently disabled for your account."}

    try:
        message_request = MessageRequest(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message
        )
        sender_id = message_request.sender_id
        receiver_id = message_request.receiver_id
        message = message_request.message.strip()

        if not message:
            raise HTTPException(status_code=400, detail="Empty message")

        # Step 1: Mask sensitive data before anything else
        safe_message = mask_sensitive_data(message)

        # Step 2: Detect sender's intent and tone
        sender_intent = detect_intent(safe_message, sender_id)
        sender_tone = detect_tone(safe_message)

        # Step 3: Use RASA for structured intent responses if applicable
        use_rasa = sender_intent not in ["greeting", "chitchat", "out_of_scope"]
        final_reply = None

        if use_rasa:
            try:
                rasa_reply = query_rasa(safe_message, sender_id)
                if not rasa_reply or rasa_reply.startswith("⚠️"):
                    # Try RAG fallback
                    try:
                        rag_reply = search_documents(safe_message)
                    except Exception as rag_err:
                        print(f"[RAG ERROR] {rag_err}")
                        rag_reply = None
                    if rag_reply:
                        final_reply = rag_reply
                    else:
                        # Try LLM fallback
                        try:
                            llm_reply = call_llm(safe_message)
                            final_reply = llm_reply
                        except Exception as llm_err:
                            print(f"[LLM ERROR] {llm_err}")
                            final_reply = "🤖 Sorry, I'm unable to generate a reply right now."
                else:
                    final_reply = rasa_reply
            except Exception as rasa_err:
                print(f"[RASA ERROR] {rasa_err}")
                # Try RAG then LLM fallback
                try:
                    rag_reply = search_documents(safe_message)
                except Exception as rag_err:
                    print(f"[RAG ERROR] {rag_err}")
                    rag_reply = None
                if rag_reply:
                    final_reply = rag_reply
                else:
                    try:
                        final_reply = call_llm(safe_message)
                    except Exception as llm_err:
                        print(f"[LLM ERROR] {llm_err}")
                        final_reply = "🤖 Sorry, I'm unable to generate a reply right now."
        else:
            # Skip RASA entirely if intent is chit-chat etc.
            final_reply = generate_local_reply(
                safe_message, sender_intent, sender_tone, sender_id
            )

        # Step 6: Log for monitoring
        log_conversation(sender_id, message, final_reply, sender_intent)

        # Step 7: Log fallback source per user in Redis
        try:
            fallback_used = (
                "rasa" if "rasa_reply" in locals() and rasa_reply and not rasa_reply.startswith("⚠️")
                else "rag" if "rag_reply" in locals() and rag_reply
                else "llm" if "llm_reply" in locals() and llm_reply
                else "local"
            )

            # Save last fallback type used (1 hour expiry)
            await redis.set(f"fallback:{sender_id}", fallback_used, ex=3600)

            # Optional: maintain last 5 fallback types used
            await redis.lpush(f"fallback:history:{sender_id}", fallback_used)
            await redis.ltrim(f"fallback:history:{sender_id}", 0, 4)

        except Exception as log_fallback_err:
            print(f"[REDIS Fallback Log Error] {log_fallback_err}")

        return {
            "reply": final_reply,
            "intent": sender_intent,
            "tone": sender_tone
        }

    except Exception as e:
        print(f"[ERROR] Reply generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal AI engine failure")

