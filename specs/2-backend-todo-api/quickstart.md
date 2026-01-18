# Quickstart Guide: Backend Todo API

## Setup Instructions

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Copy `.env.example` to `.env` and set:
   ```bash
   DATABASE_URL="postgresql://username:password@localhost:5432/todo_db"
   BETTER_AUTH_SECRET="your-secret-key-here"
   ```

4. **Initialize database**
   ```bash
   # Run database migrations
   python -c "from src.database.engine import init_db; init_db()"
   ```

5. **Start the development server**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## API Endpoints

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Task Operations

**GET** `/api/tasks`
- Query parameters: `status` (all/completed/pending), `sort` (created_at/due_date)
- Returns: Array of user's tasks

**POST** `/api/tasks`
- Body: `{ "title": "Task title", "description": "Optional description", "due_date": "ISO datetime" }`
- Returns: Created task object

**GET** `/api/tasks/{id}`
- Returns: Specific task if owned by user

**PUT** `/api/tasks/{id}`
- Body: `{ "title": "Updated title", "description": "Updated description", "due_date": "ISO datetime", "completed": true/false }`
- Returns: Updated task object

**PATCH** `/api/tasks/{id}/complete`
- Toggles completion status
- Returns: Updated task object

**DELETE** `/api/tasks/{id}`
- Deletes the task if owned by user
- Returns: Success confirmation

## Testing

Run unit tests:
```bash
pytest tests/unit/
```

Run integration tests:
```bash
pytest tests/integration/
```

Run all tests:
```bash
pytest
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT verification
- `ENVIRONMENT`: dev/prod/staging
- `LOG_LEVEL`: debug/info/warn/error