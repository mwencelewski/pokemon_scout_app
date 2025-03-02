from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Species(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemons: List["Pokemon"] = Relationship(back_populates="species")


class Pokemon(SQLModel, table=True):
    id: int = Field(primary_key=True)  # Id do Pokémon
    name: str
    base_experience: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    order: Optional[int] = None
    is_default: Optional[bool] = None
    location_area_encounters: Optional[str] = None

    species_id: Optional[int] = Field(default=None, foreign_key="species.id")
    species: Optional[Species] = Relationship(back_populates="pokemons")

    abilities: List["PokemonAbility"] = Relationship(back_populates="pokemon")
    moves: List["PokemonMove"] = Relationship(back_populates="pokemon")
    stats: List["PokemonStat"] = Relationship(back_populates="pokemon")
    types: List["PokemonType"] = Relationship(back_populates="pokemon")
    sprite: Optional["Sprite"] = Relationship(
        back_populates="pokemon", sa_relationship_kwargs={"uselist": False}
    )


class Ability(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemon_associations: List["PokemonAbility"] = Relationship(
        back_populates="ability"
    )


class PokemonAbility(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    ability_id: int = Field(foreign_key="ability.id", primary_key=True)
    is_hidden: Optional[bool] = None
    slot: Optional[int] = None

    pokemon: Optional[Pokemon] = Relationship(back_populates="abilities")
    ability: Optional[Ability] = Relationship(back_populates="pokemon_associations")


class Move(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemon_associations: List["PokemonMove"] = Relationship(back_populates="move")


class MoveLearnMethod(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    move_details: List["PokemonMoveDetail"] = Relationship(
        back_populates="move_learn_method"
    )


class VersionGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    move_details: List["PokemonMoveDetail"] = Relationship(
        back_populates="version_group"
    )


class PokemonMove(SQLModel, table=True):
    __tablename__ = "pokemon_move"
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    move_id: int = Field(foreign_key="move.id", primary_key=True)

    pokemon: Optional[Pokemon] = Relationship(back_populates="moves")
    move: Optional[Move] = Relationship(back_populates="pokemon_associations")
    details: List["PokemonMoveDetail"] = Relationship(
        back_populates="pokemon_move", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class PokemonMoveDetail(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon_move.pokemon_id", primary_key=True)
    move_id: int = Field(foreign_key="pokemon_move.move_id", primary_key=True)
    move_learn_method_id: int = Field(
        foreign_key="movelearnmethod.id", primary_key=True
    )
    version_group_id: int = Field(foreign_key="versiongroup.id", primary_key=True)
    level_learned_at: Optional[int] = None

    pokemon_move: Optional[PokemonMove] = Relationship(back_populates="details")
    move_learn_method: Optional[MoveLearnMethod] = Relationship(
        back_populates="move_details"
    )
    version_group: Optional[VersionGroup] = Relationship(back_populates="move_details")


class Stat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemon_stats: List["PokemonStat"] = Relationship(back_populates="stat")


class PokemonStat(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    stat_id: int = Field(foreign_key="stat.id", primary_key=True)
    base_stat: Optional[int] = None
    effort: Optional[int] = None

    pokemon: Optional[Pokemon] = Relationship(back_populates="stats")
    stat: Optional[Stat] = Relationship(back_populates="pokemon_stats")


class Type(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemon_types: List["PokemonType"] = Relationship(back_populates="type")


class PokemonType(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    type_id: int = Field(foreign_key="type.id", primary_key=True)
    slot: Optional[int] = None

    pokemon: Optional[Pokemon] = Relationship(back_populates="types")
    type: Optional[Type] = Relationship(back_populates="pokemon_types")


class Sprite(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    front_default: Optional[str] = None
    back_default: Optional[str] = None
    front_shiny: Optional[str] = None
    back_shiny: Optional[str] = None

    pokemon: Optional[Pokemon] = Relationship(back_populates="sprite")
