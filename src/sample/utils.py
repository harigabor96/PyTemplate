from functools import wraps

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine
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

class PostgresQuery:
    def __init__(self, engine: Engine, query: str):
        self.engine = engine
        self.query = query

    def get_query(self) -> str:
        """Return the SQL query string."""
        return self.query

    def get_result(self) -> pd.DataFrame:
        """Execute the SQL query and return the result as a DataFrame."""
        with self.engine.connect() as connection:
            df = pd.read_sql_query(
                sql=text(self.query),
                con=connection
            )
        return df
