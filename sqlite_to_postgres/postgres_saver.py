import logging
from dataclasses import dataclass

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch


class PostgresSaver:
    def __init__(self, conn: _connection, schema_name) -> None:
        self.conn = conn
        self.schema_name = schema_name

    def truncate_table(self, table_name: str) -> None:
        try:
            cur = self.conn.cursor()
            cur.execute(
                "TRUNCATE {0}.{1} CASCADE;".format(
                    self.schema_name, table_name
                )
            )
            logging.info("Таблица {0} очищена.".format(table_name))
        except Exception as err:
            logging.error(
                "Ошибка при очистки таблицы: {0}"
                "\n{1}".format(table_name, err)
            )

    def truncate_all_tables(self, tables) -> None:
        for table in tables:
            self.truncate_table(table)
        logging.info("Таблицы очищены.")

    def insert_data(self, table_name: str, data: dataclass):
        try:
            cur = self.conn.cursor()
            entries = []
            for entry in data:
                args = []
                for arg in entry.__dict__:
                    args.append(entry.__dict__[arg])
                entries.append(args)
            fields_amount = "%s, " * len(entries[0])
            fields_amount = fields_amount[:-2]
            execute_batch(
                cur,
                """
                INSERT INTO {0}.{1} VALUES({2})
                """.format(
                    self.schema_name,
                    table_name,
                    fields_amount,
                ),
                entries,
            )
        except Exception as err:
            logging.error(
                "Ошибка при вставки данных в таблицу: "
                "{0}.\n{1}".format(table_name, err)
            )
            return
