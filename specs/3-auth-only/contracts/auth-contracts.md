# Contract: Authentication System API Specifications

## Frontend Authentication Interface

### Better Auth Client Initialization
- **Purpose**: Initialize Better Auth client on frontend
- **Method**: `initClient(config)`
- **Parameters**:
  - `baseURL`: Authentication server URL
  - `headers`: Optional headers configuration
- **Returns**: Auth client instance with signup/signin/logout methods

### User Signup Flow
- **Trigger**: User visits `/sign-up` page and submits form
- **Input**: `{ email: string, password: string }`
- **Processing**:
  - Validate email format and password strength
  - Send signup request to Better Auth
  - Receive JWT token on success
- **Output**: `{ success: boolean, token?: string, error?: string }`

### User Signin Flow
- **Trigger**: User visits `/sign-in` page and submits credentials
- **Input**: `{ email: string, password: string }`
- **Processing**:
  - Validate credentials format
  - Send signin request to Better Auth
  - Receive JWT token on success
- **Output**: `{ success: boolean, token?: string, error?: string }`

### User Logout Flow
- **Trigger**: User triggers logout action
- **Processing**:
  - Clear JWT token from client storage
  - Invalidate session state
  - Redirect to public area
- **Output**: `{ success: boolean }`

## Backend JWT Verification Contract

### JWT Token Verification
- **Purpose**: Verify JWT tokens for all authenticated API requests
- **Method**: Middleware function applied to protected routes
- **Input**: `Authorization: Bearer <token>` header
- **Processing**:
  - Extract token from Authorization header
  - Verify token signature using BETTER_AUTH_SECRET
  - Validate token expiration
  - Extract user identity from token payload
- **Output**:
  - Valid token: Continue to route handler with user identity
  - Invalid token: Return 401 Unauthorized response

### Token Payload Structure
- **Required Claims**:
  - `sub`: Subject (user ID)
  - `exp`: Expiration time (Unix timestamp)
  - `iat`: Issued at time (Unix timestamp)
- **Optional Claims**:
  - `email`: User email address
  - `name`: User display name

## Protected Route Handling

### Frontend Route Protection
- **Method**: Next.js middleware in `middleware.ts`
- **Logic**:
  - Check for valid JWT token in cookies/localStorage
  - If no valid token, redirect to `/sign-in`
  - If valid token, allow access to protected routes
- **Protected Routes**: All routes under `/dashboard`, `/api/private/*`

### API Request Authorization
- **Method**: Interceptor in API client
- **Logic**:
  - Attach JWT token to Authorization header for all requests to `/api/*`
  - Handle 401 responses by redirecting to login
- **Header Format**: `Authorization: Bearer <jwt-token>`

## Failure Scenarios and Error Handling

### Authentication Failure
- **Scenario**: Invalid credentials provided during signin
- **Response**: `{ success: false, error: "Invalid email or password" }`
- **Frontend Action**: Display error message to user

### Token Expiration
- **Scenario**: JWT token has expired
- **Response**: 401 Unauthorized from backend
- **Frontend Action**: Redirect to login page with notification

### Network Error
- **Scenario**: Authentication server unavailable
- **Response**: Network error
- **Frontend Action**: Display connection error and retry option

### Token Tampering
- **Scenario**: JWT signature verification fails
- **Response**: 401 Unauthorized from backend
- **Frontend Action**: Clear stored tokens and redirect to login