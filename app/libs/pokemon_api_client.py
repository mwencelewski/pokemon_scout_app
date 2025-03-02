import httpx
from commons import config


class PokemonAPIClient:
    def __init__(self):
        self.base_url = config.API_POKEMON

    def get_pokemon(self, name):
        url = f"{self.base_url}/{name}"
        response = httpx.get(url)
        return response.json()
