# Data Model: Backend Todo API

## Entity: Task
- **Fields**:
  - id: Integer (Primary Key, Auto-increment)
  - user_id: String (Indexed, Foreign Key reference to user)
  - title: String (Required, 1-200 characters)
  - description: String (Optional, nullable)
  - completed: Boolean (Default: False)
  - due_date: DateTime (Optional, nullable, ISO 8601 format)
  - created_at: DateTime (Auto-generated timestamp)
  - updated_at: DateTime (Auto-generated timestamp, updates on change)

- **Validation rules**:
  - Title must be 1-200 characters
  - Completed defaults to False
  - created_at and updated_at are automatically managed
  - user_id must match authenticated user's ID from JWT

- **Relationships**:
  - Belongs to one User (via user_id foreign key)
  - User can have many Tasks

## Entity: User (External Reference)
- **Reference only** (managed by Better Auth):
  - user_id: String (Extracted from JWT token)
  - No direct database storage of user details
  - Identity verified through JWT validation

## State Transitions
- **Task Creation**: New task with completed=False, created_at set to now
- **Task Update**: Fields updated with updated_at reflecting change time
- **Task Completion Toggle**: completed field flips between True/False
- **Task Deletion**: Record permanently removed from database

## Indexes
- Primary: id (auto)
- Foreign Key: user_id (for ownership queries)
- Additional: created_at (for sorting/filtering)