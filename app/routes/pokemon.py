from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlmodel import select
from libs import pokemon_api_client
from libs import pokemon_db_client
from libs.models import users
from libs import pokemon_parser as parser
from loguru import logger as log
import httpx

pokemon_bp = Blueprint("scrape", __name__)


@pokemon_bp.route("/pokemon/collect", methods=["POST"])
@jwt_required()
def fetch_data():
    """
    Ingest Pokemon data into the database
    ---
    tags:
      - Pokemon
    summary: Collect and ingest Pokemon data
    description: >
      This endpoint ingests Pokemon data into the database. It accepts a JSON payload containing a list of Pokemon names or IDs under the key "pokemon".
      For each provided Pokemon, it fetches data from an external Pokemon API, parses the data, and inserts multiple related records (Species, Pokemon, Abilities, Cries, Type, Stats, Forms, Moves) into the database.
      If an error occurs during data fetching, the endpoint records the error for that Pokemon and continues processing the rest.
    security:
      - Bearer: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: JSON payload containing list of Pokemon to ingest.
        required: true
        schema:
          type: object
          required:
            - pokemon
          properties:
            pokemon:
              type: array
              items:
                type: string
              description: List of Pokemon names or IDs to be ingested.
    responses:
      200:
        description: A list of ingestion results for each Pokemon.
        schema:
          type: array
          items:
            type: object
            properties:
              pokemon:
                type: string
                description: The Pokemon identifier that was processed.
              status:
                type: string
                description: Ingestion status for the Pokemon (e.g., "ingested", "error").
    """
    try:
        log.info("Ingesting Pokemon data into the Database")
        api = pokemon_api_client.PokemonAPIClient()
        data = request.get_json()
        pokemons = data.get("pokemon")

        response_pokemon_data = []
        for pokemon in pokemons:
            try:
                log.info(f"Fetching pokemon {pokemon}")
                result = api.get_pokemon(pokemon)
            except httpx.HTTPStatusError as e:
                log.error(f"Error fetching pokemon {pokemon} - {e}")
                response_pokemon_data.append({"pokemon": pokemon, "status": "error"})
                continue
            log.info("Parsing pokemon data")
            pokemon_parser_original = parser.parser_payload(result)
            with users.get_session() as session:
                log.info(f"Preparing parsed data for {pokemon}")
                pokemon_parser = pokemon_parser_original
                log.info("Creating database object")
                db_client = pokemon_db_client.PokemonClientDB(session=session)
                log.info("Inserting Species into database")
                species_data = db_client.create_species(pokemon_parser["Species"])
                log.info(species_data.id)
                pokemon_parser["Pokemon"][0]["species_id"] = species_data.id
                log.info("Creating Pokemon")
                pokemon_data = db_client.create_pokemon(pokemon_parser["Pokemon"])
                log.info(f"Pokemon created with Id  {pokemon_data.id}")
                log.info("Creating Abilities")
                ability_data = db_client.create_ability(
                    pokemon_parser["PokemonAbilities"]
                )
                log.warning(ability_data)
                log.info("Creating Cries")
                db_client.create_cries(pokemon_parser["Cries"])
                log.info("Creating Type")
                db_client.create_type(pokemon_parser["Type"])
                log.info("Creating Stats")
                # Create stats
                db_client.create_stat(pokemon_parser["Stat"])
                # Create Forms
                log.info("Creating Forms")
                db_client.create_forms(pokemon_parser["Forms"])
                # Create Moves
                log.info("Creating Moves")
                db_client.create_moves(pokemon_parser["Moves"])

            response_pokemon_data.append({"pokemon": pokemon, "status": "ingested"})
    except Exception as e:
        log.error(f"Error using the API {pokemon} - {e}")
    finally:
        return jsonify(response_pokemon_data)


@pokemon_bp.route("/pokemon", methods=["GET"])
@jwt_required()
def get_pokemon_by_type():
    """
    Retrieve Pokemon by type
    ---
    tags:
      - Pokemon
    summary: Retrieve Pokemon records filtered by type
    description: >
      This endpoint retrieves a list of Pokemon from the database that match the provided type.
      The type should be supplied as a query parameter. If the parameter is missing, an error is returned.
    security:
      - Bearer: []
    produces:
      - application/json
    parameters:
      - in: query
        name: type
        type: string
        required: true
        description: The type of Pokemon to filter by.
    responses:
      200:
        description: A list of Pokemon objects matching the specified type.
        schema:
          type: array
          items:
            type: object
            properties:
              # Example properties (customize according to your model)
              id:
                type: integer
                description: The unique identifier of the Pokemon.
              name:
                type: string
                description: The name of the Pokemon.
      400:
        description: Type parameter not provided
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message indicating that the type parameter is required.
    """
    type_filter = request.args.get("type")
    with users.get_session() as session:
        db_client = pokemon_db_client.PokemonClientDB(session=session)
        if type_filter:
            log.info(f"Getting pokemon by type {type_filter}")
            result = db_client.get_pokemon_by_type(type_filter)
        else:
            return jsonify({"error": "Type not provided"}), 400

        log.debug(result)
        pokemons = [pokemon.dict() for pokemon in result]
        return jsonify(pokemons)


@pokemon_bp.route("/pokemon/top", methods=["GET"])
@jwt_required()
def get_top_pokemons():
    """
    Retrieve top pokemons based on order and limit
    ---
    tags:
      - Pokemon
    summary: Retrieve top pokemons
    description: >
      This endpoint retrieves the top pokemons from the database based on the specified ordering and limit.
      The default limit is 10 and the default ordering is by base_experience in descending order.
    security:
      - Bearer: []
    produces:
      - application/json
    parameters:
      - in: query
        name: limit
        type: integer
        required: false
        default: 10
        description: The maximum number of pokemons to return.
      - in: query
        name: order_by
        type: string
        required: false
        default: base_experience_desc
        description: The field and order to sort pokemons by (e.g., "base_experience_desc").
    responses:
      200:
        description: A list of top pokemons.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The unique identifier of the pokemon.
              name:
                type: string
                description: The name of the pokemon.
              base_experience:
                type: integer
                description: The base experience of the pokemon.
    """
    limit = request.args.get("limit", 10, type=int)
    order_by = request.args.get("order_by", "base_experience_desc", type=str)
    with users.get_session() as session:
        db_client = pokemon_db_client.PokemonClientDB(session=session)
        result = db_client.get_top_pokemons(limit, order_by)
        log.debug(result)
        pokemons = [pokemon.dict() for pokemon in result]
        return jsonify(pokemons)


#
@pokemon_bp.route("/pokemon/with-species", methods=["GET"])
@jwt_required()
def get_pokemon_by_species():
    """
    Retrieve top pokemons based on order and limit
    ---
    tags:
      - Pokemon
    summary: Retrieve top pokemons
    description: >
      This endpoint retrieves the top pokemons from the database based on the specified ordering and limit.
      The default limit is 10 and the default ordering is by base_experience in descending order.
    security:
      - Bearer: []
    produces:
      - application/json
    parameters:
      - in: query
        name: limit
        type: integer
        required: false
        default: 10
        description: The maximum number of pokemons to return.
      - in: query
        name: order_by
        type: string
        required: false
        default: base_experience_desc
        description: The field and order to sort pokemons by (e.g., "base_experience_desc").
    responses:
      200:
        description: A list of top pokemons.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The unique identifier of the pokemon.
              name:
                type: string
                description: The name of the pokemon.
              base_experience:
                type: integer
                description: The base experience of the pokemon.
    """
    with users.get_session() as session:
        db_client = pokemon_db_client.PokemonClientDB(session=session)
        result = db_client.get_pokemons_by_species()
        log.debug(result)
        pokemons = [
            {
                "id": pokemon.id,
                "name": pokemon.name,
                "species": species.name,
                "species_id": species.id,
            }
            for pokemon, species in result
        ]
        return jsonify(pokemons)


@pokemon_bp.route("/types/pokemon-count", methods=["GET"])
@jwt_required()
def get_types_pokemon_count():
    """
    Get pokemon count by type
    ---
    tags:
      - Pokemon
    summary: Retrieve count of pokemons for each type
    description: >
      This endpoint retrieves the count of pokemons for each type available in the database.
      The response is a list of objects, where each object contains a 'type_name' and the 'total_pokemons' count for that type.
    security:
      - Bearer: []
    produces:
      - application/json
    responses:
      200:
        description: A list of pokemon types with their corresponding counts.
        schema:
          type: array
          items:
            type: object
            properties:
              type_name:
                type: string
                description: The name of the pokemon type.
              total_pokemons:
                type: integer
                description: The total number of pokemons of that type.
    """
    with users.get_session() as session:
        db_client = pokemon_db_client.PokemonClientDB(session=session)
        results = db_client.get_pokemon_count()

        data = [
            {"type_name": type_name, "total_pokemons": total_pokemons}
            for type_name, total_pokemons in results
        ]
        log.debug(results)

        return jsonify(data)


@pokemon_bp.route("/stats/hp/average", methods=["GET"])
@jwt_required()
def get_hp_average():
    """
    Retrieve average HP of pokemons
    ---
    tags:
      - Pokemon
    summary: Retrieve average HP of all pokemons
    description: >
      This endpoint calculates and returns the average HP (Hit Points) of all pokemons stored in the database.
    security:
      - Bearer: []
    produces:
      - application/json
    responses:
      200:
        description: A JSON array containing the average HP value.
        schema:
          type: array
          items:
            type: object
            properties:
              average_hp:
                type: number
                description: The computed average HP value across all pokemons.
    """
    with users.get_session() as session:
        db_client = pokemon_db_client.PokemonClientDB(session=session)
        result = db_client.get_hp_average()
        log.debug(result)
        data = [{"average_hp": result}]

        return jsonify(data)
