# Quickstart Guide: Authentication-Only System

## Setup Instructions

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies**
   ```bash
   # Frontend
   cd frontend
   npm install better-auth react react-dom next

   # Backend
   cd backend
   pip install fastapi pyjwt python-multipart python-jose[cryptography]
   ```

3. **Configure environment variables**
   Create `.env.local` file with:
   ```bash
   # Frontend
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-key-here

   # Backend
   BETTER_AUTH_SECRET=your-jwt-secret-key-here
   ```

4. **Initialize Better Auth on frontend**
   ```typescript
   // lib/auth.ts
   import { initClient } from "better-auth/client";

   export const authClient = initClient({
     baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL!,
     // Configuration options
   });
   ```

5. **Start the development servers**
   ```bash
   # Terminal 1: Start backend
   cd backend
   uvicorn main:app --reload --port 8000

   # Terminal 2: Start frontend
   cd frontend
   npm run dev
   ```

## Authentication Flows

### User Signup
1. Navigate to `/sign-up` page
2. Enter valid email and password
3. Submit form to create account
4. Receive JWT token upon successful registration

### User Signin
1. Navigate to `/sign-in` page
2. Enter registered email and password
3. Submit form to authenticate
4. Receive JWT token upon successful authentication

### Protected Route Access
1. Attempt to access protected route (e.g., `/dashboard`)
2. If unauthenticated, redirect to `/sign-in`
3. If authenticated, allow access to route
4. Attach JWT token to all API requests automatically

### User Logout
1. Trigger logout action (button/click)
2. Clear JWT token from client storage
3. Redirect to public area (e.g., home page)
4. Prevent access to protected routes until re-authentication

## Backend JWT Verification

All backend API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

The backend will:
- Verify JWT signature using BETTER_AUTH_SECRET
- Validate token expiration
- Extract user identity from token payload
- Reject requests with invalid/missing tokens with 401 status

## Testing

Run frontend tests:
```bash
npm run test:auth
```

Run backend tests:
```bash
pytest tests/auth/
```

## Environment Variables

### Frontend
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth server URL
- `NEXT_PUBLIC_JWT_SECRET`: JWT signing secret

### Backend
- `BETTER_AUTH_SECRET`: JWT verification secret
- `JWT_EXPIRATION_HOURS`: Token expiration timeframe
- `JWT_ALGORITHM`: Algorithm used for signing (default: HS256)