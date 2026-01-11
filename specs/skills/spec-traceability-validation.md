# Spec Traceability Validation Skill - Specification

## Skill Overview
**Name:** spec-traceability-validation
**Type:** Quality Assurance Skill
**Category:** Validation & Compliance

## Purpose
Validates traceability between specifications, plans, tasks, and implementation to ensure every feature is properly documented and every spec item is implemented.

## Input Requirements
- Specification files (markdown, requirements docs)
- Implementation files (source code)
- Plan documents
- Task lists

## Core Functions

### 1. Spec-to-Code Traceability
- Map each specification requirement to implementation
- Identify implemented features and their spec sources
- Create bidirectional traceability matrix
- Track requirement coverage percentage

### 2. Implementation Coverage Analysis
- Scan all implemented features
- Verify each has specification backing
- Flag unspecified implementations (gold-plating)
- Identify scope creep

### 3. Specification Coverage Analysis
- Review all spec requirements
- Verify each is implemented
- Identify unimplemented spec items
- Flag missing features

### 4. Phase Boundary Enforcement
- Validate current phase scope
- Detect future-phase features in implementation
- Ensure phase isolation
- Prevent premature feature implementation

## Validation Process

### Step 1: Specification Discovery
1. Locate all spec files in project
2. Parse requirements and user stories
3. Extract acceptance criteria
4. Build requirements database

### Step 2: Implementation Analysis
1. Scan source code for features
2. Identify API endpoints
3. List database models
4. Map UI components

### Step 3: Traceability Mapping
1. For each spec item, find implementation
2. For each implementation, find spec
3. Create cross-reference matrix
4. Calculate coverage metrics

### Step 4: Gap Analysis
1. Identify spec items without implementation
2. Identify implementation without specs
3. Flag phase boundary violations
4. Generate remediation recommendations

## Output Format

### Traceability Matrix
```markdown
## TRACEABILITY MATRIX

### Spec → Code Mapping
| Requirement ID | Spec File | Implementation | Status | Notes |
|---------------|-----------|----------------|--------|-------|
| REQ-001       | spec.md   | auth.py:45     | ✓      | Complete |
| REQ-002       | spec.md   | -              | ✗      | Missing |

### Code → Spec Mapping
| Feature | File:Line | Spec Reference | Status | Action |
|---------|-----------|----------------|--------|---------|
| Login   | auth.py:45 | spec.md:REQ-001 | ✓     | OK |
| Export  | tasks.py:120 | NONE         | ✗     | Add spec or remove |
```

### Coverage Report
```markdown
## COVERAGE ANALYSIS

**Specification Coverage:** 85% (17/20 requirements implemented)
**Implementation Coverage:** 92% (23/25 features specified)

### Missing Implementations (Spec items not coded)
- REQ-002: User profile editing
- REQ-015: Export to CSV
- REQ-018: Email notifications

### Unspecified Implementations (Code without specs)
- Feature: Dark mode toggle (tasks.py:156)
- Feature: Task sorting by priority (api.py:89)

### Phase Boundary Violations
- REQ-023: Advanced analytics (Phase III feature in Phase II code)
```

### Compliance Verdict
```markdown
## COMPLIANCE VERDICT: [PASS | FAIL]

**Status:** [Summary of traceability health]

**Critical Issues:**
- [List blocking issues]

**Recommendations:**
1. [Prioritized actions to achieve compliance]
2. [Specification updates needed]
3. [Code changes required]
```

## Validation Rules

### Traceability Requirements
- Every feature MUST have a spec reference
- Every spec item SHOULD be implemented (or deferred)
- Phase boundaries MUST be respected
- Gold-plating MUST be removed or specified

### Acceptable Exceptions
- Infrastructure code (build scripts, configs)
- Internal utilities (if documented separately)
- Technical debt (if tracked in backlog)

## Use Cases

### When to Use
1. Before major releases
2. During compliance audits
3. After completing a development phase
4. When onboarding new team members
5. For handoff documentation

### Integration with Agents
- Works with spec-compliance-enforcer agent
- Feeds quality-readiness-validation skill
- Supports workflow-orchestrator agent
- Validates backend-architect and frontend-ui-dashboard work

## Success Metrics
- **Target Spec Coverage:** ≥95%
- **Target Implementation Coverage:** ≥98%
- **Max Unspecified Features:** ≤2
- **Phase Boundary Violations:** 0
