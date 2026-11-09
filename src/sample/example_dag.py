from dataclasses import dataclass

from sqlalchemy import Engine
from sqlalchemy import text

from sample.example_dag_helper import AvgAge, User
from sample.utils import PostgresQuery


@dataclass
class ExampleConf:
    source_table_user: str
    sink_table_avg_age: str

class ExampleDAG:
    def __init__(self, conf: ExampleConf, postgres_engine: Engine):
        self.conf = conf
        self.postgres_engine = postgres_engine

    def execute(self) -> None:
        extract_user_query = self.extract_user()
        transform_avg_age = self.transform_avg_age(extract_user_query)
        self.load_sink(transform_avg_age)

    def extract_user(self) -> PostgresQuery[User]:
        return PostgresQuery[User](self.postgres_engine, f"""
            SELECT * FROM {self.conf.source_table_user};
        """)

    def transform_avg_age(self, extract_user_query: PostgresQuery[User]) -> PostgresQuery[AvgAge]:
        return PostgresQuery[AvgAge](self.postgres_engine, f"""
            SELECT age
            FROM ({extract_user_query.get_text()})
        """)

    def load_sink(self, transform_avg_age_query: PostgresQuery[AvgAge]) -> None:
        with self.postgres_engine.begin() as conn:
            conn.execute(text(f"""
                INSERT INTO {self.conf.sink_table_avg_age} (age)
                FROM ({transform_avg_age_query.get_text()})
            """))
