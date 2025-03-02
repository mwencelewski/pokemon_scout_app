from libs.pokemon_api_sanitize_base import BaseDFBuilder
import pandas as pd


class Pokemon(BaseDFBuilder):
    def build_df(
        self,
    ):
        pokemon_df = pd.DataFrame([self.data])
        pokemon_df = pokemon_df.drop(
            columns=[
                "abilities",
                "cries",
                "forms",
                "game_indices",
                "held_items",
                "moves",
                "species",
                "sprites",
                "stats",
                "types",
                "past_abilities",
                "past_types",
            ]
        )
        # pokemon_df = pokemon_df.drop(columns=[
        #                                     'abilities', 'forms', 'game_indices', 'held_items', 'moves', 'stats', 'types'])
        return pokemon_df


class PokemonAbilities(BaseDFBuilder):
    def build_df(self) -> pd.DataFrame:  # type: ignore
        ability_df = pd.DataFrame(self.data["abilities"])
        ability_df["ability_id"] = ability_df["ability"].apply(
            lambda x: BaseDFBuilder.extract_id(x["url"])
        )
        return ability_df


class Abilities(BaseDFBuilder):
    def build_df(self):
        abilities_df = pd.json_normalize(self.data["abilities"])
        abilities_df["id"] = abilities_df["ability.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        abilities_df = abilities_df.drop(columns=["is_hidden", "slot"])
        abilities_df = abilities_df.rename(
            columns={"ability.name": "name", "ability.url": "url"}
        )
        return abilities_df


class Cries(BaseDFBuilder):
    def build_df(self):
        cries_df = pd.DataFrame([self.data["cries"]])
        return cries_df


class Forms(BaseDFBuilder):
    def build_df(self):
        forms_df = pd.DataFrame(self.data["forms"])
        return forms_df


class GameIndeces(BaseDFBuilder):
    def build_df(self):
        game_indices_df = pd.json_normalize(self.data["game_indices"])
        game_indices_df["version_id"] = game_indices_df["version.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        game_indices_df = game_indices_df.rename(
            columns={"version.name": "version_name", "version.url": "version_url"}
        )
        return game_indices_df


class HeldItems(BaseDFBuilder):
    def build_df(self):
        held_items_df = pd.json_normalize(self.data["held_items"])
        held_items_df["item_id"] = held_items_df["item.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        # held_items_df = held_items_df.drop(columns=['item.url'])
        held_items_df = held_items_df.rename(
            columns={"item.name": "item_name", "item.url": "item_url"}
        )
        held_items_df = held_items_df.drop(columns=["version_details"])
        return held_items_df


class HeldItemVersionDetails(BaseDFBuilder):
    def build_df(self) -> pd.DataFrame:
        df_held_item_version_details_df = pd.json_normalize(
            self.data["held_items"],
            record_path="version_details",
            meta=[["item", "url"]],
        )
        df_held_item_version_details_df["item_id"] = df_held_item_version_details_df[
            "item.url"
        ].apply(lambda x: BaseDFBuilder.extract_id(x))
        df_held_item_version_details_df["version_id"] = df_held_item_version_details_df[
            "version.url"
        ].apply(lambda x: BaseDFBuilder.extract_id(x))
        df_held_item_version_details_df = df_held_item_version_details_df.rename(
            columns={
                "item.name": "item_name",
                "item.url": "item_url",
                "version.name": "version_name",
                "version.url": "version_url",
            }
        )
        df_held_item_version_details_df = df_held_item_version_details_df[
            ["item_id", "rarity", "version_name", "version_url", "version_id"]
        ]
        return df_held_item_version_details_df


class MovesVersionDetails(BaseDFBuilder):
    def build_df(self):
        moves_df = pd.json_normalize(
            self.data["moves"],
            record_path="version_group_details",
            meta=[["move", "url"], ["move", "name"]],
        )
        moves_df["move_id"] = moves_df["move.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        moves_df = moves_df.rename(
            columns={"move.name": "move_name", "move.url": "move_url"}
        )
        return moves_df


class Moves(BaseDFBuilder):
    def build_df(self):
        moves_df = pd.json_normalize(self.data["moves"])
        moves_df["id"] = moves_df["move.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        moves_df = moves_df.rename(columns={"move.name": "name", "move.url": "url"})
        return moves_df


class Stats(BaseDFBuilder):
    def build_df(self):
        stats_df = pd.json_normalize(self.data["stats"])
        stats_df["id"] = stats_df["stat.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        stats_df = stats_df.rename(
            columns={
                "stat.name": "name",
                "stat.url": "url",
            }
        )
        return stats_df


class Types(BaseDFBuilder):
    def build_df(self):
        types = pd.json_normalize(self.data["types"])
        types["id"] = types["type.url"].apply(lambda x: BaseDFBuilder.extract_id(x))
        types = types.rename(columns={"type.name": "name", "type.url": "url"})
        return types


class Sprite(BaseDFBuilder):
    def build_df(self):
        sprite_df = pd.json_normalize(self.data["sprites"])

        return sprite_df


class Species(BaseDFBuilder):
    def build_df(self):
        species_df = pd.json_normalize(self.data["species"])
        if species_df.empty:
            return species_df
        species_df["id"] = species_df["url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        return species_df


class PastAbilities(BaseDFBuilder):
    def build_df(self):
        past_abilities_df = pd.json_normalize(self.data["past_abilities"])
        if past_abilities_df.empty:
            return past_abilities_df
        past_abilities_df["ability_id"] = past_abilities_df["ability.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        past_abilities_df = past_abilities_df.rename(
            columns={"ability.name": "ability_name", "ability.url": "ability_url"}
        )
        return past_abilities_df


class PastTypes(BaseDFBuilder):
    def build_df(self):
        past_types_df = pd.json_normalize(self.data["past_types"])
        if past_types_df.empty:
            return past_types_df
        past_types_df["type_id"] = past_types_df["type.url"].apply(
            lambda x: BaseDFBuilder.extract_id(x)
        )
        past_types_df = past_types_df.rename(
            columns={"type.name": "type_name", "type.url": "type_url"}
        )
        return past_types_df
