# Application Constitution: Todo Full-Stack Web Application

## Project Vision and Scope

### Vision Statement
To create a secure, scalable, and responsive multi-user todo application that enables individuals to manage their personal tasks efficiently while maintaining strict data isolation and privacy.

### In Scope
- Multi-user todo management system with full CRUD operations
- Responsive web interface supporting desktop and mobile devices
- Secure authentication and authorization with user isolation
- Persistent storage in PostgreSQL database
- Real-time task synchronization across devices
- Modern UI/UX with Next.js App Router and Tailwind CSS

### Out of Scope
- File attachments or rich media in tasks
- Collaborative sharing of individual tasks between users
- Advanced analytics or reporting features
- Offline-first functionality
- Email notifications or reminders
- Third-party integrations beyond authentication

### Non-Negotiable Constraints
- Serverless deployment on Vercel for frontend, with serverless PostgreSQL
- Complete separation of frontend and backend services
- Stateless JWT-based authentication system
- All user data must remain isolated and private
- Zero-trust principle: backend never trusts client-provided user identifiers

## Responsibilities by Layer

### Frontend (Next.js 14+ App Router)
- Handle user interface rendering and user experience
- Implement responsive design with Tailwind CSS
- Manage client-side state and form validation
- Coordinate with backend via standardized API calls
- Implement client components only where interactivity is required
- Route management using Next.js App Router conventions
- Client-side navigation and loading states

### Backend (Python FastAPI)
- Process all business logic and data validation
- Enforce authentication and authorization rules
- Manage database transactions and data persistence
- Implement REST API endpoints under /api/ path
- Handle error responses with consistent format
- Validate JWT tokens for all authenticated routes
- Ensure data integrity and user isolation

### Authentication (Better Auth + JWT)
- Issue and verify JWT tokens for authenticated users
- Manage user registration, login, and session management
- Provide secure password hashing and recovery mechanisms
- Verify token validity and expiration on all protected routes
- Handle refresh token rotation and security
- Maintain authentication statelessness

### Integration Layer
- Define API contracts between frontend and backend
- Ensure consistent data serialization and deserialization
- Handle CORS policies and security headers
- Implement request/response validation
- Manage environment configuration and secrets
- Coordinate deployment and service communication

## Security Guarantees

### User Data Isolation
- Each user can only access their own tasks and data
- Backend must verify user ownership for every data access request
- Database queries must always filter by authenticated user ID
- No direct user-to-user data access is permitted
- Cross-user data leakage is absolutely prohibited

### Token Verification Requirements
- All protected routes must validate JWT tokens
- Backend must decode and verify token signature without trusting client
- Token expiration must be enforced on all requests
- User identity must be extracted from token payload, not client request
- Invalid or expired tokens must result in 401 Unauthorized responses

### Ownership Enforcement
- Every database query must include user_id filter from verified token
- Write operations must validate that user owns the resource
- Delete operations must confirm user ownership before deletion
- Unauthorized access attempts must be logged for security monitoring
- Resource identifiers must be globally unique to prevent enumeration

### Data Protection
- All sensitive data must be encrypted in transit (HTTPS only)
- Passwords must never be stored in plaintext
- Environment variables must be used for all secrets
- Database connections must use SSL encryption
- Audit trails must be maintained for security-relevant operations

## API Contract Invariants

### Standard Response Format
- Successful responses: `{ "success": true, "data": {...} }`
- Error responses: `{ "success": false, "error": "error_message" }`
- HTTP status codes must align with response content
- All dates must be in ISO 8601 format (UTC)
- Pagination responses must include metadata when applicable

### Authentication Headers
- All protected endpoints require `Authorization: Bearer <token>` header
- Unauthenticated requests must return 401 Unauthorized
- Malformed or invalid tokens must return 401 Unauthorized
- Expired tokens must return 401 Unauthorized with refresh instructions
- Authentication failure details must not expose sensitive information

### Error Handling Standards
- 400 Bad Request: Invalid input data or malformed requests
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Insufficient permissions for resource
- 404 Not Found: Requested resource does not exist
- 500 Internal Server Error: Unexpected server errors

### Request Validation
- All input parameters must be validated before processing
- Type checking and format validation required for all fields
- Maximum length limits must be enforced for text fields
- Rate limiting must be implemented to prevent abuse
- SQL injection prevention through parameterized queries

## Database Integrity Rules

### Schema Requirements
- All tables must have proper foreign key relationships
- User ID must be indexed for performance on all user-owned tables
- Created_at and updated_at timestamps required on all tables
- Soft deletes preferred over hard deletes where applicable
- Proper constraints to prevent orphaned records

### Data Consistency
- All database transactions must maintain ACID properties
- Concurrent access must be handled with proper locking
- Referential integrity must be enforced at database level
- Unique constraints must prevent duplicate user resources
- Cascade delete rules must be carefully defined

### ORM Usage (SQLModel)
- All database operations must use SQLModel ORM
- Raw SQL queries are prohibited unless absolutely necessary
- Proper session management with connection pooling
- Transaction boundaries must be clearly defined
- Query optimization must be performed for performance

## Error Handling Standards

### Backend Error Responses
- Use consistent error response format across all endpoints
- Log errors with sufficient context for debugging
- Never expose internal implementation details in error messages
- Map exceptions to appropriate HTTP status codes
- Include correlation IDs for distributed tracing

### Frontend Error Handling
- Display user-friendly error messages for client-facing errors
- Show loading states during API operations
- Implement retry mechanisms for transient failures
- Gracefully degrade functionality when services are unavailable
- Maintain offline capability awareness where possible

### Logging Requirements
- Log all authentication attempts (success and failure)
- Log security-relevant operations and access violations
- Include request IDs for traceability across services
- Follow structured logging format with consistent fields
- Ensure sensitive data is not logged in plaintext

## Naming Conventions

### File and Directory Structure
- Use kebab-case for file names: `user-tasks.tsx`
- Use PascalCase for React components: `UserTasks.tsx`
- Use snake_case for Python files: `user_routes.py`
- Group related files in feature-based directories
- Maintain consistent casing across frontend and backend

### Variable and Function Names
- Use camelCase for JavaScript/TypeScript variables and functions
- Use snake_case for Python variables and functions
- Use PascalCase for React components and TypeScript interfaces
- Use UPPER_SNAKE_CASE for constants and environment variables
- Use descriptive names that clearly indicate purpose

### Database Naming
- Use snake_case for table and column names
- Prefix foreign keys with table name: `user_id`, `task_id`
- Use plural names for tables: `users`, `tasks`
- Use descriptive names that indicate relationship: `created_by_user_id`
- Follow SQLModel naming conventions consistently

## Folder Structure Invariants

### Frontend Structure
```
app/
├── (auth)/          # Authentication-related pages
├── dashboard/       # Main application views
├── api/            # Client-side API route handlers
├── components/     # Reusable UI components
├── lib/           # Shared utilities and API clients
└── globals.css    # Global styles
```

### Backend Structure
```
src/
├── models/         # SQLModel database models
├── schemas/        # Pydantic request/response schemas
├── routes/         # API route definitions
├── auth/          # Authentication utilities
├── database/      # Database connection and session management
└── main.py       # Application entry point
```

### Mandatory Directories
- `/lib/api.ts` must contain all frontend API communication logic
- `/src/routes/` must contain all backend API route definitions
- `/src/models/` must contain all database models
- `/components/ui/` must contain reusable UI components
- `/src/auth/` must contain all authentication utilities

## Non-Goals and Forbidden Behaviors

### Prohibited Actions
- Direct database access from frontend applications
- Storing sensitive data in browser localStorage without encryption
- Hardcoding secrets or credentials in source code
- Bypassing authentication on any user-protected routes
- Sharing user data between different authenticated users

### Implementation Restrictions
- No client-side user ID manipulation in API requests
- No direct SQL queries bypassing ORM layer
- No synchronous operations that block event loop
- No global state mutation without proper validation
- No direct database connections without connection pooling

### Architecture Violations
- Mixing frontend and backend logic in same service
- Storing session state on server (stateless requirement)
- Trusting user-provided IDs without token verification
- Implementing business logic in database triggers
- Using cookies for authentication (JWT-only policy)

## Quality Gates for Generated Code

### Code Review Standards
- All code must pass type checking (TypeScript and Python)
- All database queries must use ORM (no raw SQL without approval)
- All API routes must implement proper authentication validation
- All user inputs must be validated before processing
- All error cases must be properly handled and logged

### Testing Requirements
- Unit tests must cover all business logic functions
- Integration tests must verify API contract compliance
- Security tests must validate authentication enforcement
- Performance tests must confirm acceptable response times
- All tests must pass before code acceptance

### Documentation Standards
- All public functions must have proper documentation
- API endpoints must be documented with request/response examples
- Security-sensitive functions must include security notes
- Configuration requirements must be clearly documented
- Deployment instructions must be included

### Security Validation
- Static code analysis must pass security scanning
- Dependency vulnerabilities must be addressed before merging
- Authentication flows must be validated by security team
- Database queries must be reviewed for injection vulnerabilities
- All secrets must be properly configured through environment variables

---

**This constitution serves as the highest-priority rule set for all future specifications, plans, tasks, and implementations. All agents and generated code must comply with these principles and constraints.**
