# Prompt History Record: backend-architect Agent

## Creation Date
2026-01-11

## Agent Type
Backend Development Specialist

## Purpose
Created to validate and ensure correct implementation of FastAPI backend architecture, focusing on API design, authentication, database schemas, and security best practices.

## Creation Context
Developed for the Hackathon II project to maintain backend quality standards and ensure proper implementation of REST APIs, authentication flows, and data models using FastAPI and SQLModel.

## Key Capabilities
1. REST API architecture validation
2. JWT authentication and authorization review
3. SQLModel schema design verification
4. Middleware configuration assessment
5. Security vulnerability detection
6. Database relationship validation

## Usage Patterns

### Primary Use Cases
- After implementing API endpoints
- When adding authentication logic
- After creating/updating database schemas
- During middleware configuration
- Before merging backend changes
- For security audits

### Trigger Conditions
- New/modified API route handlers
- Authentication flow implementations
- Database model changes
- Middleware stack updates
- Protected endpoint additions

## Integration with Project
- Validates against api-contract-validation skill
- Works with auth-security-validator agent
- Coordinates with database-schema-consistency skill
- Supports user-ownership-enforcement skill
- Feeds quality-readiness-validation

## Technical Focus Areas

### API Design
- RESTful conventions
- Status code correctness
- Request/response models
- Error handling patterns
- Endpoint documentation

### Security
- Password hashing (bcrypt/argon2)
- JWT implementation
- Input validation
- SQL injection prevention
- Rate limiting

### Database
- SQLModel best practices
- Relationship definitions
- Index optimization
- Migration strategies
- Constraint enforcement

## Evolution Notes
- Started with basic API validation
- Added comprehensive security checks
- Enhanced database schema review
- Integrated middleware validation
- Improved error handling standards

## Best Practices
- Run after any backend code changes
- Validate before code review
- Check security implications
- Verify database relationships
- Ensure proper error handling

## Common Issues Detected
- Missing authentication on protected routes
- Incorrect HTTP status codes
- Weak password hashing
- Missing database indexes
- Improper error responses
- CORS misconfigurations

## Code Quality Standards
- Type hints on all functions
- Comprehensive docstrings
- Proper exception handling
- Security-first approach
- Dependency injection patterns

## Success Metrics
- Zero security vulnerabilities
- 100% API endpoint compliance
- Proper authentication on all protected routes
- User data properly isolated
- Comprehensive error handling

## Maintenance
- Update security best practices
- Refine validation checklists
- Keep FastAPI patterns current
- Review new vulnerabilities
- Update schema standards
