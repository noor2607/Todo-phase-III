# Quickstart Guide: Full-Stack Integration

## Environment Setup

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Docker and Docker Compose (for containerized setup)
- Git

### Environment Variables
Create `.env` files for each service with the following variables:

#### Backend (.env in backend directory)
```env
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
DATABASE_URL=sqlite:///./todo_app.db
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
ENVIRONMENT=development
LOG_LEVEL=info
```

#### Frontend (.env in frontend directory)
```env
NEXT_PUBLIC_API_BASE_URL=https://larebnoor-todo-backend.hf.space/
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

## Local Development Setup

### Option 1: Separate Services (Recommended for development)

1. **Start the backend service:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --port 8000
```

2. **Start the frontend service:**
```bash
cd frontend
npm install
npm run dev
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: https://larebnoor-todo-backend.hf.space/
- Backend API docs: https://larebnoor-todo-backend.hf.space/docs

### Option 2: Docker Compose (Recommended for production-like environment)

1. **Build and start all services:**
```bash
docker-compose up --build
```

2. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Integration Testing

### Basic Authentication Flow Test
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

## API Endpoints

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

## Troubleshooting

### Common Issues

**Issue:** Cannot connect to backend API from frontend
**Solution:** Verify NEXT_PUBLIC_API_BASE_URL is set correctly and backend service is running

**Issue:** Authentication tokens not being sent with requests
**Solution:** Check that authentication middleware is properly configured on both frontend and backend

**Issue:** CORS errors
**Solution:** Verify backend CORS configuration allows frontend origin

**Issue:** Database connection errors
**Solution:** Ensure DATABASE_URL is configured correctly and database service is accessible

### Debugging Tips
- Enable detailed logging in both frontend and backend
- Use browser developer tools to inspect network requests
- Check backend logs for authentication and authorization errors
- Verify JWT secret configuration matches between services