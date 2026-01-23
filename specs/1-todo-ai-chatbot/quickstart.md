# Todo AI Chatbot - Quickstart Guide

## Prerequisites

### Environment Setup
- Python 3.9+ installed
- Node.js 18+ installed
- PostgreSQL database (Neon Serverless recommended)
- Cohere API key
- Better Auth configured for frontend authentication

### Required Packages
- FastAPI
- SQLModel
- OpenAI Agents SDK
- Official MCP SDK
- python-dotenv
- Next.js 16+
- OpenAI ChatKit

## Configuration

### Environment Variables
Create a `.env` file with the following variables:
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
COHERE_API_KEY=your-cohere-api-key-here
JWT_SECRET=your-jwt-secret
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_TOKEN=your-better-auth-token
```

### Database Setup
1. Install required database drivers
2. Run database migrations to create Task, Conversation, and Message tables
3. Verify database connectivity

## Installation Steps

### 1. Backend Setup
```bash
# Install Python dependencies
pip install fastapi sqlmodel openai-agents-sdk python-dotenv

# Create database tables
python -m scripts.create_tables
```

### 2. MCP Tools Implementation
```python
# Example MCP tool implementation
from mcp_sdk import function_tool

@function_tool
def add_task(user_id: int, title: str, description: str = None):
    """Creates a new task for the user."""
    # Implementation here
    pass
```

### 3. AI Agent Configuration
```python
import os
from openai_agents import Agent, Runner
from openai_agents.models import OpenAIChatCompletionsModel
from openai_agents.config import RunConfig
from dotenv import load_dotenv

load_dotenv()

# Validate API key exists
if not os.getenv("COHERE_API_KEY"):
    raise ValueError("COHERE_API_KEY environment variable is required")

# Initialize Cohere-compatible client
client = OpenAIChatCompletionsModel(
    model="command-r-plus",  # Cohere model
    api_key=os.getenv("COHERE_API_KEY"),
    base_url="https://api.cohere.ai/v1/"  # Cohere's OpenAI-compatible endpoint
)

# Configure run settings
config = RunConfig(tracing_disabled=True)

# Initialize agent with MCP tools
agent = Agent(
    name="TodoAssistant",
    instructions="You are a helpful assistant that manages tasks for users. Use the provided tools to add, list, complete, update, or delete tasks.",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)
```

### 4. Chat Endpoint Implementation
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT and extract user information."""
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    current_user_id: int = Depends(get_current_user)
):
    """Process natural language chat requests."""
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Load conversation history
    # Run agent with tools
    # Save new messages
    # Return response
```

### 5. Frontend Integration
```javascript
// Example React component using ChatKit
import { ChatInterface } from '@openai/chatkit';

const TodoChat = () => {
  const handleSendMessage = async (message) => {
    const response = await fetch(`/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwtToken}`
      },
      body: JSON.stringify({
        conversation_id: currentConversationId,
        message: message
      })
    });

    const data = await response.json();
    return data.response;
  };

  return (
    <ChatInterface
      onSendMessage={handleSendMessage}
      // Other props
    />
  );
};
```

## Running the Application

### Development
```bash
# Backend
uvicorn main:app --reload

# Frontend
npm run dev
```

### Testing
```bash
# Run backend tests
pytest tests/

# Run frontend tests
npm test
```

## Key Components

### MCP Tools
- `add_task()`: Create new tasks
- `list_tasks()`: Retrieve user's tasks
- `complete_task()`: Mark tasks as completed
- `delete_task()`: Remove tasks
- `update_task()`: Modify task details

### Data Models
- `Task`: User's task information
- `Conversation`: Chat session tracking
- `Message`: Individual chat messages

### Security Features
- JWT validation for all requests
- User isolation enforcement
- Rate limiting on chat endpoints
- MCP tool access control