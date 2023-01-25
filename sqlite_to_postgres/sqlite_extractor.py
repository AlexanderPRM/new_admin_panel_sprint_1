import dataclasses
import logging
import sqlite3


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.cur = conn.cursor()

    def select_data_from_table(self, table_name: str):
        try:
            request = self.cur.execute(
                """SELECT * FROM {0}""".format(table_name)
            )
        except Exception as err:
            logging.error(
                "Произошла ошибка во время "
                "запроса данных из таблицы: "
                "{0}\nОшибка: {1}".format(table_name, err)
            )
        return request

    def fetchmany_from_request(
        self, request: sqlite3.Cursor, size: int, dataclass: dataclasses
    ):
        try:
            data = []
            for entry in request.fetchmany(size=size):
                data.append(dataclass(*entry))
            return data
        except Exception as err:
            logging.error(
                "Произошла ошибка во время извлечения данных\n"
                "Ошибка: {0}".format(err)
            )
