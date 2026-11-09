import unittest

from sqlalchemy import create_engine, text
from testcontainers.postgres import PostgresContainer

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres = PostgresContainer(
            "postgres:16-alpine",
            driver="psycopg",
        )
        cls.postgres.start()

        cls.engine = create_engine(
            cls.postgres.get_connection_url()
        )

        with cls.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """))

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
        cls.postgres.stop()

    def setUp(self):
        with self.engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY"))

    def test_insert_user(self):
        with self.engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {"name": "Alice"},
            )

        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT name FROM users")
            )

            self.assertEqual(result.scalar_one(), "Alice")

    def test_empty_users(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users"))

            self.assertEqual(result.fetchall(), [])


if __name__ == "__main__":
    unittest.main()
