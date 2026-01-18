# API Contracts: Full-Stack Integration

## Authentication Endpoints

### User Registration
```
POST /api/auth/register
```

#### Request
```json
{
  "email": "string (required, valid email format)",
  "username": "string (required, 3-30 alphanumeric with underscores/hyphens)",
  "password": "string (required, 8-72 characters)",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

#### Response
**Success (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string (UUID)",
      "email": "string",
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "is_active": "boolean",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime",
      "last_login_at": "ISO 8601 datetime (nullable)"
    },
    "token": "string (JWT)"
  }
}
```

**Error (409 Conflict - Duplicate):**
```json
{
  "success": false,
  "error": "A user with this email/username already exists"
}
```

### User Login
```
POST /api/auth/login
```

#### Request
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string (UUID)",
      "email": "string",
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "is_active": "boolean",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime",
      "last_login_at": "ISO 8601 datetime (nullable)"
    },
    "token": "string (JWT)"
  }
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

### Get User Profile
```
GET /api/auth/profile
```

#### Headers
```
Authorization: Bearer {jwt_token}
```

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "string (UUID)",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "is_active": "boolean",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "last_login_at": "ISO 8601 datetime (nullable)"
  }
}
```

## Task Management Endpoints

### Get All Tasks
```
GET /api/tasks
```

#### Headers
```
Authorization: Bearer {jwt_token}
```

#### Query Parameters
- `status` (optional): "all", "completed", or "pending"
- `sort` (optional): "created_at", "due_date", or "title"

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "integer",
      "title": "string",
      "description": "string (nullable)",
      "completed": "boolean",
      "due_date": "ISO 8601 datetime (nullable)",
      "user_id": "string (UUID)",
      "created_at": "ISO 8601 datetime",
      "updated_at": "ISO 8601 datetime"
    }
  ]
}
```

### Create New Task
```
POST /api/tasks
```

#### Headers
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### Request
```json
{
  "title": "string (required, 1-200 characters)",
  "description": "string (optional, max 1000 characters)",
  "completed": "boolean (optional, default false)",
  "due_date": "ISO 8601 datetime (optional)"
}
```

#### Response
**Success (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "title": "string",
    "description": "string (nullable)",
    "completed": "boolean",
    "due_date": "ISO 8601 datetime (nullable)",
    "user_id": "string (UUID)",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

### Get Specific Task
```
GET /api/tasks/{id}
```

#### Headers
```
Authorization: Bearer {jwt_token}
```

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "title": "string",
    "description": "string (nullable)",
    "completed": "boolean",
    "due_date": "ISO 8601 datetime (nullable)",
    "user_id": "string (UUID)",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Task not found"
}
```

### Update Task
```
PUT /api/tasks/{id}
```

#### Headers
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### Request
```json
{
  "title": "string (optional, 1-200 characters)",
  "description": "string (optional, max 1000 characters)",
  "completed": "boolean (optional)",
  "due_date": "ISO 8601 datetime (optional)"
}
```

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "title": "string",
    "description": "string (nullable)",
    "completed": "boolean",
    "due_date": "ISO 8601 datetime (nullable)",
    "user_id": "string (UUID)",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

### Toggle Task Completion
```
PATCH /api/tasks/{id}/complete
```

#### Headers
```
Authorization: Bearer {jwt_token}
```

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "integer",
    "title": "string",
    "description": "string (nullable)",
    "completed": "boolean",
    "due_date": "ISO 8601 datetime (nullable)",
    "user_id": "string (UUID)",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

### Delete Task
```
DELETE /api/tasks/{id}
```

#### Headers
```
Authorization: Bearer {jwt_token}
```

#### Response
**Success (200 OK):**
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

## Error Response Format

All error responses follow the same structure:

**Client Errors (4xx):**
```json
{
  "detail": "Human-readable error message"
}
```

**Server Errors (5xx):**
```json
{
  "detail": "Internal server error occurred"
}
```

## Authentication Error Responses

**Unauthorized (401):**
```json
{
  "detail": "Not authenticated, Authorization header missing or invalid format"
}
```

**Invalid Token (401):**
```json
{
  "detail": "Could not validate credentials - invalid token"
}
```

**Expired Token (401):**
```json
{
  "detail": "Token has expired"
}
```