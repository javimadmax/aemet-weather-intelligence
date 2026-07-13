from sqlalchemy import Engine, create_engine, text

from aemet_weather.config import get_database_url


def create_database_engine() -> Engine:
    """Crea el motor de conexión con PostgreSQL."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )


def check_database_connection(engine: Engine) -> str:
    """Comprueba la conexión y devuelve el nombre de la base de datos."""
    query = text("SELECT current_database();")

    with engine.connect() as connection:
        result = connection.execute(query)
        database_name = result.scalar_one()

    return str(database_name)