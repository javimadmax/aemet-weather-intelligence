import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


RAW_DATA_DIRECTORY = Path("data/raw")


def save_json(
    data: Any,
    category: str,
    filename_prefix: str,
) -> Path:
    """Guarda datos JSON crudos con una marca temporal."""
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    output_directory = RAW_DATA_DIRECTORY / category
    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / f"{filename_prefix}_{timestamp}.json"

    with output_path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path