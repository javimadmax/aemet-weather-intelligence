from typing import Any

import requests

from aemet_weather.config import get_aemet_api_key

from datetime import date

import time

AEMET_BASE_URL = "https://opendata.aemet.es/opendata/api"

STATIONS_ENDPOINT = (
    f"{AEMET_BASE_URL}/valores/climatologicos/"
    "inventarioestaciones/todasestaciones"
)


def request_aemet_metadata(
    endpoint: str,
    max_attempts: int = 3,
) -> dict[str, Any]:
    """
    Realiza una petición a AEMET.

    Reintenta temporalmente cuando AEMET responde con HTTP 429.
    """
    api_key = get_aemet_api_key()

    for attempt in range(1, max_attempts + 1):
        response = requests.get(
            endpoint,
            params={"api_key": api_key},
            timeout=30,
        )

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            if retry_after and retry_after.isdigit():
                wait_seconds = int(retry_after)
            else:
                wait_seconds = 60 * attempt

            if attempt == max_attempts:
                raise RuntimeError(
                    "AEMET ha rechazado la petición por exceso de solicitudes. "
                    "No se realizarán más intentos. Prueba más tarde."
                )

            print(
                "AEMET ha respondido con HTTP 429. "
                f"Nuevo intento en {wait_seconds} segundos "
                f"({attempt}/{max_attempts})."
            )

            time.sleep(wait_seconds)
            continue

        if response.status_code == 401:
            raise RuntimeError(
                "La API key de AEMET no es válida o no está autorizada."
            )

        if response.status_code == 404:
            raise RuntimeError(
                "AEMET no ha encontrado datos para el recurso solicitado. "
                "Comprueba la estación y las fechas."
            )

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise RuntimeError(
                "No se pudo completar la petición a AEMET. "
                f"Código HTTP: {response.status_code}."
            ) from error

        metadata = response.json()

        if not isinstance(metadata, dict):
            raise TypeError(
                "La respuesta de metadatos de AEMET no es un objeto JSON."
            )

        return metadata

    raise RuntimeError("No se pudo completar la petición a AEMET.")

def download_json(data_url: str) -> Any:
    """Descarga el JSON desde la URL temporal generada por AEMET."""
    try:
        response = requests.get(
            data_url,
            timeout=30,
        )

        response.raise_for_status()

    except requests.Timeout as error:
        raise RuntimeError(
            "La descarga de datos de AEMET ha superado el tiempo de espera."
        ) from error

    except requests.RequestException as error:
        raise RuntimeError(
            "No se pudieron descargar los datos desde la URL temporal de AEMET."
        ) from error

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

def get_daily_climatology(
    station_id: str,
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """Descarga valores climatológicos diarios de una estación."""
    start_text = f"{start_date.isoformat()}T00:00:00UTC"
    end_text = f"{end_date.isoformat()}T23:59:59UTC"

    endpoint = (
        f"{AEMET_BASE_URL}/valores/climatologicos/diarios/datos/"
        f"fechaini/{start_text}/"
        f"fechafin/{end_text}/"
        f"estacion/{station_id}"
    )

    metadata = request_aemet_metadata(endpoint)

    if "datos" not in metadata:
        raise ValueError(
            "AEMET no ha proporcionado una URL de datos. "
            f"Respuesta recibida: {metadata}"
        )

    observations = download_json(metadata["datos"])

    if not isinstance(observations, list):
        raise TypeError(
            "Se esperaba una lista de observaciones climatológicas."
        )

    return observations