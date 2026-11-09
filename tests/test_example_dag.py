import unittest

import pandas as pd
import pandera.pandas as pa
from pandas.testing import assert_frame_equal
from sqlalchemy import text

from sample.utils import with_postgres, PostgresQuery


class TestExampleDAG(unittest.TestCase):

    @with_postgres
    def test_insert_user(self, engine):
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """))
            conn.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {"name": "Alice"},
            )

            class UserSchema(pa.DataFrameModel):
                name: str

        query = PostgresQuery(engine, "SELECT name FROM users", UserSchema)

        print(query.get_result())
        print(query.get_query())

        assert_frame_equal(
            pd.DataFrame({
                "name": ["Alice"]
            }),
            query.get_result()
        )


if __name__ == "__main__":
    unittest.main()
