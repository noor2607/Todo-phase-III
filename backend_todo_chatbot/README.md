# Todo AI Chatbot Backend

This is the backend component for the Todo AI Chatbot application. It provides a REST API that allows users to manage their tasks through natural language commands using AI-powered processing.

## Features

- Natural language task management via AI agent
- Secure JWT-based authentication
- MCP tools integration for safe database operations
- Conversation history persistence
- Rate limiting for API protection
- Stateless architecture

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs with Python 3.7+
- SQLModel: SQL databases in Python, with SQLAlchemy and Pydantic
- Cohere: AI language models for natural language processing
- OpenAI Agents SDK: Framework for creating AI agents with tool usage
- Official MCP SDK: Model Context Protocol for tool integration

## Installation

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file with the required environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
COHERE_API_KEY=your-cohere-api-key-here
JWT_SECRET=your-jwt-secret
```

## Running the Application

```bash
uvicorn backend_todo_chatbot.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `POST /api/{user_id}/chat`: Process natural language chat requests
- `GET /health`: Health check endpoint

## Architecture

The backend follows a modular architecture with the following components:

- **Models**: SQLModel database models for Task, Conversation, and Message entities
- **Services**: Business logic layer for data operations
- **Tools**: MCP tools for safe database operations
- **Agents**: AI agent integration for natural language processing
- **API**: FastAPI routes and request handling
- **Utils**: Helper functions and utilities

## Security

- JWT-based authentication for all API requests
- User isolation enforcement through user_id validation
- Rate limiting to prevent abuse
- MCP-enforced data access to prevent direct database manipulation by AI agents