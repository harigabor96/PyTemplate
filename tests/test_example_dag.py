import unittest

from sqlalchemy import text

from sample.utils import with_postgres


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

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT name FROM users")
            )

            self.assertEqual(result.scalar_one(), "Alice")


if __name__ == "__main__":
    unittest.main()
