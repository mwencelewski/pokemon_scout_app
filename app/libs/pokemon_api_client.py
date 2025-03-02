import httpx
from commons import config
from loguru import logger as log


class PokemonAPIClient:
    def __init__(self):
        self.base_url = config.API_POKEMON

    def get_pokemon(self, name):
        log.info(f"Getting pokemon {name}")
        url = f"{self.base_url}/{name}"
        response = httpx.get(url)
        if response.status_code != 200:
            log.error(f"Error while calling the pokemon api {name} - {response.text}")
            raise response.raise_for_status()
        return response.json()
