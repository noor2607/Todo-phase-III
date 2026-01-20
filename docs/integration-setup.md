# Full-Stack Integration Setup Guide

## Overview
This document provides instructions for setting up the full-stack integration between the Next.js frontend, Better Auth authentication layer, and FastAPI backend for the Todo application using JWT-based stateless authentication.

## Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Docker and Docker Compose
- Git

## Architecture Overview
- **Frontend**: Next.js application serving user interface and client-side logic
- **Authentication**: Better Auth handling user registration, login, and session management
- **Backend**: FastAPI service managing business logic and data persistence
- **Database**: PostgreSQL for production, SQLite for development

## Local Development Setup

### Option 1: Manual Setup (Recommended for development)

#### 1. Clone the repository
```bash
git clone <repository-url>
cd todo-application
```

#### 2. Set up the backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your specific configuration

# Start the backend
uvicorn src.main:app --reload --port 8000
```

#### 3. Set up the frontend
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env file with your specific configuration

# Start the frontend
npm run dev
```

#### 4. Access the application
- Frontend: http://localhost:3000
- Backend API: https://larebnoor-todo-backend.hf.space/
- Backend API docs: https://larebnoor-todo-backend.hf.space/docs

### Option 2: Docker Setup (Recommended for production-like environment)

#### 1. Set up environment variables
Create a `.env` file at the root of the project:
```bash
# Backend variables
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
NEXTAUTH_SECRET=your-own-secret-here

# Database variables
POSTGRES_DB=todo_db
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=todo_password
```

#### 2. Build and start services
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

#### 3. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Database: localhost:5432 (internal use only)

## Environment Configuration

### Backend Environment Variables
- `DATABASE_URL`: Database connection string (e.g., `postgresql://user:password@localhost/dbname` or `sqlite:///./todo_app.db`)
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing (at least 32 characters)
- `JWT_ALGORITHM`: Algorithm for JWT signing (default: `HS256`)
- `JWT_EXPIRATION_HOURS`: Hours until JWT tokens expire (default: `24`)
- `ENVIRONMENT`: Environment mode (`development` or `production`)
- `LOG_LEVEL`: Logging level (`debug`, `info`, `warning`, `error`)

### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (e.g., `http://localhost:8000`)
- `NEXTAUTH_URL`: NextAuth base URL (e.g., `http://localhost:3000`)
- `NEXTAUTH_SECRET`: Secret for NextAuth signing

## API Contract Details

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Task Management Endpoints
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete specific task

## JWT Token Handling

### Frontend Implementation
- Centralized API client automatically attaches Authorization headers
- Tokens stored securely in browser storage (localStorage or sessionStorage)
- Automatic token removal on logout or session expiration
- Retry mechanisms for failed requests due to expired tokens

### Backend Implementation
- All protected endpoints validate JWT tokens using consistent middleware
- Token signature verification against configured secret key
- Expiration time validation to prevent use of expired tokens
- User identity extraction from token claims for authorization checks

## Error Handling

### Error Response Format
All error responses follow the consistent structure:
```json
{
  "success": false,
  "data": null,
  "error": "Descriptive error message"
}
```

### Error Types
- Authentication errors (401): Invalid credentials, expired tokens, unauthorized access
- Validation errors (422): Invalid input data, missing required fields
- System errors (500): Database connectivity issues, service unavailability
- Business logic errors (400): Constraint violations, business rule failures

## CORS Configuration

### Allowed Origins
- Production: Limited to deployed frontend domain
- Development: Localhost addresses with common ports
- Staging: Designated staging environment domains

### Allowed Methods and Headers
- Support for standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Authorization header for JWT token transmission
- Content-Type header for JSON data
- Custom headers as required by application functionality

## Security Considerations

### Data Protection
- All sensitive data encrypted in transit using HTTPS
- JWT tokens signed and verified using strong cryptographic algorithms
- Input validation to prevent injection attacks
- Secure storage of authentication credentials

### Access Control
- Principle of least privilege for all user operations
- User ownership validation for all task operations
- Regular security audits of authentication and authorization mechanisms
- Protection against common web vulnerabilities (XSS, CSRF, etc.)

## Testing Integration

### Authentication Flow Test
1. Register a new user via the frontend registration page
2. Verify JWT token is received and stored
3. Verify user can access protected task features
4. Verify token is attached to backend API requests

### Task Management Flow Test
1. Create a new task via the frontend
2. Verify task is created in the backend with correct ownership
3. Update the task and verify changes persist
4. Toggle task completion status and verify
5. Delete the task and verify it's removed

### Error Handling Test
1. Try to access protected endpoints without authentication
2. Verify 401 responses are handled correctly
3. Test expired token scenarios
4. Verify error messages are user-friendly

## Troubleshooting

### Common Issues
- **Cannot connect to backend API from frontend**: Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly and backend service is running
- **Authentication tokens not being sent with requests**: Check that authentication middleware is properly configured on both frontend and backend
- **CORS errors**: Verify backend CORS configuration allows frontend origin
- **Database connection errors**: Ensure `DATABASE_URL` is configured correctly and database service is accessible

### Debugging Tips
- Enable detailed logging in both frontend and backend
- Use browser developer tools to inspect network requests
- Check backend logs for authentication and authorization errors
- Verify JWT secret configuration matches between services