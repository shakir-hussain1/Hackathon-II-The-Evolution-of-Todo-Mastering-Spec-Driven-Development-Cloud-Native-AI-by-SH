# Agentic Workflow Enforcement Skill - Specification

## Skill Overview
**Name:** agentic-workflow-enforcement
**Type:** Process Enforcement Skill
**Category:** Workflow & Governance

## Purpose
Ensures correct execution order of the Agentic Development Stack (Spec → Plan → Tasks → Implementation) to maintain development discipline and prevent technical debt.

## Input Requirements
- Project file structure
- Specification documents
- Plan files
- Task breakdowns
- Implementation code

## Core Functions

### 1. Workflow State Detection
- Identify current development phase
- Detect which workflow steps are complete
- Track phase transitions
- Monitor workflow compliance

### 2. Prerequisite Validation
- Confirm specs exist before allowing planning
- Ensure plans exist before task breakdown
- Verify tasks exist before implementation
- Validate approvals at each gate

### 3. Violation Detection
- Flag skipped workflow steps
- Detect merged phases
- Identify out-of-order execution
- Catch direct implementation without planning

### 4. Corrective Action Guidance
- Provide remediation steps
- Guide retroactive documentation
- Suggest workflow recovery paths
- Recommend process improvements

## Workflow Enforcement Rules

### The Agentic Dev Stack
```
1. SPECIFICATION → Define what to build
2. PLANNING → Design how to build it
3. TASK BREAKDOWN → Break down into actionable items
4. IMPLEMENTATION → Write the code
5. VALIDATION → Verify against specs
```

### Gate Requirements

**Gate 1: Spec → Plan**
- ✓ Specification exists and is complete
- ✓ Requirements are unambiguous
- ✓ Acceptance criteria defined
- → THEN allow planning

**Gate 2: Plan → Tasks**
- ✓ Implementation plan exists
- ✓ Architecture decisions documented
- ✓ Technical approach defined
- → THEN allow task breakdown

**Gate 3: Tasks → Implementation**
- ✓ Tasks are broken down
- ✓ Dependencies identified
- ✓ Priorities assigned
- → THEN allow coding

**Gate 4: Implementation → Validation**
- ✓ All tasks completed
- ✓ Code follows plan
- ✓ Tests passing
- → THEN allow review

## Validation Process

### Step 1: Phase Detection
1. Scan project for spec files
2. Look for plan documents
3. Check for task lists
4. Analyze code presence
5. Determine current phase

### Step 2: Workflow Audit
1. For each phase, verify completion
2. Check for prerequisite satisfaction
3. Identify any skipped steps
4. Flag workflow violations

### Step 3: Compliance Assessment
1. Calculate workflow adherence score
2. Identify critical violations
3. Determine if work should proceed
4. Generate compliance report

### Step 4: Remediation Planning
1. List required corrective actions
2. Prioritize by workflow impact
3. Provide templates/examples
4. Guide through recovery process

## Output Format

### Workflow Compliance Report
```markdown
## WORKFLOW COMPLIANCE REPORT

**Overall Status:** [COMPLIANT | PARTIAL COMPLIANCE | NON-COMPLIANT]
**Current Phase:** [Specification | Planning | Tasks | Implementation | Validation]
**Workflow Adherence Score:** [0-100%]

### Phase Completion Matrix
| Phase          | Status      | Gate Passed | Issues |
|----------------|-------------|-------------|--------|
| Specification  | ✓ Complete  | ✓ Yes       | None   |
| Planning       | ⚠ Partial   | ✗ No        | Missing architecture decisions |
| Task Breakdown | ✗ Missing   | ✗ No        | Not started |
| Implementation | ⚠ Started   | ✗ No        | VIOLATION: Coding before tasks |

### Violations Detected
**CRITICAL:**
- Implementation started without task breakdown (blocking violation)
- No architectural plan exists (must create before continuing)

**WARNING:**
- Specification incomplete (missing edge cases)
- Planning document exists but lacks detail

### Required Actions (Prioritized)
1. **STOP IMPLEMENTATION** - Do not write more code
2. **CREATE PLAN** - Document architecture and technical approach
3. **BREAK DOWN TASKS** - Define specific implementation tasks
4. **COMPLETE SPECS** - Add missing edge case documentation
5. **RESUME IMPLEMENTATION** - Proceed with coding after gates pass

### Corrective Actions
- [ ] Create `docs/plan.md` with architecture decisions
- [ ] Create `docs/tasks.md` with task breakdown
- [ ] Update `docs/spec.md` with edge cases
- [ ] Review and approve plan before coding
```

### Workflow Compliance Score
```
Formula: (Completed Gates / Total Required Gates) × 100
- Gate 1 Passed: 100% (Spec exists)
- Gate 2 Passed: 0% (No plan)
- Gate 3 Passed: 0% (No tasks)
- Gate 4 Passed: N/A (Not ready)

Overall: 33% - NON-COMPLIANT
```

## Violation Severity Levels

### CRITICAL (Block all work)
- Implementation without specifications
- Coding without task breakdown
- Skipped planning phase entirely

### HIGH (Require immediate remediation)
- Incomplete specifications
- Plan lacks technical depth
- Tasks not prioritized

### MEDIUM (Address before next phase)
- Missing approval documentation
- Sparse acceptance criteria
- Unclear dependencies

### LOW (Document and monitor)
- Template deviations
- Formatting inconsistencies
- Minor documentation gaps

## Use Cases

### When to Use
1. **Before starting implementation** - Verify all prerequisites
2. **When user requests direct coding** - Enforce workflow
3. **During code reviews** - Validate process was followed
4. **After development iteration** - Audit compliance
5. **For new team members** - Teach proper workflow

### Integration with Agents
- Gates workflow-orchestrator agent execution
- Feeds compliance data to spec-compliance-enforcer
- Blocks backend-architect and frontend-ui-dashboard until ready
- Validates before quality-readiness-validation runs

## Workflow Recovery Patterns

### Pattern 1: No Specs Exist
```
DETECTED: Code exists, no specs
ACTION:
1. Pause all development
2. Create retroactive specification
3. Validate code matches spec
4. Create missing plan and tasks
5. Resume with compliance
```

### Pattern 2: Specs Exist, No Plan
```
DETECTED: Specs and code exist, no plan
ACTION:
1. Pause new features
2. Document existing architecture (retroactive)
3. Create plan for future work
4. Break down remaining tasks
5. Resume with workflow
```

### Pattern 3: Merged Steps
```
DETECTED: Plan and tasks in same document
ACTION:
1. Acceptable if both are complete
2. Separate if clarity suffers
3. Ensure both aspects are covered
4. Proceed with caution
```

## Success Metrics
- **Target Compliance:** 100% workflow adherence
- **Max Critical Violations:** 0
- **Retroactive Documentation:** Minimize to <10%
- **Gate Bypass Rate:** 0%
