---
id: 3
title: "Todo AI Chatbot Plan"
stage: plan
date_iso: 2026-01-23
surface: agent
model: Claude Sonnet 4.5
feature: todo-ai-chatbot
branch: 1-todo-ai-chatbot
user: user
command: "/sp.plan Create a detailed implementation plan for the Todo AI Chatbot"
labels:
  - plan
  - ai-chatbot
  - todo-app
  - mcp-tools
  - cohere

links:
  spec: "specs/1-todo-ai-chatbot/spec.md"
  plan: "specs/1-todo-ai-chatbot/plan.md"
  ticket: null
  adr: null
  pr: null

files_yaml:
  - "specs/1-todo-ai-chatbot/plan.md"
  - "specs/1-todo-ai-chatbot/research.md"
  - "specs/1-todo-ai-chatbot/data-model.md"
  - "specs/1-todo-ai-chatbot/contracts/api-contract.yaml"
  - "specs/1-todo-ai-chatbot/quickstart.md"
  - ".specify/memory/claude-agent-context.md"
  - "history/prompts/todo-ai-chatbot/3-todo-ai-chatbot-plan.plan.prompt.md"

tests_yaml:
  - "No tests created in this phase"

outcome: "Created detailed implementation plan for Todo AI Chatbot with all required components."
evaluation: "Plan covers all necessary phases from MCP setup to deployment with proper constitutional compliance."
---

# Todo AI Chatbot - Implementation Plan

## Technical Context

### Known Architecture
- **Frontend**: Next.js 16+ App Router, TypeScript, Tailwind, OpenAI ChatKit UI, Better Auth, deployed on Vercel
- **Backend**: FastAPI, SQLModel ORM, Neon Serverless PostgreSQL, Better Auth JWT authentication
- **AI Integration**: OpenAI Agents SDK with Cohere as model provider
- **MCP Server**: Official MCP SDK for task operations
- **Database**: Neon Serverless PostgreSQL with Task, Conversation, and Message models
- **Authentication**: JWT-based with Better Auth integration

### Unknown Elements (NEEDS CLARIFICATION)
- Specific Cohere model name to use with OpenAI-compatible interface
- Exact structure of MCP server implementation
- Rate limiting thresholds for chat endpoint
- Conversation history retention policy
- Specific error handling strategies for AI service outages

### Dependencies
- OpenAI Agents SDK
- Cohere API service
- dotenv for environment management
- Official MCP SDK
- Better Auth for JWT validation
- SQLModel for database operations

### Integration Points
- Frontend ChatKit UI integration with backend chat endpoint
- JWT authentication validation in chat endpoint
- MCP tools registration with AI agent
- Database models for conversation persistence

## Constitution Check

### Compliance Verification
- ✅ **Stateless Architecture**: Chat endpoint will reconstruct context from database on every request, with no in-memory session storage
- ✅ **MCP-Enforced Data Access**: AI agent will only modify data through registered MCP tools, never direct DB access
- ✅ **Security-First Authentication**: Every request will validate JWT and derive user_id from verified token
- ✅ **Test-First Approach**: All MCP tools and chat endpoint will have comprehensive test coverage
- ✅ **Data Integrity**: Database models will maintain referential integrity with proper foreign key relationships
- ✅ **AI Agent Behavioral Constraints**: Agent will follow specified behavior patterns for each task operation

### Potential Violations
- None identified - all requirements align with constitution principles

## Phase 0: Research & Preparation

### Research Tasks
1. **Cohere Integration Research**
   - Decision: Determine which Cohere model to use with OpenAI-compatible interface
   - Rationale: Need to select appropriate model for task management conversations
   - Alternatives considered: Command-R, Command-R+, or other available Cohere models

2. **MCP Server Implementation Patterns**
   - Decision: Understand how to properly implement MCP server with task operations
   - Rationale: MCP tools are critical for agent data access compliance
   - Alternatives considered: Different MCP SDK configurations

3. **Rate Limiting Strategy**
   - Decision: Define appropriate rate limits for chat endpoint per user
   - Rationale: Prevent abuse while allowing normal usage patterns
   - Alternatives considered: Time-based vs request-count-based limits

4. **Error Handling Best Practices**
   - Decision: Establish error handling patterns for AI service outages
   - Rationale: Ensure graceful degradation when external services fail
   - Alternatives considered: Retry mechanisms vs immediate failover responses

### Expected Outcomes
- Research document with technical decisions for unknown elements
- Clear understanding of MCP server implementation
- Defined rate limiting and error handling strategies

## Phase 1: Data Model & API Design

### Data Model Design

#### Task Model
- Fields: id (int, primary key), user_id (int, foreign key), title (str), description (str, nullable), completed (bool), created_at (datetime), updated_at (datetime)
- Constraints: Foreign key relationship to user, user_id validation
- Indexes: user_id for efficient querying by user

#### Conversation Model
- Fields: id (int, primary key), user_id (int, foreign key), created_at (datetime), updated_at (datetime)
- Constraints: Foreign key relationship to user
- Indexes: user_id for efficient querying by user

#### Message Model
- Fields: id (int, primary key), user_id (int, foreign key), conversation_id (int, foreign key), role (str - "user" or "assistant"), content (str), created_at (datetime)
- Constraints: Foreign key relationships to user and conversation
- Indexes: conversation_id for chronological message retrieval

### API Contract Design

#### Chat Endpoint
- Method: POST
- Path: /api/{user_id}/chat
- Headers: Authorization: Bearer {jwt_token}
- Request Body:
  ```json
  {
    "conversation_id": 123, // optional, null for new conversation
    "message": "Add a new task to buy groceries"
  }
  ```
- Response Body:
  ```json
  {
    "conversation_id": 123,
    "response": "I've added the task 'buy groceries' to your list.",
    "tool_calls": [
      {
        "name": "add_task",
        "arguments": {"title": "buy groceries"},
        "result": {"task_id": 456}
      }
    ]
  }
  ```
- Status Codes: 200 (success), 401 (unauthorized), 403 (forbidden), 500 (server error)

#### Error Responses
- Format: Standardized error responses with appropriate HTTP status codes
- Content: { "error": "error message", "code": "error_code" }

### MCP Tool Contracts

#### add_task(user_id, title, description?)
- Purpose: Creates new task for user
- Parameters: user_id (int), title (str), description (str, optional)
- Returns: { "task_id": int, "title": str, "description": str, "completed": bool }

#### list_tasks(user_id, status?)
- Purpose: Retrieves user's tasks with optional status filter
- Parameters: user_id (int), status (str, optional - "all", "active", "completed")
- Returns: { "tasks": [{"task_id": int, "title": str, "completed": bool}] }

#### complete_task(user_id, task_id)
- Purpose: Marks user's task as completed
- Parameters: user_id (int), task_id (int)
- Returns: { "task_id": int, "completed": true, "title": str }

#### delete_task(user_id, task_id)
- Purpose: Removes user's task from system
- Parameters: user_id (int), task_id (int)
- Returns: { "task_id": int, "deleted": true }

#### update_task(user_id, task_id, title?, description?)
- Purpose: Modifies user's task details
- Parameters: user_id (int), task_id (int), title (str, optional), description (str, optional)
- Returns: { "task_id": int, "title": str, "description": str, "updated": true }

## Phase 2: Implementation Roadmap

### Phase 2A: MCP Tool Setup
**Objective**: Implement MCP tools for task operations that comply with constitutional requirements
- Create MCP server with registered task operation tools
- Implement proper user_id validation in each tool
- Add logging and rate limiting to tools
- Write comprehensive tests for each MCP tool

### Phase 2B: Database Models & Persistence
**Objective**: Set up database models and persistence layer for conversation history
- Implement SQLModel database models for Task, Conversation, and Message
- Create database migration scripts
- Implement repository/DAO classes for data access
- Add proper foreign key constraints and indexes
- Write tests for data persistence operations

### Phase 2C: Backend Chat Endpoint
**Objective**: Create the stateless chat endpoint that integrates with AI agent
- Implement JWT authentication middleware
- Create the POST /api/{user_id}/chat endpoint
- Add conversation history loading and saving logic
- Implement error handling and rate limiting
- Write comprehensive endpoint tests

### Phase 2D: OpenAI Agent Integration
**Objective**: Integrate OpenAI Agents SDK with Cohere as provider
- Set up environment loading with dotenv
- Create AsyncOpenAI-compatible client for Cohere
- Initialize OpenAIChatCompletionsModel with Cohere model
- Configure RunConfig with tracing_disabled=True
- Register MCP tools with @function_tool decorator
- Create Agent with appropriate instructions
- Implement Runner.run_sync execution pattern
- Add proper error handling for AI service calls

### Phase 2E: Frontend ChatKit Integration
**Objective**: Integrate ChatKit UI into existing frontend application
- Add ChatKit component to existing Next.js app
- Implement JWT token passing to chat endpoint
- Add support for new and resumed conversations
- Display assistant messages, user messages, and confirmations
- Handle conversation state management
- Implement error feedback to users

### Phase 2F: Authentication & Security
**Objective**: Ensure all security requirements are met
- Verify JWT authentication flows
- Test user isolation enforcement
- Validate proper user_id derivation from JWT
- Test cross-user data protection
- Implement audit logging for security events

### Phase 2G: Testing & Quality Assurance
**Objective**: Ensure comprehensive test coverage and quality
- Unit tests for MCP tools
- Integration tests for chat endpoint
- End-to-end tests for complete chat flows
- Performance tests for response times
- Security tests for authentication and authorization

### Phase 2H: Deployment & Production Readiness
**Objective**: Prepare for production deployment
- Environment configuration for production
- Database migration scripts for production
- Monitoring and logging setup
- Performance optimization
- Documentation updates

## Success Criteria for Implementation

### Technical Metrics
- 95% of chat requests return responses within 5 seconds
- Zero direct database access violations by the AI agent
- 99% uptime maintained for the chat endpoint
- All user data remains isolated with no cross-contamination

### Quality Metrics
- 90% code coverage for all components
- All MCP tools have comprehensive test coverage
- Error rates below 1% in production
- Successful authentication validation for 100% of requests

### User Experience Metrics
- Users can successfully create, list, update, complete, and delete tasks using natural language
- High satisfaction scores for natural language task management
- Smooth conversation continuity between sessions
- Clear error messages when operations fail

## Prompt Text

Create a detailed implementation plan for the Todo AI Chatbot for my full-stack Todo app with /frontend (Next.js 16+, Tailwind, Better Auth, ChatKit), /backend (FastAPI, SQLModel, Neon PostgreSQL, JWT auth), MCP server with Official MCP SDK, and stateless chat endpoint. The plan must integrate OpenAI Agents SDK using the pattern: load COHERE_API_KEY from .env with dotenv, raise error if missing, create AsyncOpenAI-compatible client, initialize OpenAIChatCompletionsModel, configure RunConfig(tracing_disabled=True), import Agent, Runner, @function_tool, register MCP task tools (add_task, list_tasks, complete_task, delete_task, update_task), pass tools to Agent, execute with Runner.run_sync(agent, input=user_message, run_config=config). Include stateless POST /api/{user_id}/chat endpoint, conversation/message persistence in DB, enforce task ownership via JWT, frontend ChatKit integration (support new/resumed conversations), tool call handling, confirmation messages, and error handling. Break the plan into sequential implementation phases covering MCP tool setup, database models, backend chat endpoint, OpenAI agent integration, frontend ChatKit UI, authentication flow, testing, and deployment, fully compatible with existing Phase II architecture and folder structure.

## Response Text

Created a comprehensive implementation plan for the Todo AI Chatbot that includes: technical context with known/unknown elements, constitution compliance verification, research phase with technical decisions, data model design for Task/Conversation/Message entities, API contract design for the chat endpoint and MCP tools, phased implementation roadmap from MCP setup to deployment, and success criteria for technical, quality, and user experience metrics. The plan addresses all specified requirements including Cohere integration, stateless architecture, JWT authentication, MCP tool usage, and frontend ChatKit integration.