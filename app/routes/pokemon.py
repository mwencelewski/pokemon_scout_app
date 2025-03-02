from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlmodel import select
from libs import pokemon_api_client

pokemon_bp = Blueprint("scrape", __name__)


@pokemon_bp.route("/pokemon", methods=["POST"])
@jwt_required()
def fetch_data():
    api = pokemon_api_client.PokemonAPIClient()
    data = request.get_json()
    pokemon = data.get("pokemon")

    result = api.get_pokemon(pokemon)
    return jsonify(result)
