# Prompt History Record: agentic-workflow-enforcement Skill

## Creation Date
2026-01-11

## Skill Type
Process Enforcement Skill

## Purpose
Ensures correct execution order of the Agentic Development Stack (Spec → Plan → Tasks → Implementation) to prevent technical debt through workflow discipline.

## Key Functions
1. Workflow state detection and tracking
2. Prerequisite validation at each gate
3. Process violation detection
4. Corrective action guidance
5. Compliance scoring

## Usage Patterns
- Before starting any implementation
- When users bypass workflow steps
- During retroactive audits
- For process compliance reporting
- Team workflow training

## Workflow Gates
- Gate 1: Spec → Plan (spec complete)
- Gate 2: Plan → Tasks (plan approved)
- Gate 3: Tasks → Implementation (tasks defined)
- Gate 4: Implementation → Validation (tests pass)

## Success Metrics
- **Target Compliance:** 100% workflow adherence
- **Max Critical Violations:** 0
- **Retroactive Documentation:** <10%
- **Gate Bypass Rate:** 0%

## Common Violations
- Implementation without specs
- Skipped planning phase
- Missing task breakdown
- Merged workflow steps

## Integration Points
- Gates workflow-orchestrator execution
- Feeds spec-compliance-enforcer
- Blocks implementation agents
- Validates quality-readiness

## Evolution Notes
- Added comprehensive gate validation
- Enhanced violation detection
- Improved recovery patterns
- Integrated compliance scoring
