from config42.handlers.databases.handler import DatabaseHandler

try:
    import mysql.connector
except ImportError:
    raise ImportError("MySQL handler needs package 'mysql-connector'\n"
                      "Install it with 'pip install mysql-connector'")


class MySQL(DatabaseHandler):
    @property
    def table_columns(self):
        return "(%s SERIAL PRIMARY KEY, %s TEXT, %s TEXT)" % (self.id_col, self.key_col,
                                                              self.value_col)

    @property
    def values_sql_format(self):
        return "(%s, %s)"

    def _connect(self):
        return mysql.connector.connect(**self.cnx_info)
