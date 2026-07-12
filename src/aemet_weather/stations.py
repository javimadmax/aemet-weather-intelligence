from typing import Any


def search_stations(
    stations: list[dict[str, Any]],
    search_text: str,
) -> list[dict[str, Any]]:
    """
    Busca estaciones cuyo nombre o provincia contengan un texto.

    La búsqueda no distingue entre mayúsculas y minúsculas.
    """
    normalized_search = search_text.strip().lower()
    results: list[dict[str, Any]] = []

    for station in stations:
        name = str(station.get("nombre", "")).lower()
        province = str(station.get("provincia", "")).lower()

        if normalized_search in name or normalized_search in province:
            results.append(station)

    return results


def print_stations(stations: list[dict[str, Any]]) -> None:
    """Muestra una lista de estaciones en la terminal."""
    if not stations:
        print("No se han encontrado estaciones.")
        return

    print(
        f"{'CÓDIGO':<10}"
        f"{'NOMBRE':<45}"
        f"{'PROVINCIA':<20}"
        f"{'ALTITUD':>10}"
    )

    print("-" * 85)

    for station in stations:
        station_id = str(station.get("indicativo", ""))
        name = str(station.get("nombre", ""))
        province = str(station.get("provincia", ""))
        altitude = str(station.get("altitud", ""))

        print(
            f"{station_id:<10}"
            f"{name:<45}"
            f"{province:<20}"
            f"{altitude:>10}"
        )