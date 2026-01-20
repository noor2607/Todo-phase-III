# Environment Setup Guide

## Required Environment Variables

### Backend (FastAPI) Environment Variables

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./todo_app.db` | Yes |
| `BETTER_AUTH_SECRET` | JWT signing secret for authentication | `your-super-secret-jwt-key-here` | Yes |
| `JWT_ALGORITHM` | JWT algorithm to use | `HS256` | No |
| `JWT_EXPIRATION_HOURS` | Hours until JWT tokens expire | `24` | No |
| `ENVIRONMENT` | Environment mode (development/production) | `development` | No |
| `LOG_LEVEL` | Logging level | `info` | No |

### Frontend (Next.js) Environment Variables

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL | `https://larebnoor-todo-backend.hf.space/` | Yes |
| `NEXTAUTH_URL` | NextAuth base URL | `http://localhost:3000` | Yes |
| `NEXTAUTH_SECRET` | NextAuth signing secret | `fallback-dev-secret` | Yes |

## Local Development Setup

### Backend Setup

1. Create a `.env` file in the `backend` directory:

```bash
DATABASE_URL=sqlite:///./todo_app.db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
ENVIRONMENT=development
LOG_LEVEL=info
```

2. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup

1. Create a `.env` file in the `frontend` directory:

```bash
NEXT_PUBLIC_API_BASE_URL=https://larebnoor-todo-backend.hf.space/
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-own-secret-here
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Docker Setup

When using Docker, environment variables can be set in a `.env` file at the root of the project:

```bash
# Backend variables
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
NEXTAUTH_SECRET=your-own-secret-here

# Database variables
POSTGRES_DB=todo_db
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=todo_password
```

## Production Deployment

For production deployments, ensure the following:

1. Use strong, unique secrets for `BETTER_AUTH_SECRET` and `NEXTAUTH_SECRET`
2. Use a production-grade database (PostgreSQL, MySQL, etc.)
3. Set `ENVIRONMENT` to `production`
4. Adjust `LOG_LEVEL` to `warning` or `error` for reduced verbosity
5. Use HTTPS for all API URLs
6. Ensure JWT expiration times are appropriate for your security requirements

## Security Recommendations

- Never commit secrets to version control
- Use different secrets for different environments
- Rotate secrets periodically
- Use environment-specific secrets (dev, staging, prod)
- Use a secrets management system in production environments