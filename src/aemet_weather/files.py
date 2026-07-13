from pathlib import Path


def get_latest_file(
    directory: Path,
    pattern: str,
) -> Path:
    """Devuelve el archivo más reciente que coincide con un patrón."""
    files = list(directory.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No se han encontrado archivos '{pattern}' en: {directory}"
        )

    return max(
        files,
        key=lambda path: path.stat().st_mtime,
    )


def get_latest_json(directory: Path) -> Path:
    """Devuelve el archivo JSON más reciente."""
    return get_latest_file(
        directory=directory,
        pattern="*.json",
    )


def get_latest_csv(directory: Path) -> Path:
    """Devuelve el archivo CSV más reciente."""
    return get_latest_file(
        directory=directory,
        pattern="*.csv",
    )