from libs import pokemon_api_sanitize as sanitizer


def parser_payload(data):
    species = sanitizer.Species(data=data)
    pokemon = sanitizer.Pokemon(data=data)
    abilities = sanitizer.Abilities(data=data)
    pokemon_abilities = sanitizer.PokemonAbilities(data=data)
    cries = sanitizer.Cries(data=data)

    move = sanitizer.Moves(data=data)
    pokemon_move_detail = sanitizer.MovesVersionDetails(data=data)
    stat = sanitizer.Stats(data=data)
    type_ = sanitizer.Types(data=data)
    sprite = sanitizer.Sprite(data=data)
    forms = sanitizer.Forms(data=data)
    response = {
        "Pokemon": pokemon.build_df().to_dict(orient="records"),
        "Species": species.build_df().to_dict(orient="records"),
        "Abilities": abilities.build_df().to_dict(orient="records"),
        "PokemonAbilities": pokemon_abilities.build_df().to_dict(orient="records"),
        "Cries": cries.build_df().to_dict(orient="records"),
        "Type": type_.build_df().to_dict(orient="records"),
        "Forms": forms.build_df().to_dict(orient="records"),
        "Moves": move.build_df().to_dict(orient="records"),
        "Pokemon Move Detail": pokemon_move_detail.build_df().to_dict(orient="records"),
        "Stat": stat.build_df().to_dict(orient="records"),
        "Sprite": sprite.build_df().to_dict(orient="records"),
    }
    return response
