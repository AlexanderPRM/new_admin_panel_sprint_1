import os
import sqlite3
import unittest

import psycopg2
from dotenv import load_dotenv
from parameterized import parameterized_class
from psycopg2.extras import DictCursor

load_dotenv()


@parameterized_class(
    ("table"),
    [
        ("genre",),
        ("film_work",),
        ("person",),
        ("person_film_work",),
        ("genre_film_work",),
    ],
)
class TestMigrator(unittest.TestCase):
    def setUp(self):
        self.dls = {
            "dbname": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "host": "127.0.0.1",
            "port": 5432,
        }
        self.sqlite_conn = sqlite3.connect(
            "new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite"
        )
        self.pg_conn = psycopg2.connect(**self.dls, cursor_factory=DictCursor)
        self.pg_cur = self.pg_conn.cursor()
        self.sqlite_cur = self.sqlite_conn.cursor()

    def test_entries_count(self):
        self.pg_cur.execute(
            "SELECT COUNT(*) FROM content.{0}".format(self.table)
        )
        self.sqlite_cur.execute("SELECT COUNT(*) FROM {0}".format(self.table))
        assert self.pg_cur.fetchone()[0] == self.sqlite_cur.fetchone()[0]

    def test_entries_values(self):
        self.pg_cur.execute("SELECT * FROM content.{0}".format(self.table))
        self.sqlite_cur.execute("SELECT * FROM {0}".format(self.table))
        for pg_entry, sq_entry in zip(
            self.pg_cur.fetchall(), self.sqlite_cur.fetchall()
        ):
            # Обрезание даты. В SQLite и PSQL храниться по разному.
            if self.table in ["person_film_work", "genre_film_work"]:
                assert pg_entry[:-1] == list(sq_entry)[:-1]
            else:
                assert pg_entry[:-2] == list(sq_entry)[:-2]


if __name__ == "__main__":
    unittest.main()
