from libs.models import pokemon
from libs.models import users
from loguru import logger as log
from sqlmodel import select
from sqlalchemy import func


class PokemonClientDB:
    def __init__(self, session):
        self.session = session

    def create_species(self, species_data):
        for specie in species_data:
            species_obj = pokemon.Species(**specie)
            self.session.merge(species_obj)
            self.session.commit()
        return species_obj

    def create_pokemon(self, pokemon_data):
        for pokemon_ in pokemon_data:
            pokemon_obj = pokemon.Pokemon(**pokemon_)
            self.session.merge(pokemon_obj)
            self.session.commit()
            self.pokemon_id = pokemon_obj.id
        return pokemon_obj

    def create_ability(self, ability_data):
        ability_ids = []
        for ability in ability_data:
            ability_ = ability["ability"]
            ability_["id"] = ability["ability_id"]
            log.warning(ability_)
            ability_obj = pokemon.Ability(**ability_)
            self.session.merge(ability_obj)
            self.session.commit()
            self.create_pokemon_ability(ability, self.pokemon_id, ability_["id"])
            ability_ids.append(ability_obj.id)
        return ability_ids

    def create_pokemon_ability(
        self, pokemon_ability: dict, pokemon_id: int, ability_id: list[int]
    ):
        log.debug(f"Creating Pokemon Ability - {pokemon_ability}")
        pokemon_ability.pop("ability")
        pokemon_ability["pokemon_id"] = pokemon_id
        pokemon_ability["ability_id"] = ability_id
        log.warning(pokemon_ability)
        pokemon_ability_obj = pokemon.PokemonAbility(**pokemon_ability)
        self.session.merge(pokemon_ability_obj)
        self.session.commit()
        return pokemon_ability_obj

    def create_cries(self, cries_data):
        for cry in cries_data:
            log.debug(f"Creating cry - {cry}")
            cry_obj = pokemon.Cries(**cry)
            merge_obj = self.session.merge(cry_obj)
            self.session.flush()
            log.debug(f"Creating cry relation with id {merge_obj.id}")
            self.session.commit()
            pokemon_cry = {"pokemon_id": self.pokemon_id, "cry_id": merge_obj.id}
            self.create_pokemon_cry(pokemon_cry)
        return cry_obj

    def create_pokemon_cry(self, pokemon_cry):
        pokemon_cry_obj = pokemon.PokemonCry(**pokemon_cry)
        self.session.merge(pokemon_cry_obj)
        self.session.commit()
        return pokemon_cry_obj

    def create_type(self, type_data):
        for type_ in type_data:
            type_obj = pokemon.Type(**type_)
            merge_obj = self.session.merge(type_obj)
            self.session.commit()
            self.type_id = merge_obj.id
            self.create_pokemon_type(type_)
        return type_obj

    def create_pokemon_type(self, pokemon_type):
        pokemon_type["pokemon_id"] = self.pokemon_id
        pokemon_type["type_id"] = self.type_id
        pokemon_type_obj = pokemon.PokemonType(**pokemon_type)
        self.session.merge(pokemon_type_obj)
        self.session.commit()
        return pokemon_type_obj

    def create_stat(self, stat_data):
        for stat in stat_data:
            stat_obj = pokemon.Stat(**stat)
            merge_obj = self.session.merge(stat_obj)
            self.session.commit()
            stat["db_id"] = merge_obj.id
            self.create_pokemon_stat(stat)

        return stat_obj

    def create_pokemon_stat(self, stat_data):
        stat_data["pokemon_id"] = self.pokemon_id
        stat_data["stat_id"] = stat_data["db_id"]
        stat_obj = pokemon.PokemonStat(**stat_data)
        self.session.merge(stat_obj)
        self.session.commit()
        return stat_obj

    def create_forms(self, forms_data):
        for form in forms_data:
            form_obj = pokemon.Form(**form)
            merge_obj = self.session.merge(form_obj)
            self.session.commit()
            self.create_pokemon_form(
                {"form_id": merge_obj.id, "pokemon_id": self.pokemon_id}
            )
        return form_obj

    def create_pokemon_form(self, pokemon_form):
        form_obj = pokemon.PokemonForm(**pokemon_form)
        self.session.merge(form_obj)
        self.session.commit()
        return form_obj

    def create_moves(self, moves_data):
        for move in moves_data:
            move_obj = pokemon.Move(**move)
            merge_obj = self.session.merge(move_obj)
            self.session.commit()
            self.create_pokemon_move(
                {"move_id": merge_obj.id, "pokemon_id": self.pokemon_id}
            )
        return move_obj

    def create_pokemon_move(self, pokemon_move):
        move_obj = pokemon.PokemonMove(**pokemon_move)
        self.session.merge(move_obj)
        self.session.commit()
        return move_obj

    def get_pokemon_by_type(self, type_filter):
        return (
            self.session.query(pokemon.Pokemon)
            .join(pokemon.PokemonType)
            .join(pokemon.Type)
            .filter(pokemon.Type.name == type_filter)
            .all()
        )

    def get_top_pokemons(self, limit, order_by):
        if order_by == "base_experience_desc":
            return (
                self.session.query(pokemon.Pokemon)
                .order_by(pokemon.Pokemon.base_experience.desc())
                .limit(limit)
                .all()
            )
        elif order_by == "base_experience_asc":
            return (
                self.session.query(pokemon.Pokemon)
                .order_by(pokemon.Pokemon.base_experience.asc())
                .limit(limit)
                .all()
            )
        else:
            return self.session.query(pokemon.Pokemon).limit(limit).all()

    def get_pokemons_by_species(self):
        stmt = select(pokemon.Pokemon, pokemon.Species).join(
            pokemon.Species, pokemon.Pokemon.species_id == pokemon.Species.id
        )
        result = self.session.exec(stmt)
        return result.all()

    def get_pokemon_count(self):
        stmt = (
            select(
                pokemon.Type.name,
                func.count(pokemon.PokemonType.pokemon_id).label("total_pokemons"),
            )
            .join(pokemon.PokemonType, pokemon.Type.id == pokemon.PokemonType.type_id)
            .group_by(pokemon.Type.name)
        )

        result = self.session.exec(stmt)
        return result.all()

    def get_hp_average(self):
        stmt = (
            select(func.avg(pokemon.PokemonStat.base_stat))
            .join(pokemon.Stat, pokemon.PokemonStat.stat_id == pokemon.Stat.id)
            .where(pokemon.Stat.name == "hp")
        )
        result = self.session.exec(stmt)
        return result.one()
