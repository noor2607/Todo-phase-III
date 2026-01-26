from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from routes.api import router as api_router
from routes.auth_routes import router as auth_router
from routes.tasks import router as tasks_router
from routes.chat import router as chat_router  # Import the new chat router
from config.settings import settings
from database.engine import init_db


# Create FastAPI app instance
app = FastAPI(
    title="Todo App Backend",
    description="Backend service for Todo application with authentication, task management, and AI chat functionality",
    version="1.0.0",
)

# Add security middleware
if settings.environment.lower() == "production":
    # Trusted host middleware to prevent host header attacks
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["todo-app.com", "www.todo-app.com", ".todo-app.com", "localhost", "127.0.0.1", "[::1]"],
    )

# Add CORS middleware
allow_origins_list = settings.allowed_origins.split(",") if hasattr(settings, 'allowed_origins') and settings.allowed_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins_list,  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def on_startup():
    init_db()

# Include authentication routes
app.include_router(api_router, prefix="/api", tags=["authentication"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])  # Include the new chat router

@app.get("/")
def read_root():
    """Root endpoint for health check"""
    return {
        "status": "healthy",
        "service": "Todo App Backend",
        "environment": settings.environment
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Todo App service is running"
    }