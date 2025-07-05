# File: interfaces/api_server/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces.api_server.routes import chat, auth
from interfaces.api_server.config import get_cors_origins, settings
from interfaces.api_server.routes import chat, auth, plugin_admin

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# 1. Initialize limiter using IP address
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

# 2. Define the rate-limit exceeded handler
def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

# 3. Initialize FastAPI app
app = FastAPI(title="AI-RTCA API Server")

# 4. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Register rate-limiting components
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# 6. Include API routers
app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/api", tags=["/chat"])
app.include_router(chat.router, prefix="/chat")
app.include_router(plugin_admin.router)  # <-- Add this line