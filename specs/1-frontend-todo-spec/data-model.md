# Data Model: Todo Frontend Application

## Task Entity
- **id**: string (UUID) - Unique identifier for the task
- **title**: string (required, max 255 characters) - Task title
- **description**: string (optional, max 1000 characters) - Task description
- **completed**: boolean - Completion status of the task
- **createdAt**: string (ISO 8601 format) - Timestamp when task was created
- **updatedAt**: string (ISO 8601 format) - Timestamp when task was last updated
- **userId**: string (from JWT token) - Owner of the task

### Validation Rules
- title must be between 1 and 255 characters
- description must be maximum 1000 characters if provided
- completed must be a boolean value
- createdAt and updatedAt must be valid ISO 8601 timestamps
- userId must match the authenticated user's ID from JWT token

### State Transitions
- Task starts as incomplete (completed: false)
- Task can transition to completed (completed: true)
- Task can transition back to incomplete (completed: false)
- Task can be deleted (removed from user's task list)

## User Session Entity
- **token**: string (JWT) - Authentication token
- **user**: object - User profile information
  - id: string - User ID
  - email: string - User email
  - name: string - User name (optional)
- **expiresAt**: string (ISO 8601 format) - Token expiration time
- **lastActivity**: string (ISO 8601 format) - Last activity timestamp

### Validation Rules
- token must be a valid JWT
- user.id must be present
- user.email must be a valid email format
- expiresAt must be a future timestamp
- lastActivity must be current or past timestamp