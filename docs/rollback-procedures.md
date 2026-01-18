# Rollback Procedures: Todo Full-Stack Application

## Overview
This document outlines the procedures to rollback the Todo Full-Stack Application to a previous working state in case of deployment failures or critical issues discovered after deployment.

## When to Initiate Rollback

Rollback should be initiated immediately if any of the following conditions occur:
- Complete application failure (cannot access frontend or API)
- Critical security vulnerabilities discovered
- Data corruption or loss reported
- Authentication system completely fails
- Major performance degradation affecting all users
- High error rates (>50%) for core functionality

## Rollback Readiness

### Prerequisites
- Previous stable version available in container registry
- Automated rollback script prepared and tested
- Database migration scripts for rollback (if needed)
- Monitoring system in place to verify rollback success

### Rollback Timeline
- Minor issues: Evaluate before rollback (may not be needed)
- Critical issues: Begin rollback within 5 minutes
- System-wide outages: Begin rollback immediately
- Complete service failure: Automatic rollback trigger (if configured)

## Manual Rollback Process

### 1. Frontend Rollback
1. Identify the last stable frontend version tag
2. Update the deployment to use the stable version:
   ```bash
   kubectl set image deployment/todo-frontend frontend=todo-frontend:stable-version
   ```
3. Verify the rollout:
   ```bash
   kubectl rollout status deployment/todo-frontend
   ```
4. Check frontend availability:
   ```bash
   curl -I http://your-frontend-domain.com
   ```

### 2. Backend Rollback
1. Identify the last stable backend version tag
2. Update the deployment to use the stable version:
   ```bash
   kubectl set image deployment/todo-backend backend=todo-backend:stable-version
   ```
3. Verify the rollout:
   ```bash
   kubectl rollout status deployment/todo-backend
   ```
4. Test API functionality:
   ```bash
   curl -I http://your-api-domain.com/health
   ```

### 3. Database Rollback (if applicable)
> **Note**: Database rollbacks should only be performed if structural changes were introduced and should be coordinated with database administrator.

1. Ensure you have a recent database backup
2. Run database rollback migrations if applicable:
   ```bash
   # Example for alembic-based migrations
   alembic downgrade -1  # Roll back to previous revision
   ```
3. Verify database integrity after rollback

## Kubernetes Rollback Commands

### Using Kubernetes Rollback
```bash
# Rollback frontend deployment to previous version
kubectl rollout undo deployment/todo-frontend

# Rollback backend deployment to previous version
kubectl rollout undo deployment/todo-backend

# Verify rollback status
kubectl rollout status deployment/todo-frontend
kubectl rollout status deployment/todo-backend
```

### Rolling Back to Specific Revision
```bash
# View rollout history
kubectl rollout history deployment/todo-frontend
kubectl rollout history deployment/todo-backend

# Rollback to specific revision (e.g., revision 3)
kubectl rollout undo deployment/todo-frontend --to-revision=3
kubectl rollout undo deployment/todo-backend --to-revision=3
```

## Docker Compose Rollback

### Using Docker Compose Tags
```bash
# Stop current services
docker-compose -f docker-compose.prod.yml down

# Deploy previous version
docker-compose -f docker-compose.prev.yml up -d
```

### Using Git to Revert Configuration
```bash
# Check current deployment state
git status

# Revert to previous stable commit
git checkout <previous-stable-commit-hash>

# Redeploy with previous configuration
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

## Rollback Verification

### 1. Health Checks
After rollback completion, verify:

**Frontend:**
```bash
curl -s -o /dev/null -w "%{http_code}" https://your-domain.com
# Should return 200
```

**Backend:**
```bash
curl -s -o /dev/null -w "%{http_code}" https://api.your-domain.com/health
# Should return 200 with healthy status
```

### 2. Core Functionality Tests
Perform these manual tests:
- User login with existing credentials
- Create a new task
- Update an existing task
- Toggle task completion status
- View task list
- Logout and verify session clearance

### 3. Monitor System Metrics
- Verify error rates return to normal levels (<1%)
- Check API response times (<1000ms)
- Monitor CPU and memory usage
- Verify database connection pool utilization

## Rollback Failure Procedures

If the rollback itself fails:

### 1. Immediate Actions
1. Stop any ongoing deployment/rollback processes
2. Notify the deployment team and stakeholders
3. Document current system state
4. Assess available recovery options

### 2. Recovery Options
**Option A: Emergency hotfix**
- Deploy minimal fixes to current version
- Focus only on restoring core functionality

**Option B: Restore from backup**
- Use recent database backup
- Deploy known good application version
- Manually update configuration if needed

**Option C: Static maintenance page**
- Serve maintenance page from CDN/load balancer
- Preserve database to prevent data loss
- Work on fixes in parallel

## Communication Plan

### Stakeholders to Notify
- Development team lead
- Operations team
- Product manager
- Customer support team
- Key customers (if applicable)

### Communication Template
```
Subject: Emergency Rollback Initiated - Todo Application

Summary:
We have initiated an emergency rollback of the Todo application due to [reason].
The rollback began at [timestamp] and is expected to complete by [estimated time].

Current Status:
- [Status of frontend rollback]
- [Status of backend rollback]
- [Status of database if applicable]

Impact:
- [Expected user impact]

Next Steps:
- [Planned verification steps]
- [Timeline for completion]
- [Next update timeline]
```

## Prevention for Future Deployments

### 1. Implement Blue-Green Deployments
- Maintain two identical production environments
- Deploy to inactive environment first
- Switch traffic after verification
- Reduce rollback time to seconds

### 2. Add Comprehensive Health Checks
- Add application-specific health endpoints
- Verify database connectivity
- Test authentication functionality
- Check external service dependencies

### 3. Improve Testing
- Add integration tests before deployment
- Test deployment in staging environment
- Validate environment-specific configurations
- Test rollback procedures in staging

### 4. Canary Releases
- Deploy to subset of users first
- Monitor metrics during phased rollout
- Gradually increase deployment percentage
- Faster rollback with minimal impact

## Rollback Checklist

Before initiating rollback, verify:
- [ ] Backup of current state is available
- [ ] Previous stable version is accessible
- [ ] Rollback script tested in staging
- [ ] Database migration rollback scripts ready (if needed)
- [ ] Communication template prepared
- [ ] Rollback team is available
- [ ] Monitoring system is functional
- [ ] Rollback success criteria defined

During rollback:
- [ ] Monitor system metrics continuously
- [ ] Test core functionality at intervals
- [ ] Update stakeholders on progress
- [ ] Document any unexpected issues
- [ ] Maintain rollback team availability

After rollback:
- [ ] Verify all services are functional
- [ ] Confirm error rates are normal
- [ ] Perform smoke tests for all features
- [ ] Notify stakeholders of completion
- [ ] Document lessons learned
- [ ] Schedule post-mortem for root cause analysis

## Contact Information
- Deployment Team: [deployment-team@yourcompany.com]
- On-Call Engineer: [oncall@yourcompany.com]
- Emergency Support: [emergency@yourcompany.com]
- Database Admin: [dba@yourcompany.com]