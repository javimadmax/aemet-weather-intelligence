from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, text


def read_sql_file(path: Path) -> str:
    """Lee una consulta SQL desde un archivo."""
    return path.read_text(encoding="utf-8")


def execute_query_as_dataframe(
    engine: Engine,
    sql_path: Path,
) -> pd.DataFrame:
    """Ejecuta una consulta SQL y devuelve el resultado como DataFrame."""
    query = read_sql_file(sql_path)

    with engine.connect() as connection:
        return pd.read_sql(
            text(query),
            connection,
        )