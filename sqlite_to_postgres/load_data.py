import os
import sqlite3
import logging

import psycopg2
from dotenv import load_dotenv
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_extractor import SQLiteExtractor
from tables_dataclasses import (FilmWork, Genre, GenreFilmWork, Person,
                                PersonFilmWork)
from contextlib import contextmanager


@contextmanager
def open_db(file_name: str):
    conn = sqlite3.connect(file_name)
    try:
        logging.info("Подключено.")
        yield conn
    finally:
        logging.info("Соединение закрыто.")
        conn.commit()
        conn.close()


def load_from_sqlite(
    connection: sqlite3.Connection, pg_conn: _connection, size: int
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, "content")
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver.truncate_all_tables(tables)  # ОСТОРОЖНО! Очищает базу.
    for table in tables.keys():
        select = sqlite_extractor.select_data_from_table(table)
        while table_data := (
            sqlite_extractor.fetchmany_from_request(
                request=select, size=size, dataclass=tables[table]
            )
        ):
            postgres_saver.insert_data(table, table_data)
    print("Данные были перегружены с SQLite в Postgres")


if __name__ == "__main__":
    load_dotenv()
    tables = {}
    tables["genre"] = Genre
    tables["person"] = Person
    tables["film_work"] = FilmWork
    tables["genre_film_work"] = GenreFilmWork
    tables["person_film_work"] = PersonFilmWork
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": "127.0.0.1",
        "port": 5432,
    }
    sqlite_path = "new_admin_panel_sprint_1/sqlite_to_postgres/db.sqlite"
    size = int(os.environ.get("SIZE", default=10))
    with open_db(sqlite_path) as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, size)
