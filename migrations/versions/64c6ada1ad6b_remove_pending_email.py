"""remove pending_email

Revision ID: 64c6ada1ad6b
Revises: 7b3db26cb538
Create Date: 2016-12-02 11:55:46.295289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64c6ada1ad6b'
down_revision = '7b3db26cb538'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    #op.drop_index('ix_users_pending_email', table_name='users')
    #op.drop_column('users', 'pending_email')
    ### end Alembic commands ###

    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_index('ix_users_pending_email', table_name='users')
        batch_op.drop_column('pending_email')



def downgrade():
    ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('pending_email', sa.VARCHAR(length=64), nullable=True))
        batch_op.create_index('ix_users_pending_email', ['pending_email'], unique=1)
    ### end Alembic commands ###
