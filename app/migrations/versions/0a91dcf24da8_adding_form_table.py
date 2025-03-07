"""Adding Form Table

Revision ID: 0a91dcf24da8
Revises: 1ce24b569cc5
Create Date: 2025-03-02 15:50:41.331683

"""

from typing import Sequence, Union

from alembic import op 
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0a91dcf24da8"
down_revision: Union[str, None] = "1ce24b569cc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "form",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pokemonform",
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["form.id"],
        ),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.PrimaryKeyConstraint("pokemon_id", "form_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("pokemonform")
    op.drop_table("form")
    # ### end Alembic commands ###
