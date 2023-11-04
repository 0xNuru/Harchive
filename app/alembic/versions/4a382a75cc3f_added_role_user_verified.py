"""added_role_user_verified

Revision ID: 4a382a75cc3f
Revises: 
Create Date: 2023-10-03 02:08:16.995833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a382a75cc3f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ...
    op.add_column('user', sa.Column('role', sa.String(length=50)))
    op.add_column('user', sa.Column('is_verified', sa.Boolean()))
    op.add_column('patient', sa.Column('nin', sa.String(length=11)))
    # ...

def downgrade():
    # ...
    op.add_column('user', sa.Column('failed_login_attempts', sa.INTEGER()))
    op.add_column('user', sa.Column('is_suspended', sa.BOOLEAN()))
    op.add_column('user', sa.Column('suspended_at', sa.DateTime()))

    # ...
