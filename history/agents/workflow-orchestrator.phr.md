# Prompt History Record: workflow-orchestrator Agent

## Creation Date
2026-01-11

## Agent Type
Process Enforcement Agent

## Purpose
Created to ensure proper development workflow (Spec → Plan → Tasks → Implementation) is followed, preventing technical debt and maintaining code quality through process discipline.

## Creation Context
Developed for the Hackathon II project to enforce the Agentic Development Stack methodology and prevent common workflow violations like implementing code before planning or skipping specification steps.

## Key Capabilities
1. Workflow step validation (spec → plan → tasks → implementation)
2. Pre-implementation prerequisite checks
3. Process violation detection
4. Retroactive compliance auditing
5. Workflow guidance and recovery
6. Phase gate enforcement

## Usage Patterns

### Primary Use Cases
- Before any code implementation
- When users request direct coding
- After development iterations
- During PR reviews
- For new feature kickoff
- Retroactive process validation

### Trigger Conditions
- User requests feature implementation
- Code changes detected
- New project phases start
- Process compliance audits
- Team onboarding
- Quality gate reviews

## Integration with Project
- Gates spec-compliance-enforcer execution
- Feeds agentic-workflow-enforcement skill
- Blocks implementation agents until ready
- Validates before quality-readiness-validation
- Coordinates all development phases

## Workflow Enforcement

### The Agentic Dev Stack
```
1. SPECIFICATION → Define what to build
2. PLANNING → Design how to build it
3. TASK BREAKDOWN → Break into actionable items
4. IMPLEMENTATION → Write the code
5. VALIDATION → Verify against specs
```

### Phase Gates

**Gate 1: Spec → Plan**
- Specification complete and unambiguous
- Requirements clearly defined
- Acceptance criteria documented
- → THEN allow planning

**Gate 2: Plan → Tasks**
- Implementation plan exists
- Architecture decisions made
- Technical approach defined
- → THEN allow task breakdown

**Gate 3: Tasks → Implementation**
- Tasks broken down
- Dependencies identified
- Priorities assigned
- → THEN allow coding

**Gate 4: Implementation → Validation**
- All tasks completed
- Code follows plan
- Tests passing
- → THEN allow review

## Evolution Notes
- Started with basic workflow checking
- Added comprehensive gate validation
- Enhanced retroactive auditing
- Integrated recovery patterns
- Improved guidance mechanisms

## Best Practices
- Enforce BEFORE implementation starts
- Use for all feature requests
- Audit retroactively if needed
- Guide users through recovery
- Document all violations

## Common Violations Detected

### Critical (Block Work)
- Implementation without specs
- Coding without task breakdown
- Skipped planning phase
- Direct coding on request

### High (Immediate Fix)
- Incomplete specifications
- Shallow planning documents
- Unprioritized tasks
- Missing approvals

### Medium (Address Soon)
- Sparse acceptance criteria
- Unclear dependencies
- Missing documentation
- Template deviations

### Low (Monitor)
- Formatting inconsistencies
- Minor doc gaps
- Process variations

## Workflow Recovery Patterns

### No Specs Exist
1. Pause development
2. Create retroactive specification
3. Validate code matches spec
4. Create missing plan/tasks
5. Resume with compliance

### Specs Exist, No Plan
1. Pause new features
2. Document existing architecture
3. Create plan for future work
4. Break down remaining tasks
5. Resume workflow

### Merged Steps
1. Acceptable if both complete
2. Separate if clarity suffers
3. Ensure coverage
4. Proceed with caution

## Decision Tree
```
User requests feature
    ↓
Spec exists? NO → BLOCK: Create spec first
    ↓ YES
Plan exists? NO → BLOCK: Create plan first
    ↓ YES
Tasks exist? NO → BLOCK: Break down tasks
    ↓ YES
ALLOW implementation
```

## Compliance Metrics
- **Workflow Adherence:** 100% target
- **Gate Bypasses:** 0% allowed
- **Critical Violations:** 0 tolerated
- **Retroactive Docs:** <10% goal

## Reporting Format
- Current phase identification
- Gate passage status
- Violation severity levels
- Required corrective actions
- Recovery guidance
- Compliance score

## Success Metrics
- 100% features have specs before coding
- Zero direct implementations
- All phases in correct order
- Reduced technical debt
- Improved code quality

## Maintenance
- Update gate requirements
- Refine violation detection
- Keep workflow current
- Review recovery patterns
- Update guidance templates
