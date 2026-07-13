from aemet_weather.database import create_database_engine
from aemet_weather.download_history import main as download_history
from aemet_weather.generate_report import main as generate_report
from aemet_weather.load_history import main as load_history
from aemet_weather.pipeline_runs import (
    fail_pipeline_run,
    finish_pipeline_run,
    start_pipeline_run,
)
from aemet_weather.process_history import main as process_history


def main() -> None:
    engine = create_database_engine()
    run_id = start_pipeline_run(engine)

    print("=" * 60)
    print("INICIO DEL PIPELINE AEMET")
    print(f"Run ID: {run_id}")
    print("=" * 60)

    try:
        print()
        print("PASO 1 — DESCARGA")
        download_history()

        print()
        print("PASO 2 — TRANSFORMACIÓN")
        process_history()

        print()
        print("PASO 3 — CARGA EN POSTGRESQL")
        records_loaded = load_history()

        print()
        print("PASO 4 — GENERACIÓN DEL INFORME")
        generate_report()

        finish_pipeline_run(
            engine=engine,
            run_id=run_id,
            records_loaded=records_loaded,
        )

        print()
        print("=" * 60)
        print("PIPELINE COMPLETADO")
        print("=" * 60)

    except Exception as error:
        fail_pipeline_run(
            engine=engine,
            run_id=run_id,
            error_message=str(error),
        )

        print()
        print("=" * 60)
        print("PIPELINE FALLIDO")
        print(f"Error: {error}")
        print("=" * 60)

        raise


if __name__ == "__main__":
    main()