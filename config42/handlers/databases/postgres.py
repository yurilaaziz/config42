try:
    import psycopg2
except ImportError:
    raise ImportError("databases.PostgreSQL handler needs package 'psycopg2-binary'\n"
                      "Install it with 'pip install psycopg2-binary'")

from . import DatabaseHandler


class PostgreSQL(DatabaseHandler):
    @property
    def values_sql_format(self):
        return "(%s, %s)"

    def _connect(self):
        return psycopg2.connect(**self.cnx_info)
