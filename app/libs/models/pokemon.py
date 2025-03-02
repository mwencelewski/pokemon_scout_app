from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, select
from sqlalchemy import and_


class Species(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemons: List["Pokemon"] = Relationship(back_populates="species")


class PokemonForm(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    form_id: int = Field(foreign_key="form.id", primary_key=True)


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
    cries: Optional["PokemonCry"] = Relationship(back_populates="pokemon")
    moves: List["PokemonMove"] = Relationship(back_populates="pokemon")
    stats: List["PokemonStat"] = Relationship(back_populates="pokemon")
    forms: List["Form"] = Relationship(
        back_populates="pokemons", link_model=PokemonForm
    )
    types: List["PokemonType"] = Relationship(back_populates="pokemon")


class Form(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None
    pokemons: List[Pokemon] = Relationship(
        back_populates="forms", link_model=PokemonForm
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


class Cries(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    latest: Optional[str] = Field(default=None)
    legacy: Optional[str] = Field(default=None)
    pokemon_cries: List["PokemonCry"] = Relationship(back_populates="cry")


class PokemonCry(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    cry_id: int = Field(foreign_key="cries.id", primary_key=True)
    pokemon: Optional[Pokemon] = Relationship(back_populates="cries")
    cry: Optional[Cries] = Relationship(back_populates="pokemon_cries")


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


class Move(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None

    pokemon_associations: List["PokemonMove"] = Relationship(back_populates="move")


class PokemonMove(SQLModel, table=True):
    __tablename__ = "pokemon_move"
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    move_id: int = Field(foreign_key="move.id", primary_key=True)

    pokemon: Optional[Pokemon] = Relationship(back_populates="moves")
    move: Optional[Move] = Relationship(back_populates="pokemon_associations")
