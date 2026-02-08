"""create tasks table

Revision ID: 002
Revises: 001
Create Date: 2026-02-08 10:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('priority', sa.String(10), nullable=False, server_default='medium'),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.Text), nullable=False, server_default=sa.text("'{}'::text[]")),
        sa.Column('recurrence_pattern', postgresql.JSONB(), nullable=True),
        sa.Column('next_occurrence', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        schema='chat_api'
    )

    # Create foreign key constraint
    op.create_foreign_key(
        'fk_tasks_user_id',
        'tasks',
        'users',
        ['user_id'],
        ['id'],
        source_schema='chat_api',
        referent_schema='chat_api',
        ondelete='CASCADE'
    )

    # Create check constraints
    op.create_check_constraint(
        'check_status',
        'tasks',
        "status IN ('pending', 'completed', 'archived')",
        schema='chat_api'
    )

    op.create_check_constraint(
        'check_priority',
        'tasks',
        "priority IN ('high', 'medium', 'low')",
        schema='chat_api'
    )

    # Create indexes
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'], unique=False, schema='chat_api')
    op.create_index('idx_tasks_status', 'tasks', ['status'], unique=False, schema='chat_api')
    op.create_index(
        'idx_tasks_due_date',
        'tasks',
        ['due_date'],
        unique=False,
        schema='chat_api',
        postgresql_where=sa.text('due_date IS NOT NULL')
    )
    op.create_index(
        'idx_tasks_next_occurrence',
        'tasks',
        ['next_occurrence'],
        unique=False,
        schema='chat_api',
        postgresql_where=sa.text('next_occurrence IS NOT NULL')
    )
    op.create_index('idx_tasks_user_status', 'tasks', ['user_id', 'status'], unique=False, schema='chat_api')

    # Create GIN index for tags array
    op.execute(
        "CREATE INDEX idx_tasks_tags ON chat_api.tasks USING GIN(tags)"
    )

    # Create full-text search GIN index
    op.execute(
        "CREATE INDEX idx_tasks_full_text ON chat_api.tasks USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '')))"
    )


def downgrade() -> None:
    # Drop indexes
    op.execute("DROP INDEX IF EXISTS chat_api.idx_tasks_full_text")
    op.execute("DROP INDEX IF EXISTS chat_api.idx_tasks_tags")
    op.drop_index('idx_tasks_user_status', table_name='tasks', schema='chat_api')
    op.drop_index('idx_tasks_next_occurrence', table_name='tasks', schema='chat_api')
    op.drop_index('idx_tasks_due_date', table_name='tasks', schema='chat_api')
    op.drop_index('idx_tasks_status', table_name='tasks', schema='chat_api')
    op.drop_index('idx_tasks_user_id', table_name='tasks', schema='chat_api')

    # Drop constraints
    op.drop_constraint('check_priority', 'tasks', schema='chat_api', type_='check')
    op.drop_constraint('check_status', 'tasks', schema='chat_api', type_='check')
    op.drop_constraint('fk_tasks_user_id', 'tasks', schema='chat_api', type_='foreignkey')

    # Drop table
    op.drop_table('tasks', schema='chat_api')
