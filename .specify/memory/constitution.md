<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.0 (initial constitution for Phase III Todo AI Chatbot)
- Added sections: Core Principles specific to AI Chatbot, Architecture Rules, Security Model, Agent Behavior Policy
- Templates requiring updates: ⚠ pending review of .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Todo AI Chatbot Constitution

## Core Principles

### I. Stateless Architecture
Backend services remain fully stateless with no in-memory session storage. All conversation history must be persisted in PostgreSQL. Every request must be authenticated using JWT from Better Auth. The chat endpoint must reconstruct context from database on every request. Server holds no memory between requests.

### II. MCP-Enforced Data Access
AI agent may only modify data through MCP tools and never direct DB access. MCP tools must enforce user isolation using authenticated user_id. Task ownership and authorization must be enforced on every tool call. AI agent must never bypass MCP tools for data manipulation.

### III. Security-First Authentication
Every chat request requires valid JWT. User_id must be derived from verified JWT and never trusted from URL alone. All conversations and messages must belong only to the authenticated user. MCP tools must validate ownership using user_id for every operation.

### IV. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All MCP tools must have comprehensive test coverage. Agent behavior must be validated through integration tests.

### V. Data Integrity and Consistency
Database models must maintain referential integrity. Task operations must be atomic and consistent. Message ordering must be preserved through timestamps. Conversation state must be accurately reconstructed from persisted data.

### VI. AI Agent Behavioral Constraints
Agent must use add_task when user expresses intent to create or remember. Use list_tasks when user asks to see, show, or filter. Use complete_task when user indicates completion. Use delete_task when user requests removal. Use update_task when user requests modification. Agent must never hallucinate task data and always rely on MCP tool results.

## Architecture Rules

### Backend Architecture
- Backend: FastAPI, SQLModel ORM, OpenAI Agents SDK, Official MCP SDK, Neon Serverless PostgreSQL
- Remain fully stateless with no in-memory session storage
- Every request must authenticate using JWT from Better Auth
- Chat endpoint must reconstruct context from database on every request
- Server holds no memory between requests

### Frontend Architecture
- Frontend: Next.js 16+ App Router, TypeScript, Tailwind, OpenAI ChatKit UI, deployed on Vercel
- Integrate ChatKit UI inside existing authenticated app
- Support starting new conversations and resuming existing ones
- Display assistant messages, user messages, and confirmations
- Send JWT token with every chat request
- Maintain authenticated user session via Better Auth

### Database Schema
- Task model: id, user_id, title, description, completed, created_at, updated_at
- Conversation model: id, user_id, created_at, updated_at
- Message model: id, user_id, conversation_id, role, content, created_at
- All models must enforce foreign key relationships and user ownership

## MCP Tools Specification

### Standardized Tool Definitions
- add_task(user_id, title, description?): Creates new task for user
- list_tasks(user_id, status?): Retrieves user's tasks with optional status filter
- complete_task(user_id, task_id): Marks user's task as completed
- delete_task(user_id, task_id): Removes user's task from system
- update_task(user_id, task_id, title?, description?): Modifies user's task details

### Tool Requirements
- Each tool must validate ownership using user_id
- Return structured JSON responses
- Handle not-found and unauthorized cases gracefully
- Log all tool executions for audit trail
- Enforce rate limiting to prevent abuse

## API Contract

### Chat Endpoint
- Endpoint: POST /api/{user_id}/chat
- Request fields: conversation_id (optional integer), message (required string)
- Response fields: conversation_id (integer), response (string), tool_calls (array of executed MCP tools)
- Authentication: JWT token in Authorization header
- Rate limiting: Per-user request throttling

### Error Handling
- Standardized error responses with appropriate HTTP status codes
- Detailed error messages for debugging without exposing internals
- Graceful degradation when MCP tools are unavailable

## Governance

### Amendment Process
- All changes to this constitution require documentation and team approval
- Major architectural changes require migration planning
- Security-related amendments require security review

### Compliance Requirements
- All PRs/reviews must verify compliance with these principles
- Architecture decisions must align with stated principles
- Security requirements must be validated during code reviews

### Development Standards
- Follow existing code style and patterns from Phase II Todo application
- Maintain backward compatibility with existing authentication system
- Ensure performance standards are met for real-time chat interactions

**Version**: 1.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23
