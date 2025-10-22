"""Alter user table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'user',
        sa.Column('age', sa.Integer(), nullable=False)
    )
    op.add_column(
        'user',
        sa.Column('gender', sa.String(length=20), nullable=False)
    )
    op.add_column(
        'user',
        sa.Column('name', sa.String(length=50), nullable=False)
    )
    op.add_column(
        'user',
        sa.Column('surname', sa.String(length=50), nullable=False)
    )
    op.add_column(
        'user',
        sa.Column('description', sa.String(length=500), nullable=False)
    )

def downgrade():
    op.drop_column('user', 'age')
    op.drop_column('user', 'gender')
    op.drop_column('user', 'name')
    op.drop_column('user', 'surname')
    op.drop_column('user', 'description')
