"""empty message

Revision ID: 8060bc3932b1
Revises: 
Create Date: 2019-10-21 16:34:40.620156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8060bc3932b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('connections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('dev1', sa.String(length=100), nullable=True),
    sa.Column('dev2', sa.String(length=100), nullable=True),
    sa.Column('are_linked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dev1', 'dev2', 'timestamp', name='_devs_timestamp_uc')
    )
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('external_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connection_x_organization_table',
    sa.Column('connections_id', sa.Integer(), nullable=False),
    sa.Column('organizations_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['connections_id'], ['connections.id'], ),
    sa.ForeignKeyConstraint(['organizations_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('connections_id', 'organizations_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('connection_x_organization_table')
    op.drop_table('organizations')
    op.drop_table('connections')
    # ### end Alembic commands ###
