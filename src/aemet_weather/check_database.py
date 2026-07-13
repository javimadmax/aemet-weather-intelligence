from aemet_weather.database import (
    check_database_connection,
    create_database_engine,
)


def main() -> None:
    print("Comprobando conexión con PostgreSQL...")

    engine = create_database_engine()
    database_name = check_database_connection(engine)

    print("Conexión correcta.")
    print(f"Base de datos: {database_name}")


if __name__ == "__main__":
    main()