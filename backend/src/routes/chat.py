from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional, Dict, Any
from database.engine import get_session
from auth.dependencies import get_current_user
from pydantic import BaseModel

# Import the TodoAgent from the local agents directory
import sys
import os

# Add the src directory to the Python path so we can import from agents
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
agents_dir = os.path.join(src_dir, 'agents')

# Add to path if not already there
if agents_dir not in sys.path:
    sys.path.insert(0, agents_dir)

from todo_agent import TodoAgent

router = APIRouter()


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


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process natural language chat requests.

    Args:
        request: Chat request containing conversation_id and message
        current_user_id: User ID extracted from JWT token (dependency injection)
        session: Database session (dependency injection)

    Returns:
        ChatResponse with conversation_id, response, and tool_calls
    """
    # Use the original user ID string to maintain consistency with task retrieval
    # Convert to int for internal operations, but handle both string and int formats
    if isinstance(current_user_id, str):
        try:
            user_id = int(current_user_id)
        except ValueError:
            # If it's not a numeric string, we'll pass it as-is and let individual methods handle it
            user_id = current_user_id
    else:
        user_id = current_user_id

    try:
        # Initialize and run AI agent
        agent = TodoAgent()

        # Check if API key is available, if not provide appropriate response
        if not agent.has_api_key:
            return ChatResponse(
                conversation_id=request.conversation_id or (int(current_user_id) if isinstance(current_user_id, (int, str)) and str(current_user_id).isdigit() else 1),
                response="AI service is currently unavailable. Please set up the COHERE_API_KEY in the backend environment variables.",
                tool_calls=[]
            )

        agent_result = agent.run_agent(request.message, user_id, session)

        ai_response = agent_result.get("response", "I processed your request.")
        tool_calls = agent_result.get("tool_calls", [])

        # For now, return a conversation ID (in a real implementation, you would create conversation records in the database)
        conversation_id = request.conversation_id or (int(user_id) if isinstance(user_id, (int, str)) and str(user_id).isdigit() else 1)

        return ChatResponse(
            conversation_id=conversation_id,
            response=ai_response,
            tool_calls=tool_calls
        )
    except ValueError as ve:
        # Handle specific value errors (like user_id conversion issues)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid user ID format: {str(ve)}"
        )
    except Exception as e:
        # Handle agent errors gracefully
        print(f"Error in chat endpoint: {str(e)}")  # Log the error for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )