# Data Model: Authentication-Only System

## Entity: User Identity
- **Fields**:
  - userId: String (Unique identifier from JWT token)
  - email: String (Email address for authentication)
  - createdAt: DateTime (Account creation timestamp)
  - updatedAt: DateTime (Last account update timestamp)

- **Validation rules**:
  - Email must be valid email format
  - Email must be unique across system
  - userId must be immutable after creation

- **Relationships**:
  - Links to user's todo data in backend (via userId in JWT)

## Entity: JWT Token
- **Fields**:
  - token: String (Encoded JWT token)
  - userId: String (Embedded user identifier)
  - exp: Number (Expiration timestamp)
  - iat: Number (Issued at timestamp)
  - sub: String (Subject - typically user ID)

- **Validation rules**:
  - Token must have valid signature
  - Token must not be expired
  - Token must contain valid user identifier
  - Token must be signed with correct secret

- **State Transitions**:
  - Valid → Expired (automatically at expiration time)
  - Valid → Revoked (through logout process)

## Entity: Session State (Client-side)
- **Fields**:
  - isAuthenticated: Boolean (Login status)
  - user: Object (User identity information)
  - token: String (Current JWT token)
  - refreshToken: String (Refresh token if applicable)
  - expiresAt: DateTime (Token expiration time)

- **Validation rules**:
  - Session must be cleared on logout
  - Session must be validated before API calls
  - Session must be checked for expiration

## Security Properties
- Tokens must be signed with BETTER_AUTH_SECRET
- Token payloads must not contain sensitive information
- Token expiration must be enforced on both client and server
- User identity must be extracted from verified token, not client input