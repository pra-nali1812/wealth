"""Add investment strategy model

Revision ID: e8a2e26fb728
Revises: 65b36087c84a
Create Date: 2025-04-28 16:59:33.639999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8a2e26fb728'
down_revision = '65b36087c84a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('investment_strategy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('risk_profile', sa.String(length=50), nullable=False),
    sa.Column('allocations', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('investment_strategy')
    # ### end Alembic commands ###
