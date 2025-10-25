"""Alter user table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '3'
down_revision = '2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'user',
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.alter_column(
        'user',
        'created_at',
        server_default=None)


def downgrade():
    op.drop_column('user', 'created_at')
