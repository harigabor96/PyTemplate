import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from sample.example_dag import ExampleConf, ExampleDAG
from sample.example_dag_helper import AvgAge, User
from sample.utils import with_postgres, PostgresQuery


class TestExampleDAG(unittest.TestCase):

    @with_postgres
    def test_execute(self, postgres_engine):
        test_source = "test_source"
        test_sink = "test_sink"

        User.validate(pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        })).to_sql(
            con=postgres_engine,
            name=test_source,
            index=False
        )

        AvgAge.validate(pd.DataFrame({
            "avg_age": [],
        })).to_sql(
            con=postgres_engine,
            name=test_sink,
            index=False
        )

        ExampleDAG(
            ExampleConf(
                source_table_user=test_source,
                sink_table_avg_age=test_sink
            ),
            postgres_engine
        ).execute()

        assert_frame_equal(
            AvgAge.validate(pd.DataFrame({
                "avg_age": [30.0],
            })),
            PostgresQuery[AvgAge](postgres_engine, f"SELECT * FROM {test_sink}").get_dataframe()
        )

    @with_postgres
    def test_extract_user(self, postgres_engine):
        test_table = "test_table"

        User.validate(pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        })).to_sql(
            con=postgres_engine,
            name=test_table,
            index=False
        )

        mock_conf = MagicMock()
        mock_conf.source_table_user = test_table
        result = (
            ExampleDAG(
                mock_conf,
                postgres_engine
            ).extract_user().get_dataframe()
        )

        assert_frame_equal(
            User.validate(pd.DataFrame({
                "id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
                "age": [25, 30, 35],
            })),
            result
        )

    @with_postgres
    def test_transform_avg_age(self, postgres_engine):
        test_table = "test_table"

        User.validate(pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        })).to_sql(
            con=postgres_engine,
            name=test_table,
            index=False
        )

        result = (
            ExampleDAG(
                MagicMock(),
                postgres_engine
            ).transform_avg_age(
                PostgresQuery[User](postgres_engine, f"SELECT * FROM {test_table}")
            ).get_dataframe()
        )

        assert_frame_equal(
            AvgAge.validate(pd.DataFrame({
                "avg_age": [30.0],
            })),
            result
        )

    @with_postgres
    def test_load_sink(self, postgres_engine):
        test_source = "test_source"
        test_sink = "test_sink"

        AvgAge.validate(pd.DataFrame({
            "avg_age": [30.0],
        })).to_sql(
            con=postgres_engine,
            name=test_source,
            index=False
        )

        AvgAge.validate(pd.DataFrame({
            "avg_age": [],
        })).to_sql(
            con=postgres_engine,
            name=test_sink,
            index=False
        )

        mock_conf = MagicMock()
        mock_conf.sink_table_avg_age = test_sink
        ExampleDAG(
            mock_conf,
            postgres_engine
        ).load_avg_age(
            PostgresQuery[AvgAge](postgres_engine, f"SELECT * FROM {test_source}")
        )

        assert_frame_equal(
            AvgAge.validate(pd.DataFrame({
                "avg_age": [30.0],
            })),
            PostgresQuery[AvgAge](postgres_engine, f"SELECT * FROM {test_sink}").get_dataframe()
        )


if __name__ == "__main__":
    unittest.main()
