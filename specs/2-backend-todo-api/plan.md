# Implementation Plan: Backend Todo API

**Branch**: `2-backend-todo-api` | **Date**: 2026-01-16 | **Spec**: [link](../specs/2-backend-todo-api/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a secure, token-based backend API for a multi-user todo application using Python FastAPI, SQLModel ORM, and Neon PostgreSQL. The API will provide full CRUD operations for user tasks with strict authentication and authorization enforcement using JWT tokens compatible with Better Auth, ensuring complete data isolation between users.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, python-multipart
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server (Vercel deployment)
**Project Type**: Backend API
**Performance Goals**: <500ms p95 response time for all endpoints
**Constraints**: <200ms p95 for task operations, JWT stateless authentication, user data isolation
**Scale/Scope**: Support 10k+ concurrent users with proper database indexing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Authentication: JWT-based, stateless, no server-side sessions
- ✅ User Data Isolation: Backend enforces ownership verification on every operation
- ✅ API Contract: RESTful endpoints under /api/ with consistent response format
- ✅ Database Integrity: SQLModel ORM with proper foreign keys and indexing
- ✅ Error Handling: Proper HTTP status codes and consistent response format
- ✅ Security: Token validation without trusting client-provided user IDs

## Project Structure

### Documentation (this feature)

```text
specs/2-backend-todo-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py             # Application entry point
├── database/
│   ├── __init__.py
│   ├── engine.py       # Database engine and session management
│   └── models/         # SQLModel database models
│       └── task.py
├── auth/
│   ├── __init__.py
│   ├── jwt_handler.py  # JWT verification utilities
│   └── dependencies.py # Authentication dependencies
├── schemas/
│   ├── __init__.py
│   ├── task.py         # Pydantic request/response schemas
│   └── auth.py         # Authentication schemas
├── routes/
│   ├── __init__.py
│   └── tasks.py        # Task API route definitions
├── config/
│   ├── __init__.py
│   └── settings.py     # Application settings and environment variables
└── utils/
    ├── __init__.py
    └── validators.py   # Validation utilities

tests/
├── unit/
│   ├── test_models/
│   └── test_schemas/
├── integration/
│   ├── test_auth/
│   └── test_tasks/
└── conftest.py         # Test fixtures

requirements.txt
dev-requirements.txt
README.md
.env.example
```

**Structure Decision**: Backend API structure with clear separation of concerns following the constitution's folder structure invariants. Models in /src/models, schemas in /src/schemas, routes in /src/routes, and auth utilities in /src/auth.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |