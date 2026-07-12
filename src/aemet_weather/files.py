from pathlib import Path


def get_latest_json(directory: Path) -> Path:
    """Devuelve el archivo JSON más reciente de una carpeta."""
    json_files = list(directory.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(
            f"No se han encontrado archivos JSON en: {directory}"
        )

    return max(
        json_files,
        key=lambda path: path.stat().st_mtime,
    )