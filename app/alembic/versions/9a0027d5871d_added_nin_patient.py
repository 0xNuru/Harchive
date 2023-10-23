"""added_nin_patient

Revision ID: 9a0027d5871d
Revises: 4a382a75cc3f
Create Date: 2023-10-04 06:46:07.536067

"""
from alembic import op
import enum
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a0027d5871d'
down_revision = '4a382a75cc3f'
branch_labels = None
depends_on = None

class genderEnum(enum.Enum):
    M = "M"
    F = "F"

def upgrade() -> None:
    op.add_column('patient', sa.Column('nin', sa.String(length=11)))
    op.add_column('patient', sa.Column('gender', sa.Enum(genderEnum, name="gender_enum")))



def downgrade() -> None:
    op.add_column('user', sa.Column('failed_login_attempts', sa.INTEGER(default=0)))
    op.add_column('user', sa.Column('is_suspended', sa.BOOLEAN(default=False)))
    op.add_column('user', sa.Column('suspended_at', sa.DateTime()))

