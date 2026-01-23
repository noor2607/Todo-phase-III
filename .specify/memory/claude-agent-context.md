# Claude Code Agent Context - Todo AI Chatbot

## Technologies Used

### Backend Technologies
- FastAPI: Modern Python web framework for building APIs
- SQLModel: SQL database modeling and querying
- OpenAI Agents SDK: Framework for creating AI agents with tool usage
- Official MCP SDK: Model Context Protocol for tool integration
- python-dotenv: Environment variable management
- Neon Serverless PostgreSQL: Cloud-native PostgreSQL database

### Frontend Technologies
- Next.js 16+: React framework for production applications
- OpenAI ChatKit: Pre-built chat interface components
- Better Auth: Authentication solution for Next.js applications
- Tailwind CSS: Utility-first CSS framework

### AI/ML Technologies
- Cohere Platform: Language model provider with OpenAI-compatible API
- Command-R+ Model: Enterprise-grade language model for complex reasoning

## Architecture Patterns

### Stateless Design
- No in-memory session storage between requests
- Context reconstruction from database on each request
- Conversation history persistence in PostgreSQL

### Security-First Approach
- JWT-based authentication for all API requests
- User isolation through user_id validation
- MCP-enforced data access (no direct DB access by AI agent)

### MCP Tool Integration
- add_task, list_tasks, complete_task, delete_task, update_task functions
- @function_tool decorator for agent registration
- User ownership validation in each tool

## Implementation Patterns

### Agent Configuration
- Load COHERE_API_KEY from environment variables
- Create AsyncOpenAI-compatible client for Cohere
- Initialize OpenAIChatCompletionsModel with Cohere model
- Configure RunConfig with tracing_disabled=True
- Import Agent, Runner, and @function_tool from agents SDK

### API Endpoint Pattern
- POST /api/{user_id}/chat endpoint
- Request: { conversation_id: int, message: string }
- Response: { conversation_id: int, response: string, tool_calls: [] }

## Database Models
- Task: id, user_id, title, description, completed, created_at, updated_at
- Conversation: id, user_id, created_at, updated_at
- Message: id, user_id, conversation_id, role, content, created_at