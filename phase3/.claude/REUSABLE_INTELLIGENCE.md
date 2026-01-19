# Reusable Intelligence for Phase III

This document maps the reusable agents and skills available in Phase 3 to the AI-Powered Todo Chatbot feature requirements.

## Available Agents

Located in `.claude/agents/`:

### 1. backend-architect.md
**Relevance**: HIGH - Core to Phase 3 implementation

**Use Cases**:
- Validate FastAPI backend architecture
- Review REST API endpoint implementations (POST /api/{user_id}/chat)
- Ensure SQLModel schemas match specifications
- Verify middleware configuration (CORS, auth ordering)
- Validate user-level data isolation in database queries
- Check JWT authentication flow correctness

**When to Invoke**:
- After implementing chat endpoint
- After creating database models for User, Task, Conversation, Message
- After implementing MCP tool integration
- Before deploying backend

### 2. auth-security-validator.md
**Relevance**: CRITICAL - Security enforcement required

**Use Cases**:
- Validate JWT token generation and validation
- Ensure Better Auth integration is secure
- Verify user_id matching between JWT and route parameter
- Check protected route implementations
- Validate secret management (no hardcoded secrets)
- Ensure token expiration policies

**When to Invoke**:
- After implementing authentication middleware
- After adding JWT validation to chat endpoint
- Before merging any auth-related code
- During security review phase

### 3. qa-validator.md
**Relevance**: HIGH - Quality assurance

**Use Cases**:
- Test all 5 CRUD operations via natural language
- Verify conversation persistence across requests
- Validate stateless backend behavior (server restart tests)
- Test user isolation (cross-user data access prevention)
- Validate error handling and user-friendly messages

**When to Invoke**:
- After implementing each user story
- Before marking feature complete
- After bug fixes

### 4. spec-compliance-enforcer.md
**Relevance**: HIGH - Ensure spec adherence

**Use Cases**:
- Verify all behaviors match spec.md requirements
- Check that no unauthorized features were added
- Validate that all 15 functional requirements are met
- Ensure success criteria can be measured

**When to Invoke**:
- After implementation phase
- During code review
- Before deployment

### 5. workflow-orchestrator.md
**Relevance**: MEDIUM - Process enforcement

**Use Cases**:
- Ensure Spec → Plan → Tasks → Implement workflow followed
- Verify proper development workflow steps executed
- Validate no manual coding occurred

**When to Invoke**:
- Before starting implementation
- After completing each development iteration

### 6. dx-docs-improver.md
**Relevance**: MEDIUM - Documentation quality

**Use Cases**:
- Review and improve README documentation
- Ensure setup instructions are clear
- Validate API documentation completeness
- Improve developer onboarding materials

**When to Invoke**:
- After feature completion
- Before hackathon submission
- When preparing for external review

### 7. frontend-ui-dashboard.md
**Relevance**: MEDIUM - UI implementation (if custom UI needed)

**Use Cases**:
- Review OpenAI ChatKit integration
- Ensure chat UI follows modern SaaS patterns
- Validate responsive design
- Implement loading and error states

**When to Invoke**:
- After implementing chat frontend
- If custom UI components needed
- For UI/UX improvements

## Available Skills

Located in `.claude/skill/`:

### 1. jwt-verification-security/
**Relevance**: CRITICAL

**Use Cases**:
- Validate JWT token structure and signing
- Verify token expiration handling
- Check secret management practices
- Ensure token validation on every request

### 2. user-ownership-enforcement/
**Relevance**: CRITICAL

**Use Cases**:
- Verify all database queries filter by user_id
- Ensure no cross-user data access possible
- Validate user isolation in MCP tools
- Check authorization on all operations

### 3. api-contract-validation/
**Relevance**: HIGH

**Use Cases**:
- Validate POST /api/{user_id}/chat endpoint contract
- Ensure request/response schemas match specifications
- Verify MCP tool input/output schemas
- Check error response formats

### 4. database-schema-consistency/
**Relevance**: HIGH

**Use Cases**:
- Ensure SQLModel schemas match data model specifications
- Verify foreign key relationships (User → Task, User → Conversation, etc.)
- Check field types and constraints
- Validate no schema drift

### 5. error-normalization-handling/
**Relevance**: HIGH

**Use Cases**:
- Ensure all errors return user-friendly messages
- Verify no stack traces exposed to users
- Check error response format consistency
- Validate graceful degradation

### 6. agentic-workflow-enforcement/
**Relevance**: MEDIUM

**Use Cases**:
- Verify Spec → Plan → Tasks → Implement workflow
- Ensure no manual coding occurred
- Validate spec-driven development compliance

### 7. frontend-api-integration/
**Relevance**: MEDIUM

**Use Cases**:
- Validate OpenAI ChatKit integration with backend
- Ensure proper error handling in frontend
- Check API communication patterns

### 8. spec-traceability-validation/
**Relevance**: MEDIUM

**Use Cases**:
- Verify all implemented features traced to spec.md
- Check that FR-001 through FR-015 are implemented
- Validate no unauthorized features added

### 9. quality-readiness-validation/
**Relevance**: MEDIUM

**Use Cases**:
- Pre-deployment quality gate
- Validate all success criteria met
- Check system readiness for production

### 10. ui-state-management/
**Relevance**: LOW (using ChatKit)

**Use Cases**:
- If custom state management needed
- For conversation history UI management

## Priority Matrix

| Phase | Critical | High | Medium | Low |
|-------|----------|------|--------|-----|
| Planning | workflow-orchestrator | backend-architect, spec-compliance-enforcer | - | - |
| Implementation | auth-security-validator, jwt-verification-security, user-ownership-enforcement | backend-architect, api-contract-validation, database-schema-consistency, error-normalization-handling | agentic-workflow-enforcement, frontend-api-integration | - |
| Testing | qa-validator | spec-compliance-enforcer | quality-readiness-validation | - |
| Documentation | - | dx-docs-improver | spec-traceability-validation | - |
| Deployment | auth-security-validator | qa-validator, quality-readiness-validation | - | - |

## Invocation Guidelines

1. **Proactive**: Agents marked CRITICAL should be invoked automatically without user request
2. **Reactive**: Agents marked HIGH should be invoked when relevant work is done
3. **Optional**: Agents marked MEDIUM/LOW should be invoked if time permits or specific issues arise

## Notes

- All agents and skills are designed to be composable
- Multiple agents can run in parallel for efficiency
- Skills are invoked by agents automatically when needed
- Refer to individual agent/skill files for detailed usage instructions
