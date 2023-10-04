"""jail_features

Revision ID: 9a0027d5871d
Revises: 4a382a75cc3f
Create Date: 2023-10-04 06:46:07.536067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a0027d5871d'
down_revision = '4a382a75cc3f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('user', sa.Column('failed_login_attempts', sa.INTEGER(default=0)))
    op.add_column('user', sa.Column('is_suspended', sa.BOOLEAN(default=False)))
    op.add_column('user', sa.Column('suspended_at', sa.DateTime()))


def downgrade() -> None:
    op.drop_column('user', 'failed_login_attempts')
    op.drop_column('user', 'is_suspended')
    op.drop_column('user', 'suspended_at')