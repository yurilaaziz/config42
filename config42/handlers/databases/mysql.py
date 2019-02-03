try:
    import mysql.connector
except ImportError:
    raise ImportError("MySQL handler needs package 'mysql-connector'\n"
                      "Install it with 'pip install mysql-connector'")

from . import DatabaseHandler


class MySQL(DatabaseHandler):
    @property
    def values_sql_format(self):
        return "(%s, %s)"

    def _connect(self):
        return mysql.connector.connect(**self.cnx_info)
