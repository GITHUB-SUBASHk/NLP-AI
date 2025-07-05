# interfaces/api_server/middleware/logging.py
import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from interfaces.api_server.session import redis_client  # assumes redis_client is a Redis instance
from interfaces.api_server.auth import get_current_user
from fastapi import status

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        path = request.url.path
        ip = request.client.host
        sender_id = None

        # Only log /api/generate-reply
        if path.endswith("/generate-reply"):
            try:
                body = await request.json()
                sender_id = body.get("sender_id")
            except Exception:
                sender_id = None

            # Try to get sender_id from JWT if not in body
            if not sender_id:
                try:
                    user = await get_current_user(request)
                    sender_id = user
                except Exception:
                    sender_id = "anonymous"

        response = await call_next(request)

        if path.endswith("/generate-reply"):
            log_entry = {
                "timestamp": timestamp,
                "sender_id": sender_id or "unknown",
                "event": "error" if response.status_code >= 400 else "reply_sent",
                "intent": None,  # Optionally fill in route logic
                "confidence": None,
                "message": None,
                "path": path,
                "ip": ip,
                "status_code": response.status_code
            }
            # If error, try to extract reason
            if response.status_code >= 400:
                try:
                    body = await response.body()
                    log_entry["error"] = body.decode()
                except Exception:
                    log_entry["error"] = "Unknown error"

            # Store in Redis (capped list)
            redis_client.lpush(f"logs:{sender_id}", json.dumps(log_entry))
            redis_client.ltrim(f"logs:{sender_id}", 0, 49)

        return response