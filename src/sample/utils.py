from functools import wraps
from typing import TypeVar

import pandas as pd
import pandera.pandas as pa
from sqlalchemy import Engine, text
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

SchemaType = TypeVar("SchemaType", bound=pa.DataFrameModel)
class PostgresQuery:
    schema: type[pa.DataFrameModel]

    def __class_getitem__(cls, schema: type[SchemaType]):
        return type(
            f"{cls.__name__}[{schema.__name__}]",
            (cls,),
            {"schema": schema},
        )

    def __init__(self, engine: Engine, query: str):
        self.engine = engine
        self.query = query

    def get_query(self) -> str:
        return self.query

    def get_result(self) -> pd.DataFrame:
        with self.engine.connect() as connection:
            df = pd.read_sql_query(
                sql=text(self.query),
                con=connection,
            )

        return self.schema.validate(df)
