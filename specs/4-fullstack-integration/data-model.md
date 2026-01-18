# Data Model: Full-Stack Integration

## 1. User Identity Model

### Structure
The user identity must remain consistent across all services to ensure proper integration.

```javascript
{
  "id": "string (UUID format)",
  "email": "string (email format)",
  "username": "string (alphanumeric with underscores/hyphens)",
  "firstName": "string (optional)",
  "lastName": "string (optional)",
  "isActive": "boolean",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime",
  "lastLoginAt": "ISO 8601 datetime (nullable)"
}
```

### Validation Rules
- User ID: Must be a valid UUID format
- Email: Must be a valid email format and unique
- Username: 3-30 characters, alphanumeric with underscores and hyphens only
- isActive: Defaults to true for new users

## 2. Task Entity Model

### Structure
The task entity must be consistent between frontend and backend representations.

```javascript
{
  "id": "integer (auto-generated)",
  "title": "string (1-200 characters)",
  "description": "string (nullable, up to 1000 characters)",
  "completed": "boolean (defaults to false)",
  "dueDate": "ISO 8601 datetime (nullable)",
  "userId": "string (foreign key to user id)",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime"
}
```

### Validation Rules
- Title: Required, 1-200 characters
- Description: Optional, maximum 1000 characters
- Completed: Boolean, defaults to false
- UserId: Must reference a valid user ID
- Due date: Optional, if provided must be a valid future date

## 3. JWT Token Structure

### Claims Format
The JWT token structure must be consistent between authentication service and backend validation.

```javascript
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-id (string)",
    "email": "user-email (string)",
    "username": "user-username (string)",
    "exp": "expiration timestamp (number)",
    "iat": "issued at timestamp (number)"
  }
}
```

### Validation Requirements
- Signature verification against shared secret
- Expiration time validation
- User ID presence validation
- Algorithm validation (HS256 only)

## 4. API Response Format

### Standard Response Structure
All API responses follow a consistent structure for predictable client handling.

```javascript
{
  "success": "boolean",
  "data": "object/array (nullable)",
  "error": "string (nullable)"
}
```

### Error Response Format
Specific format for error responses to enable consistent error handling.

```javascript
{
  "success": false,
  "data": null,
  "error": {
    "message": "string",
    "code": "string (error code)",
    "details": "object (optional, error-specific details)"
  }
}
```

## 5. Request Validation Schema

### Authentication Requests
Validation schema for authentication-related requests.

```javascript
// Login Request
{
  "email": "required, valid email format",
  "password": "required, 8-72 characters"
}

// Registration Request
{
  "email": "required, valid email format, unique",
  "username": "required, 3-30 alphanumeric with underscores/hyphens",
  "password": "required, 8-72 characters",
  "firstName": "optional, string",
  "lastName": "optional, string"
}
```

### Task Operation Requests
Validation schema for task-related operations.

```javascript
// Create Task Request
{
  "title": "required, 1-200 characters",
  "description": "optional, max 1000 characters",
  "dueDate": "optional, ISO 8601 datetime format",
  "completed": "optional, boolean (defaults to false)"
}

// Update Task Request
{
  "title": "optional, 1-200 characters",
  "description": "optional, max 1000 characters",
  "dueDate": "optional, ISO 8601 datetime format",
  "completed": "optional, boolean"
}
```

## 6. Session and Authentication Data

### Client-Side Storage
Structure for storing authentication data on the client side.

```javascript
{
  "accessToken": "JWT token string",
  "refreshToken": "Refresh token string (if applicable)",
  "user": "User object (as defined above)",
  "expiresAt": "ISO 8601 datetime for token expiration"
}
```

## 7. Audit Trail Structure

### User Action Tracking
Structure for tracking user actions for security and debugging purposes.

```javascript
{
  "action": "string (operation performed)",
  "userId": "string (user who performed action)",
  "resourceType": "string (type of resource affected)",
  "resourceId": "string/number (id of resource affected)",
  "timestamp": "ISO 8601 datetime",
  "ipAddress": "string (user IP address)",
  "userAgent": "string (browser/client information)"
}
```

## 8. State Transitions

### Task Status Transitions
Valid state transitions for task completion status.

- Pending (completed: false) ↔ Completed (completed: true)
- Both states can be updated with new properties while maintaining status

### Authentication State Transitions
Valid state transitions for user authentication.

- Unauthenticated → Authenticated (via login/register)
- Authenticated → Unauthenticated (via logout/expiry)
- Authenticated (valid token) → Authenticated (refreshed token)