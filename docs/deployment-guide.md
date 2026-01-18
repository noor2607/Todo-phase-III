# Deployment Guide: Todo Full-Stack Application

## Overview
This guide provides instructions for deploying the Todo Full-Stack Application to production environments. The application consists of a Next.js frontend and a FastAPI backend with JWT-based authentication.

## Prerequisites

### Infrastructure Requirements
- Container orchestration platform (Docker Swarm, Kubernetes, or ECS)
- Load balancer for traffic distribution
- SSL certificate for HTTPS
- Database server (PostgreSQL recommended for production)
- DNS management for domain configuration

### Environment Requirements
- Docker and Docker Compose installed
- Domain name configured and pointing to deployment environment
- SSL certificate installed (or Let's Encrypt configured)
- Sufficient compute resources (minimum 2GB RAM, 2 CPU cores)

## Environment Configuration

### Backend Environment Variables
Create a `.env` file for the backend service:

```bash
# JWT Configuration
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-replace-with-actual-32-char-secret

# Database Configuration
DATABASE_URL=postgresql://username:password@database-host:5432/todo_production

# Environment Configuration
ENVIRONMENT=production
LOG_LEVEL=info

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# JWT Settings
JWT_EXPIRATION_HOURS=24
JWT_ALGORITHM=HS256
```

### Frontend Environment Variables
Create a `.env.production` file for the frontend service:

```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com

# Application Settings
NEXT_PUBLIC_APP_NAME="Todo Application"
NEXT_PUBLIC_LOG_LEVEL=info
```

## Docker-Based Deployment

### Building Docker Images

#### Backend Image
```bash
cd backend
docker build -t todo-backend:latest .
```

#### Frontend Image
```bash
cd frontend
docker build -t todo-frontend:latest .
```

### Docker Compose Deployment
Create a `docker-compose.prod.yml` file:

```yaml
version: '3.8'

services:
  backend:
    image: todo-backend:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - ENVIRONMENT=production
      - LOG_LEVEL=info
      - ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: unless-stopped
    networks:
      - app-network

  frontend:
    image: todo-frontend:latest
    environment:
      - NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=todo_production
      - POSTGRES_USER=todo_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

Deploy with:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Kubernetes Deployment

### Deploy Secrets
First, create the necessary secrets:

```bash
kubectl create secret generic todo-secrets \
  --from-literal=database-url="postgresql://username:password@database-host:5432/todo_production" \
  --from-literal=auth-secret="your-super-secret-jwt-key-here-replace-with-actual-32-char-secret"
```

### Deploy Application
Apply the deployment configuration:

```bash
kubectl apply -f deploy/deployment-config.yaml
```

## Configuration Steps

### 1. Database Setup
1. Set up PostgreSQL database (version 12 or higher)
2. Configure database connection pooling
3. Set up backup and maintenance schedules
4. Create database user with appropriate permissions

### 2. Authentication Configuration
1. Generate secure JWT secret (at least 32 characters)
2. Configure token expiration time (recommended: 24 hours)
3. Set up allowed origins for CORS
4. Test authentication flow

### 3. SSL/HTTPS Configuration
1. Obtain SSL certificate for your domain
2. Configure reverse proxy (nginx, Apache, or cloud provider)
3. Set up automatic certificate renewal (e.g., Let's Encrypt)
4. Force HTTPS redirects

### 4. Health Checks
1. Configure health check endpoints:
   - Backend: `GET /health` (should return 200 OK)
   - Frontend: `GET /` (should return 200 OK)
2. Set up monitoring for these endpoints
3. Configure alerts for service downtime

## Security Hardening

### 1. Secrets Management
- Store secrets in secure vault (HashiCorp Vault, AWS Secrets Manager, etc.)
- Use different secrets for different environments
- Rotate secrets regularly
- Restrict access to secrets

### 2. Network Security
- Configure firewall rules to limit access
- Use private networks for internal communication
- Enable SSL/TLS for all connections
- Implement rate limiting

### 3. Authentication Security
- Use strong password policies
- Implement account lockout after failed attempts
- Enable two-factor authentication (if applicable)
- Regularly audit authentication logs

## Monitoring and Logging

### 1. Application Metrics
- Monitor API response times
- Track error rates
- Monitor user authentication patterns
- Track task operations volume

### 2. Infrastructure Metrics
- CPU and memory utilization
- Database connection pool usage
- Network I/O
- Disk space usage

### 3. Log Management
- Centralize logs using ELK stack or similar
- Set up log retention policies
- Configure alerts for critical errors
- Implement structured logging

## Backup and Recovery

### 1. Database Backups
- Schedule regular database backups
- Test backup restoration procedures
- Store backups in secure, separate location
- Encrypt backups in transit and at rest

### 2. Configuration Backups
- Version control for deployment configurations
- Backup environment variables and secrets
- Document recovery procedures

## Scaling Configuration

### Horizontal Scaling
- Configure load balancer for multiple backend instances
- Implement session-less authentication (JWT)
- Use external database instead of local storage
- Set up health checks for auto-scaling

### Vertical Scaling
- Monitor resource utilization
- Plan for resource increases based on usage patterns
- Configure resource limits and requests in containers

## Post-Deployment Verification

### 1. Functionality Testing
- Verify user registration and login
- Test task creation, update, and deletion
- Confirm authentication enforcement
- Validate error handling

### 2. Performance Testing
- Test API response times under load
- Verify concurrent user support
- Check for memory leaks
- Validate database connection handling

### 3. Security Testing
- Verify authentication tokens work correctly
- Test unauthorized access prevention
- Validate input sanitization
- Check for security headers

## Troubleshooting Common Issues

### 1. Database Connection Issues
- Verify database URL format
- Check database credentials
- Confirm database server accessibility
- Review connection pooling settings

### 2. Authentication Failures
- Verify JWT secret matches between services
- Check token expiration settings
- Validate CORS configuration
- Review authentication flow

### 3. Frontend-Backend Communication
- Confirm API base URL configuration
- Check network connectivity between services
- Verify SSL certificate validity
- Review proxy configuration

## Rollback Procedure

If issues occur after deployment:

1. Document the issue and symptoms
2. Switch traffic back to previous version
3. Investigate and fix the issue
4. Test fix in staging environment
5. Redeploy the corrected version

## Maintenance Schedule

### Daily Tasks
- Monitor application logs
- Check system health
- Review error metrics
- Verify backup completion

### Weekly Tasks
- Update security patches
- Review access logs
- Check for performance trends
- Update documentation as needed

### Monthly Tasks
- Rotate authentication secrets
- Review security configurations
- Update dependencies
- Performance tuning as needed

## Contact Information
- Primary Support: [support@yourcompany.com]
- Emergency Contact: [emergency@yourcompany.com]
- Deployment Team: [deployment-team@yourcompany.com]