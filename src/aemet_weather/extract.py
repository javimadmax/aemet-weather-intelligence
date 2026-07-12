from typing import Any

import requests

from aemet_weather.config import get_aemet_api_key


AEMET_BASE_URL = "https://opendata.aemet.es/opendata/api"

STATIONS_ENDPOINT = (
    f"{AEMET_BASE_URL}/valores/climatologicos/"
    "inventarioestaciones/todasestaciones"
)


def request_aemet_metadata(endpoint: str) -> dict[str, Any]:
    """Realiza una petición a un endpoint de AEMET OpenData."""
    api_key = get_aemet_api_key()

    response = requests.get(
        endpoint,
        params={"api_key": api_key},
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def download_json(data_url: str) -> Any:
    """Descarga los datos desde la URL temporal devuelta por AEMET."""
    response = requests.get(
        data_url,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_all_stations() -> list[dict[str, Any]]:
    """Descarga el inventario completo de estaciones climatológicas."""
    metadata = request_aemet_metadata(STATIONS_ENDPOINT)

    if "datos" not in metadata:
        raise ValueError(
            "La respuesta de AEMET no contiene la propiedad 'datos'. "
            f"Respuesta recibida: {metadata}"
        )

    stations = download_json(metadata["datos"])

    if not isinstance(stations, list):
        raise TypeError("Se esperaba una lista de estaciones.")

    return stations