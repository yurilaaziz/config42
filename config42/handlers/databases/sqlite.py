import sqlite3

from . import DatabaseHandler


class SQLite(DatabaseHandler):
    @property
    def values_sql_format(self):
        return "(?, ?)"

    def _connect(self):
        return sqlite3.connect(**self.cnx_info)
