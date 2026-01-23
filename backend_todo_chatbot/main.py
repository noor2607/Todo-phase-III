from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
import os
import jwt
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models import *
from src.services import *
from src.database import get_db_session, create_db_and_tables
from src.utils.rate_limiter import rate_limit
from src.agents import TodoAgent
from sqlmodel import Session
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Todo AI Chatbot API", version="1.0.0")

# Add CORS middleware to allow requests from the deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-phase-iii.vercel.app",  # Deployed frontend
        "http://localhost:3000",              # Local development
        "http://localhost:3001",              # Alternative local port
        "http://localhost:8000",              # Backend local server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCall]


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Verify JWT token and extract user_id.

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        user_id extracted from the JWT token
    """
    try:
        # Get secret from environment
        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise HTTPException(status_code=500, detail="JWT Secret not configured")

        # Decode token
        payload = jwt.decode(credentials.credentials, secret, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")

        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
@rate_limit(max_calls=60, time_window=3600)  # 60 calls per hour per user
def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    current_user_id: int = Depends(verify_jwt_token),
    db_session: Session = Depends(get_db_session)
):
    """
    Process natural language chat requests.

    Args:
        user_id: The user ID from the URL path
        request: Chat request containing conversation_id and message
        current_user_id: User ID extracted from JWT token
        db_session: Database session

    Returns:
        ChatResponse with conversation_id, response, and tool_calls
    """
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden: User ID mismatch")

    # Initialize services
    conversation_service = ConversationService()
    message_service = MessageService()

    # Get or create conversation
    conversation = None
    if request.conversation_id:
        # Try to get existing conversation
        conversation = conversation_service.get_conversation_by_id(
            db_session, request.conversation_id, user_id
        )
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation_data = ConversationCreate(user_id=user_id)
        conversation = conversation_service.create_conversation(db_session, conversation_data)

    # Create user message
    user_message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    user_message = message_service.create_message(db_session, user_message_data)

    # Initialize and run AI agent
    try:
        agent = TodoAgent()
        agent_result = agent.run_agent(request.message, user_id)

        ai_response = agent_result.get("response", "I processed your request.")
        tool_calls = agent_result.get("tool_calls", [])
    except Exception as e:
        # Handle agent errors gracefully
        ai_response = f"I encountered an issue processing your request: {str(e)}"
        tool_calls = []

    # Create assistant message
    assistant_message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response
    )
    assistant_message = message_service.create_message(db_session, assistant_message_data)

    # Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=ai_response,
        tool_calls=tool_calls
    )


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}