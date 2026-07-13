from datetime import UTC, datetime

from sqlalchemy import Engine, text


def start_pipeline_run(engine: Engine) -> int:
    """Crea un registro de ejecución con estado running."""
    query = text(
        """
        INSERT INTO pipeline_runs (
            started_at,
            status
        )
        VALUES (
            :started_at,
            'running'
        )
        RETURNING run_id;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "started_at": datetime.now(UTC),
            },
        )

        run_id = result.scalar_one()

    return int(run_id)


def finish_pipeline_run(
    engine: Engine,
    run_id: int,
    records_loaded: int | None = None,
) -> None:
    """Marca una ejecución como completada."""
    query = text(
        """
        UPDATE pipeline_runs
        SET
            finished_at = :finished_at,
            status = 'success',
            records_loaded = :records_loaded,
            error_message = NULL
        WHERE run_id = :run_id;
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "finished_at": datetime.now(UTC),
                "records_loaded": records_loaded,
                "run_id": run_id,
            },
        )


def fail_pipeline_run(
    engine: Engine,
    run_id: int,
    error_message: str,
) -> None:
    """Marca una ejecución como fallida."""
    query = text(
        """
        UPDATE pipeline_runs
        SET
            finished_at = :finished_at,
            status = 'failed',
            error_message = :error_message
        WHERE run_id = :run_id;
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "finished_at": datetime.now(UTC),
                "error_message": error_message[:2000],
                "run_id": run_id,
            },
        )