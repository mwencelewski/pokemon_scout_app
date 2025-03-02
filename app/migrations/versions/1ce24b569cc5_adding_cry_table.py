"""Adding cry table

Revision ID: 1ce24b569cc5
Revises: 49d7ef6c483d
Create Date: 2025-03-02 14:11:22.017171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '1ce24b569cc5'
down_revision: Union[str, None] = '49d7ef6c483d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('latest', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('legacy', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pokemoncry',
    sa.Column('pokemon_id', sa.Integer(), nullable=False),
    sa.Column('cry_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cry_id'], ['cries.id'], ),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ),
    sa.PrimaryKeyConstraint('pokemon_id', 'cry_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemoncry')
    op.drop_table('cries')
    # ### end Alembic commands ###
