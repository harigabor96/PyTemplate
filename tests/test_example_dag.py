import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from sample.example_dag import ExampleDAG, ExampleConf
from sample.example_dag_helper import AvgAge, User
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
            con=postgres_engine,
            name=test_table,
            index=False
        )

        mock_conf = MagicMock()
        mock_conf.source_table_user = test_table

        assert_frame_equal(
            test_dataframe,
            ExampleDAG(
                mock_conf,
                postgres_engine
            ).extract_user().get_dataframe()
        )

    @with_postgres
    def test_transform_avg_age(self, postgres_engine):
        test_table = "test_table"
        test_dataframe = User.validate(pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        }))

        test_dataframe.to_sql(
            con=postgres_engine,
            name=test_table,
            index=False
        )

        assert_frame_equal(
            AvgAge.validate(pd.DataFrame({
                "avg_age": [30.0],
            })),
            ExampleDAG(
                MagicMock(),
                postgres_engine
            ).transform_avg_age(
                PostgresQuery[User](postgres_engine, f"SELECT * FROM {test_table}")
            ).get_dataframe()
        )


if __name__ == "__main__":
    unittest.main()
