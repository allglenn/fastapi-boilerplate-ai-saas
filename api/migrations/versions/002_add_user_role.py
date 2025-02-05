"""add user role

Revision ID: 002
Revises: 001
Create Date: 2024-02-05

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum
import enum

# Define the UserRole Enum
class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"

# revision identifiers, used by Alembic.
revision = '002_add_user_role'
down_revision = '001'  # Replace with your actual previous revision ID
branch_labels = None
depends_on = None

def upgrade():
    # Add the role column to the users table
    op.add_column('users', sa.Column('role', sa.Enum(UserRole), nullable=False, server_default=UserRole.CLIENT.name))

def downgrade():
    # Remove the role column from the users table
    op.drop_column('users', 'role')