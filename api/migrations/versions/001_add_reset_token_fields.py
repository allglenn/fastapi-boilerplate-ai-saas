"""add reset token fields

Revision ID: 001
Revises: 
Create Date: 2024-02-05

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('users', sa.Column('reset_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'reset_token_expires')
    op.drop_column('users', 'reset_token') 