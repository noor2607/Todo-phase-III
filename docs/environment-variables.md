# Environment Variables: Todo Full-Stack Application

## Overview
This document lists all environment variables required for the Todo Full-Stack Application. These variables configure the application's behavior, security settings, database connections, and other runtime parameters.

## Backend Environment Variables

### Required Variables
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing and verification (min 32 characters)
  - Example: `BETTER_AUTH_SECRET=super-secret-jwt-key-at-least-32-characters-long`
  - Security: Critical for authentication security; must be kept secret

- `DATABASE_URL`: Database connection string
  - Example: `DATABASE_URL=sqlite:///./todo_app.db` (for SQLite)
  - Example: `DATABASE_URL=postgresql://user:password@localhost:5432/todo_db` (for PostgreSQL)
  - Security: Contains database credentials; restrict access

### Optional Variables
- `JWT_EXPIRATION_HOURS`: Number of hours until JWT tokens expire (default: 24)
  - Example: `JWT_EXPIRATION_HOURS=48`
  - Range: 1-168 hours (1-7 days)

- `ENVIRONMENT`: Environment mode (development, staging, production) (default: development)
  - Example: `ENVIRONMENT=production`
  - Values: `development`, `staging`, `production`

- `LOG_LEVEL`: Logging level (default: info)
  - Example: `LOG_LEVEL=debug`
  - Values: `debug`, `info`, `warning`, `error`

- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS (default: *)
  - Example: `ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://myapp.com`
  - Security: Restrict to specific origins in production

- `JWT_ALGORITHM`: Algorithm used for JWT token signing (default: HS256)
  - Example: `JWT_ALGORITHM=HS256`
  - Values: `HS256`, `HS384`, `HS512`

## Frontend Environment Variables

### Required Variables
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
  - Example: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
  - Note: Must be prefixed with `NEXT_PUBLIC_` to be accessible in browser

### Optional Variables
- `NEXT_PUBLIC_APP_NAME`: Name of the application (default: "Todo App")
  - Example: `NEXT_PUBLIC_APP_NAME="My Todo Application"`

- `NEXT_PUBLIC_LOG_LEVEL`: Client-side logging level (default: info)
  - Example: `NEXT_PUBLIC_LOG_LEVEL=warning`
  - Values: `debug`, `info`, `warning`, `error`

## Database Configuration

### SQLite (Default for Development)
- `DATABASE_URL`: `sqlite:///./todo_app.db`
  - Creates a local SQLite file database
  - Good for development and testing
  - Not suitable for production with multiple users

### PostgreSQL (Recommended for Production)
- `DATABASE_URL`: `postgresql://username:password@host:port/database_name`
  - Full-featured database for production
  - Supports concurrent users and advanced features
  - Requires PostgreSQL server setup

## Security Considerations

### Secrets Management
- Store secrets in secure vaults (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)
- Never commit secrets to version control
- Use different secrets for different environments
- Rotate secrets regularly

### Production Environment Variables
```
# Critical security settings
BETTER_AUTH_SECRET=your-production-jwt-secret-here-ensure-at-least-32-chars
DATABASE_URL=postgresql://prod_user:prod_password@prod_host:5432/todo_prod_db

# Production-specific settings
ENVIRONMENT=production
LOG_LEVEL=warning
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
JWT_EXPIRATION_HOURS=24
```

### Development Environment Variables
```
# Development settings
BETTER_AUTH_SECRET=dev-secret-for-local-development-only-min-32-chars
DATABASE_URL=sqlite:///./todo_dev.db

# Development-specific settings
ENVIRONMENT=development
LOG_LEVEL=debug
ALLOWED_ORIGINS=*
JWT_EXPIRATION_HOURS=168  # Longer for convenience during development
```

## Docker Environment Variables

When deploying with Docker, environment variables can be set in a `.env` file:

```
# .env file for Docker deployment
BETTER_AUTH_SECRET=your-docker-secret-here-min-32-chars
DATABASE_URL=postgresql://docker_user:docker_password@db:5432/todo_db
ENVIRONMENT=docker
LOG_LEVEL=info
ALLOWED_ORIGINS=http://localhost:3000
JWT_EXPIRATION_HOURS=24
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Testing Environment Variables

For testing environments, use separate configurations:

```
# Test environment settings
BETTER_AUTH_SECRET=test-secret-for-unit-tests-min-32-chars
DATABASE_URL=sqlite:///./test_todo_app.db
ENVIRONMENT=testing
LOG_LEVEL=error
ALLOWED_ORIGINS=*
JWT_EXPIRATION_HOURS=168
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Configuration Validation

The application validates required environment variables at startup. If any required variable is missing, the application will log an error and exit.

## Security Best Practices

1. **Secret Rotation**: Rotate `BETTER_AUTH_SECRET` regularly (recommended monthly for production)
2. **Origin Restrictions**: In production, never use `ALLOWED_ORIGINS=*`
3. **Environment Separation**: Use different secrets for development, staging, and production
4. **Access Control**: Restrict file system access to environment variable files
5. **Monitoring**: Monitor access to secrets and environment variable files
6. **Logging**: Do not log sensitive environment variables in production

## Troubleshooting Common Issues

### JWT Secret Issues
- Problem: "Invalid token" or "Could not validate credentials" errors
- Solution: Verify `BETTER_AUTH_SECRET` matches between frontend and backend

### Database Connection Issues
- Problem: "Database connection failed" errors
- Solution: Verify `DATABASE_URL` format and database accessibility

### CORS Issues
- Problem: "Cross-Origin Request Blocked" errors
- Solution: Ensure `ALLOWED_ORIGINS` includes your frontend domain

### Authentication Issues
- Problem: Users cannot log in or register
- Solution: Check that JWT settings are properly configured and secrets match