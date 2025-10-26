"""Create users table"""

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = '1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('login', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login'),
        schema='public'
    )


def downgrade():
    op.drop_table('user')
