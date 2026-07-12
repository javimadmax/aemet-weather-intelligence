import os

from dotenv import load_dotenv


load_dotenv()


def get_aemet_api_key() -> str:
    """Obtiene la API key de AEMET desde las variables de entorno."""
    api_key = os.getenv("AEMET_API_KEY")

    if not api_key:
        raise ValueError(
            "No se ha encontrado AEMET_API_KEY. "
            "Comprueba que existe el archivo .env."
        )

    return api_key


def get_station_id() -> str:
    """Obtiene el identificador de estación configurado."""
    station_id = os.getenv("AEMET_STATION_ID")

    if not station_id:
        raise ValueError(
            "No se ha encontrado AEMET_STATION_ID. "
            "Añade la estación seleccionada al archivo .env."
        )

    return station_id