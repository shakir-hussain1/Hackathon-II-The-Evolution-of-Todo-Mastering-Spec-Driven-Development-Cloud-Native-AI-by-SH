"""create users table

Revision ID: 001
Revises:
Create Date: 2026-02-08 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create chat_api schema if it doesn't exist
    op.execute('CREATE SCHEMA IF NOT EXISTS chat_api')

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('notification_preferences', postgresql.JSONB(), nullable=False, server_default=sa.text("'{\"email\": true, \"push\": false}'::jsonb")),
        sa.Column('timezone', sa.String(50), nullable=False, server_default='UTC'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        schema='chat_api'
    )

    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'], unique=False, schema='chat_api')
    op.create_index(
        'idx_users_deleted_at',
        'users',
        ['deleted_at'],
        unique=False,
        schema='chat_api',
        postgresql_where=sa.text('deleted_at IS NULL')
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_users_deleted_at', table_name='users', schema='chat_api')
    op.drop_index('idx_users_email', table_name='users', schema='chat_api')

    # Drop table
    op.drop_table('users', schema='chat_api')

    # Note: Schema is not dropped to avoid issues with other tables
