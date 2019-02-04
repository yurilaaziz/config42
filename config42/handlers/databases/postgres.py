from config42.handlers.databases.handler import DatabaseHandler

try:
    import psycopg2
except ImportError:
    raise ImportError("databases.PostgreSQL handler needs package 'psycopg2-binary'\n"
                      "Install it with 'pip install psycopg2-binary'")


class PostgreSQL(DatabaseHandler):
    @property
    def table_columns(self):
        return "(%s SERIAL PRIMARY KEY, %s TEXT, %s TEXT)" % (self.id_col, self.key_col,
                                                              self.value_col)

    @property
    def values_sql_format(self):
        return "(%s, %s)"

    def _connect(self):
        return psycopg2.connect(**self.cnx_info)
