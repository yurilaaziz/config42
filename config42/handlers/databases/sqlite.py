import sqlite3

from config42.handlers.databases.handler import DatabaseHandler


class SQLite(DatabaseHandler):
    @property
    def table_columns(self):
        return "(%s INTEGER PRIMARY KEY, %s TEXT, %s TEXT)" % (self.id_col, self.key_col,
                                                               self.value_col)

    @property
    def values_sql_format(self):
        return "(?, ?)"

    def _connect(self):
        return sqlite3.connect(**self.cnx_info)
