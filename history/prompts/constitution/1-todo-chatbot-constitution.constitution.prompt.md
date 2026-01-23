---
id: 1
title: "Todo Chatbot Constitution"
stage: constitution
date_iso: 2026-01-23
surface: agent
model: Claude Sonnet 4.5
feature: todo-ai-chatbot
branch: main
user: user
command: "/sp.constitution Create a complete constitution for Phase III: Todo AI Chatbot"
labels:
  - constitution
  - ai-chatbot
  - todo-app
  - architecture
  - security

links:
  spec: null
  ticket: null
  adr: null
  pr: null

files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/1-todo-chatbot-constitution.constitution.prompt.md"

tests_yaml:
  - "No tests created in this phase"

outcome: "Created initial constitution for Todo AI Chatbot project with stateless architecture, MCP enforcement, security-first authentication, and agent behavioral constraints."
evaluation: "Constitution successfully captures all required architectural principles and constraints for the AI chatbot project."
---

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

## Prompt Text

Create a complete constitution for Phase III: Todo AI Chatbot for my existing Full-Stack Todo application. The constitution must strictly follow my current architecture, technology stack, authentication model, and stateless backend principles. The goal is to integrate a natural language chatbot into the existing Todo app using OpenAI Agents SDK and MCP Server architecture. The chatbot must manage tasks through MCP tools, persist conversation state in the database, and remain fully stateless at the server level. This project already has a completed Phase II full-stack Todo application with Frontend: Next.js 16+ App Router, TypeScript, Tailwind, deployed on Vercel, Backend: FastAPI, SQLModel ORM, Neon Serverless PostgreSQL, Authentication: Better Auth on frontend issuing JWT tokens verified by FastAPI backend, and all REST APIs already secured with JWT and filtered by authenticated user_id. Integrate an AI-powered chatbot interface that allows users to manage their todos using natural language commands. The chatbot must use OpenAI Agents SDK for reasoning and an MCP server exposing task operations as tools. The system must be stateless, scalable, and fully integrated with existing authentication and task ownership rules. Core Architectural Rules (Mandatory): Backend remains fully stateless with no in-memory session storage, all conversation history must be persisted in PostgreSQL, every request must be authenticated using JWT from Better Auth, MCP tools must enforce user isolation using authenticated user_id, AI agent may only modify data through MCP tools and never direct DB access, chat endpoint must reconstruct context from database on every request, and task ownership and authorization must be enforced on every tool call. Technology Stack (Mandatory): Frontend uses OpenAI ChatKit UI integrated into existing Next.js app with authenticated user session via Better Auth and chat requests including JWT token in Authorization header, Backend uses FastAPI, SQLModel ORM, OpenAI Agents SDK, Official MCP SDK, and Neon Serverless PostgreSQL. Database Models (Required): Task with id, user_id, title, description, completed, created_at, updated_at; Conversation with id, user_id, created_at, updated_at; Message with id, user_id, conversation_id, role, content, created_at. API Contract: POST /api/{user_id}/chat with request fields conversation_id optional integer and message required string and response fields conversation_id integer, response string, and tool_calls array of executed MCP tools. Authentication Rules: Every chat request requires valid JWT, user_id must be derived from verified JWT and never trusted from URL alone, and all conversations and messages must belong only to the authenticated user. MCP Tools Specification must define and standardize add_task(user_id, title, description?), list_tasks(user_id, status?), complete_task(user_id, task_id), delete_task(user_id, task_id), and update_task(user_id, task_id, title?, description?) and each tool must validate ownership using user_id, return structured JSON responses, and handle not-found and unauthorized cases gracefully. Agent Behavior Rules: Use add_task when user expresses intent to create or remember, use list_tasks when user asks to see, show, or filter, use complete_task when user indicates completion, use delete_task when user requests removal, use update_task when user requests modification, confirm every successful action with friendly natural language, never hallucinate task data and always rely on MCP tool results, and handle ambiguous requests by asking clarification. Conversation Flow (Stateless Cycle): Authenticate request via JWT, load conversation and message history from database, append new user message, run OpenAI Agent with MCP tools, execute tool calls if needed, persist assistant message and tool results, return response and conversation_id, and server holds no memory between requests. Frontend Requirements: Integrate ChatKit UI inside existing authenticated app, support starting new conversations and resuming existing ones, display assistant messages

## Response Text

Created a comprehensive constitution for the Todo AI Chatbot project that incorporates all the specified architectural requirements, security models, and development constraints. The constitution establishes core principles around stateless architecture, MCP-enforced data access, security-first authentication, test-first methodology, data integrity, and AI agent behavioral constraints. It also defines architecture rules, MCP tools specifications, API contracts, and governance procedures to guide the development of the AI chatbot system.