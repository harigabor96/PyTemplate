
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from testcontainers.postgres import PostgresContainer


@contextmanager
def with_postgres():
    postgres = PostgresContainer(
        "postgres:16-alpine",
        driver="psycopg",
    )

    postgres.start()
    engine = create_engine(postgres.get_connection_url())

    try:
        yield engine
    finally:
        engine.dispose()
        postgres.stop()
