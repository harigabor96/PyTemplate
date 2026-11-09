from functools import wraps

from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer


def with_postgres(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        postgres = PostgresContainer(
            "postgres:16-alpine",
            driver="psycopg",
        )

        postgres.start()
        engine = create_engine(postgres.get_connection_url())

        try:
            return func(self, engine, *args, **kwargs)
        finally:
            engine.dispose()
            postgres.stop()

    return wrapper