---
description: "Task list for Backend Todo API implementation"
---

# Tasks: Backend Todo API

**Input**: Design documents from `/specs/2-backend-todo-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend API**: `backend/src/`, `backend/backend/tests/` at repository root with specific modules

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in backend/src/
- [x] T002 Initialize Python 3.11 project with FastAPI, SQLModel, PyJWT dependencies in requirements.txt
- [x] T003 [P] Configure linting and formatting tools (black, flake8, mypy) in pyproject.toml
- [x] T004 Create .env.example file with required environment variables
- [x] T005 Create README.md with project overview and setup instructions
/sp
---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup database engine and session management in backend/src/database/engine.py
- [x] T007 [P] Configure application settings and environment variables in backend/src/config/settings.py
- [x] T008 [P] Setup main application entry point in backend/src/main.py
- [x] T009 [P] Implement JWT verification utilities in backend/src/auth/jwt_handler.py
- [x] T010 [P] Create authentication dependencies in backend/src/auth/dependencies.py
- [x] T011 Configure error handling and logging infrastructure in backend/src/utils/logging.py
- [x] T012 Create base validation utilities in backend/src/utils/validators.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Manage Personal Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable registered users to create, view, update, and delete their personal tasks through secure API endpoints with JWT authentication

**Independent Test**: Can be fully tested by authenticating with a valid tokenb and performing CRUD operations on tasks, verifying that only the authenticated user's tasks are accessible and modifiable

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for /api/tasks endpoints in backend/tests/integration/test_tasks.py
- [ ] T014 [P] [US1] Integration test for task CRUD journey in backend/tests/integration/test_tasks.py

### Implementation for User Story 1

- [x] T015 [P] [US1] Create Task model in backend/src/database/models/task.py
- [x] T016 [P] [US1] Create task request/response schemas in backend/src/schemas/task.py
- [x] T017 [US1] Implement task service with CRUD operations in backend/src/services/task_service.py
- [x] T018 [US1] Implement /api/tasks GET endpoint in backend/src/routes/tasks.py
- [x] T019 [US1] Implement /api/tasks POST endpoint in backend/src/routes/tasks.py
- [x] T020 [US1] Implement /api/tasks/{id} GET endpoint in backend/src/routes/tasks.py
- [x] T021 [US1] Implement /api/tasks/{id} PUT endpoint in backend/src/routes/tasks.py
- [x] T022 [US1] Implement /api/tasks/{id} DELETE endpoint in backend/src/routes/tasks.py
- [x] T023 [US1] Add proper error handling and validation for US1 endpoints
- [x] T024 [US1] Add logging for task operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure Authentication and Authorization (Priority: P1)

**Goal**: Ensure all API endpoints require JWT authentication and enforce strict task ownership policies to protect user data

**Independent Test**: Can be tested by attempting API calls with valid tokens, expired tokens, invalid tokens, and no tokens, verifying that only valid tokens grant access to owned resources

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US2] Contract test for authentication in backend/tests/integration/test_auth.py
- [ ] T026 [P] [US2] Integration test for unauthorized access attempts in backend/tests/integration/test_auth.py

### Implementation for User Story 2

- [x] T027 [P] [US2] Enhance JWT verification to extract user_id from token in backend/src/auth/jwt_handler.py
- [x] T028 [US2] Implement user ownership verification in backend/src/auth/dependencies.py
- [x] T029 [US2] Add authentication middleware to all task endpoints in backend/src/routes/tasks.py
- [x] T030 [US2] Implement user ownership checks in task service operations in backend/src/services/task_service.py
- [x] T031 [US2] Add 401 Unauthorized responses for invalid tokens
- [x] T032 [US2] Add 404 Not Found responses for non-owned tasks (to prevent enumeration)
- [x] T033 [US2] Update error handling to properly handle authentication failures

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task State Management (Priority: P2)

**Goal**: Enable users to update task properties including completion status, title, description, and due date through dedicated API endpoints

**Independent Test**: Can be tested by creating tasks, then updating their properties through appropriate endpoints, verifying that changes are persisted and reflected correctly

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T034 [P] [US3] Contract test for task state management endpoints in backend/tests/integration/test_tasks.py
- [ ] T035 [P] [US3] Integration test for task completion toggling in backend/tests/integration/test_tasks.py

### Implementation for User Story 3

- [x] T036 [P] [US3] Add PATCH /api/tasks/{id}/complete endpoint in backend/src/routes/tasks.py
- [x] T037 [US3] Implement toggle completion method in task service in backend/src/services/task_service.py
- [x] T038 [US3] Add proper validation for task state updates
- [x] T039 [US3] Implement filtering and sorting capabilities for GET /api/tasks in backend/src/services/task_service.py
- [x] T040 [US3] Add query parameter handling for status filtering and sorting in backend/src/routes/tasks.py
- [x] T041 [US3] Add title length validation (1-200 characters) in backend/src/schemas/task.py
- [x] T042 [US3] Add comprehensive error handling for edge cases

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T043 [P] Documentation updates in README.md
- [x] T044 Code cleanup and refactoring across all modules
- [x] T045 Performance optimization for database queries
- [x] T046 [P] Additional unit tests in backend/tests/unit/
- [x] T047 Security hardening and validation
- [x] T048 Run quickstart.md validation and update if needed
- [x] T049 Add comprehensive API documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/database/models/task.py"
Task: "Create task request/response schemas in backend/src/schemas/task.py"

# Launch all endpoints for User Story 1 together:
Task: "Implement /api/tasks GET endpoint in backend/src/routes/tasks.py"
Task: "Implement /api/tasks POST endpoint in backend/src/routes/tasks.py"
Task: "Implement /api/tasks/{id} GET endpoint in backend/src/routes/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence