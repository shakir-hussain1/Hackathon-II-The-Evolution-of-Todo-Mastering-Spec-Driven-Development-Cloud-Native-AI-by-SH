# Database Schema Consistency Skill - Specification

## Skill Overview
**Name:** database-schema-consistency
**Type:** Database Validation Skill
**Category:** Schema & Data Integrity

## Purpose
Validates that database implementation matches schema specifications by checking SQLModel models, indexes, constraints, relationships, and detecting mismatches between code and actual database.

## Input Requirements
- Schema specification documents
- SQLModel model definitions
- Database migration files
- Actual database schema (DDL)
- Relationship diagrams

## Core Functions

### 1. Model-to-Spec Validation
- Verify all specified tables exist as models
- Check field names and types
- Validate nullability constraints
- Confirm default values
- Review field lengths and constraints

### 2. Index & Constraint Verification
- Check primary key definitions
- Verify foreign key constraints
- Validate unique constraints
- Confirm check constraints
- Review index definitions for performance

### 3. Relationship Validation
- Verify one-to-many relationships
- Check many-to-many relationships
- Validate foreign key integrity
- Confirm cascade behaviors
- Review relationship naming

### 4. Code-to-Database Alignment
- Compare SQLModel to actual schema
- Detect schema drift
- Identify missing migrations
- Find orphaned tables
- Check column type mismatches

### 5. Data Integrity Checks
- Validate referential integrity
- Check constraint enforcement
- Verify default values applied
- Confirm nullable/not-null settings
- Review data type consistency

## Validation Rules

### SQLModel Standards
```python
# REQUIRED PATTERN
class Todo(SQLModel, table=True):
    __tablename__ = "todos"  # Explicit table name

    # Primary Key
    id: int | None = Field(default=None, primary_key=True)

    # Foreign Keys with relationships
    user_id: int = Field(foreign_key="users.id", index=True)

    # Required fields
    title: str = Field(max_length=200, index=True)

    # Optional fields
    description: str | None = Field(default=None, max_length=1000)

    # Enums/Constraints
    status: str = Field(
        default="pending",
        regex="^(pending|in_progress|completed)$"
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Indexes
    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
    )
```

### Index Requirements
- Primary key on all tables
- Foreign keys should be indexed
- Frequently queried fields indexed
- Composite indexes for common queries
- Avoid over-indexing (max 5 per table)

### Constraint Requirements
- Foreign keys must have ON DELETE behavior
- Unique constraints on natural keys
- Check constraints for enums/ranges
- Not null on required fields
- Default values for optional fields

### Relationship Standards
```python
# ONE-TO-MANY (User has many Todos)
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    todos: list["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="todos")

# MANY-TO-MANY (Todo and Tags)
class TodoTag(SQLModel, table=True):
    todo_id: int = Field(foreign_key="todos.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

class Todo(SQLModel, table=True):
    tags: list["Tag"] = Relationship(
        back_populates="todos",
        link_model=TodoTag
    )
```

## Validation Process

### Step 1: Spec Parsing
1. Read schema specification
2. Extract table definitions
3. Document field requirements
4. Note indexes and constraints
5. Map relationships

### Step 2: Model Analysis
1. Parse SQLModel definitions
2. Extract field definitions
3. Identify relationships
4. Document indexes
5. Check constraints

### Step 3: Schema Comparison
1. Compare spec to models
2. Check all required fields present
3. Verify types match
4. Confirm constraints match
5. Validate relationships

### Step 4: Database Inspection
1. Connect to database
2. Extract actual schema (DDL)
3. Compare models to actual tables
4. Identify drift
5. Check for orphaned tables

### Step 5: Migration Review
1. Review migration history
2. Verify migrations match models
3. Check for pending migrations
4. Validate rollback capability

## Output Format

### Schema Alignment Report
```markdown
## DATABASE SCHEMA CONSISTENCY REPORT

**Overall Status:** [ALIGNED | DRIFT DETECTED | CRITICAL MISMATCH]
**Tables in Spec:** 5
**Tables in Code:** 5
**Tables in Database:** 6
**Mismatches Found:** 4

### ✓ Aligned Models
1. **User Table**
   - Spec: ✓ Complete
   - Code: ✓ Matches spec
   - Database: ✓ Matches code
   - Indexes: ✓ All present
   - Constraints: ✓ Enforced

2. **Todo Table**
   - Spec: ✓ Complete
   - Code: ✓ Matches spec
   - Database: ✓ Matches code
   - Indexes: ✓ All present
   - Constraints: ✓ Enforced

### ⚠ Drift Detected
3. **Tag Table**
   - Spec: ✓ Defined
   - Code: ✓ Model exists
   - Database: ⚠ Missing index on 'name' field
   - **Fix:** Run migration to add index

### ✗ Critical Mismatches
4. **Category Table**
   - Spec: ✓ Requires 'description' field (nullable)
   - Code: ✗ Missing 'description' field
   - Database: ✓ Has 'description' column
   - **Fix:** Add field to SQLModel, regenerate migration

5. **Orphaned Table: 'temp_todos'**
   - Spec: ✗ Not defined
   - Code: ✗ No model
   - Database: ✓ Table exists
   - **Fix:** Drop table or create model if needed
```

### Missing or Incorrect Fields
```markdown
## FIELD MISMATCHES

### Missing Fields (In Spec, Not in Code)
1. **Todo.priority**
   - Spec: Integer, required, range 1-5
   - Code: MISSING
   - Fix: Add to SQLModel
   ```python
   priority: int = Field(ge=1, le=5, default=3)
   ```

2. **User.email_verified**
   - Spec: Boolean, default False
   - Code: MISSING
   - Fix: Add to SQLModel
   ```python
   email_verified: bool = Field(default=False)
   ```

### Extra Fields (In Code, Not in Spec)
1. **Todo.internal_id**
   - Code: UUID field
   - Spec: Not documented
   - Fix: Remove from code or add to spec

### Type Mismatches
1. **Todo.completed_at**
   - Spec: DateTime (nullable)
   - Code: String
   - Database: TIMESTAMP
   - Fix: Change code to datetime type
   ```python
   # BEFORE
   completed_at: str | None = None

   # AFTER
   completed_at: datetime | None = None
   ```

### Constraint Mismatches
1. **User.email**
   - Spec: Unique constraint required
   - Code: No unique constraint
   - Database: No unique index
   - Fix: Add unique constraint
   ```python
   email: str = Field(unique=True, index=True)
   ```
```

### Migration Recommendations
```markdown
## MIGRATION RECOMMENDATIONS

### Required Migrations
1. **Add Todo.priority field**
   ```sql
   ALTER TABLE todos ADD COLUMN priority INTEGER NOT NULL DEFAULT 3;
   ALTER TABLE todos ADD CONSTRAINT check_priority CHECK (priority >= 1 AND priority <= 5);
   ```

2. **Add User.email unique constraint**
   ```sql
   CREATE UNIQUE INDEX idx_user_email ON users(email);
   ```

3. **Fix Todo.completed_at type**
   ```sql
   ALTER TABLE todos ALTER COLUMN completed_at TYPE TIMESTAMP;
   ```

4. **Add missing index on Tag.name**
   ```sql
   CREATE INDEX idx_tag_name ON tags(name);
   ```

### Optional Migrations
1. **Drop orphaned table**
   ```sql
   DROP TABLE IF EXISTS temp_todos;
   ```

### Migration Script
```python
# Generated migration: 0004_schema_consistency_fixes.py

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add missing fields
    op.add_column('todos', sa.Column('priority', sa.Integer(), nullable=False, server_default='3'))
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false'))

    # Fix type mismatches
    op.alter_column('todos', 'completed_at', type_=sa.DateTime(), nullable=True)

    # Add constraints
    op.create_unique_constraint('uq_user_email', 'users', ['email'])
    op.create_check_constraint('ck_todo_priority', 'todos', 'priority >= 1 AND priority <= 5')

    # Add indexes
    op.create_index('idx_tag_name', 'tags', ['name'])
    op.create_index('idx_user_status', 'todos', ['user_id', 'status'])

def downgrade():
    # Reverse all changes
    op.drop_index('idx_user_status', 'todos')
    op.drop_index('idx_tag_name', 'tags')
    op.drop_constraint('ck_todo_priority', 'todos')
    op.drop_constraint('uq_user_email', 'users')
    op.alter_column('todos', 'completed_at', type_=sa.String())
    op.drop_column('users', 'email_verified')
    op.drop_column('todos', 'priority')
```
```

### Relationship Validation
```markdown
## RELATIONSHIP VALIDATION

### ✓ Correct Relationships
1. **User → Todo (One-to-Many)**
   - Foreign Key: todos.user_id → users.id
   - Cascade: ON DELETE CASCADE
   - Back-populate: ✓ Correct
   - Index: ✓ Present

### ⚠ Issues Found
2. **Todo → Tag (Many-to-Many)**
   - Link Table: todo_tags
   - Foreign Keys: ✓ Present
   - Cascade: ⚠ Missing ON DELETE CASCADE
   - **Fix:** Add cascade behavior
   ```python
   todo_id: int = Field(
       foreign_key="todos.id",
       primary_key=True,
       ondelete="CASCADE"  # Add this
   )
   ```

### ✗ Missing Relationships
3. **Category → Todo**
   - Spec: One-to-Many relationship required
   - Code: MISSING relationship definition
   - **Fix:** Add to SQLModel
   ```python
   # In Category model
   todos: list["Todo"] = Relationship(back_populates="category")

   # In Todo model
   category_id: int | None = Field(foreign_key="categories.id")
   category: Category | None = Relationship(back_populates="todos")
   ```
```

## Common Schema Issues

### Issue 1: Missing Indexes
```python
# ❌ MISSING INDEX on foreign key
class Todo(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id")  # Slow joins

# ✓ INDEXED foreign key
class Todo(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", index=True)  # Fast joins
```

### Issue 2: No Cascade Behavior
```python
# ❌ Orphaned records on user delete
user_id: int = Field(foreign_key="users.id")

# ✓ Cascade delete
user_id: int = Field(
    foreign_key="users.id",
    ondelete="CASCADE"  # Deletes todos when user deleted
)
```

### Issue 3: Type Inconsistency
```python
# ❌ INCONSISTENT types
class User(SQLModel, table=True):
    created_at: str  # String in User

class Todo(SQLModel, table=True):
    created_at: datetime  # DateTime in Todo

# ✓ CONSISTENT types
class User(SQLModel, table=True):
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Todo(SQLModel, table=True):
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Integration Points

### Works With
- backend-architect agent
- database-schema-consistency skill
- api-contract-validation skill
- spec-compliance-enforcer agent

### Validates
- SQLModel definitions
- Migration scripts
- Database schema
- Relationships and constraints

### Provides
- Schema alignment reports
- Migration recommendations
- Relationship validation
- Data integrity assessment

## Success Metrics
- **Spec Coverage:** 100% spec tables have models
- **Code-DB Alignment:** 100% models match database
- **Index Coverage:** 100% foreign keys indexed
- **Constraint Enforcement:** 100% spec constraints implemented
- **Schema Drift:** 0 mismatches
