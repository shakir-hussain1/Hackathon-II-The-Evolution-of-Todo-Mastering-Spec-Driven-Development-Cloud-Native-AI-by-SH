# Prompt History Record: database-schema-consistency Skill

## Creation Date
2026-01-11

## Skill Type
Database Validation Skill

## Purpose
Validates database implementation matches schema specs by checking SQLModel models, indexes, constraints, relationships, and code-to-database alignment.

## Key Functions
1. Model-to-spec validation
2. Index and constraint verification
3. Relationship validation
4. Code-to-database alignment
5. Data integrity checks

## SQLModel Standards
- Explicit table names
- Primary keys on all tables
- Foreign keys indexed
- Proper relationship definitions
- Cascade behaviors defined
- Constraints enforced

## Common Issues Detected
- Missing database indexes
- No cascade behavior on FKs
- Type inconsistencies
- Missing constraints
- Orphaned tables
- Schema drift

## Usage Patterns
- After model changes
- During migration creation
- Before database updates
- Schema compliance audits
- Code review validation

## Integration Points
- Works with backend-architect
- Validates database migrations
- Supports api-contract-validation
- Feeds quality-readiness-validation

## Success Metrics
- **Spec Coverage:** 100% spec tables have models
- **Code-DB Alignment:** 100% match
- **Index Coverage:** 100% FKs indexed
- **Constraint Enforcement:** 100% implemented
- **Schema Drift:** 0
