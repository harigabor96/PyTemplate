import unittest

from sqlalchemy import text

from sample.utils import with_postgres


class TestDatabase(unittest.TestCase):

    def test_insert_user(self):
        with with_postgres() as engine:
            with engine.begin() as conn:
                conn.execute(
                    text("INSERT INTO users (name) VALUES (:name)"),
                    {"name": "Alice"},
                )

            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT name FROM users")
                )

                self.assertEqual(result.scalar_one(), "Alice")

    def test_empty_users(self):
        with with_postgres() as engine:
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM users")
                )

                self.assertEqual(result.fetchall(), [])


if __name__ == "__main__":
    unittest.main()
