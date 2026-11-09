import unittest

import pandas as pd
import pandera.pandas as pa
from pandas.testing import assert_frame_equal
from sqlalchemy import text

from sample.example_dag import ExampleDAG, ExampleConf
from sample.example_dag_helper import User
from sample.utils import with_postgres, PostgresQuery


class TestExampleDAG(unittest.TestCase):

    @with_postgres
    def test_extract_user(self, postgres_engine):
        test_table = "test_table"
        test_dataframe = User.validate(pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        }))

        test_dataframe.to_sql(
            con = postgres_engine,
            name = test_table,
            index = False
        )

        assert_frame_equal(
            test_dataframe,
            ExampleDAG(
                ExampleConf(
                    source_table_user = test_table,
                    sink_table_avg_age = "NEEEDS TO BE MOCKETD"
                ),
                postgres_engine
            ).extract_user().get_dataframe()
        )

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

        query = PostgresQuery[UserSchema]("SELECT name FROM users")

        print(query.get_dataframe(engine))
        print(query.get_text())

        assert_frame_equal(
            pd.DataFrame({
                "name": ["Alice"]
            }),
            query.get_dataframe(engine)
        )


if __name__ == "__main__":
    unittest.main()
