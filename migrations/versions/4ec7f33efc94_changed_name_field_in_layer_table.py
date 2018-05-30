"""changed name field in layer table

Revision ID: 4ec7f33efc94
Revises: 6998056be233
Create Date: 2018-05-30 22:02:59.327482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ec7f33efc94'
down_revision = '6998056be233'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('layer', sa.Column('tablename', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_layer_tablename'), 'layer', ['tablename'], unique=True)
    op.drop_index('ix_layer_name', table_name='layer')
    op.drop_column('layer', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('layer', sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.create_index('ix_layer_name', 'layer', ['name'], unique=True)
    op.drop_index(op.f('ix_layer_tablename'), table_name='layer')
    op.drop_column('layer', 'tablename')
    # ### end Alembic commands ###
