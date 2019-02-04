from config42.handlers import ConfigHandler
from config42.utils import coerce_str, flat_items, flat_set


class DatabaseHandler(ConfigHandler):
    def __init__(self, *, table="config", key_col="key", value_col="value", id_col="id",
                 sep=".", value_coercion=True, **cnx_info):
        """
        :param table: table containing configuration
        :param key_col: column of the table containing dot-separated keys
        :param value_col: column of the table containing the value
        :param cnx_info: connection info, maybe depending on database connector (host,
        port, user, password, database, etc.)
        """
        super().__init__()
        self.cnx_info = cnx_info
        self.table = table
        self.key_col = key_col
        self.value_col = value_col
        self.id_col = id_col
        self.sep = sep
        self.value_coercion = value_coercion

    MIXED_KEYS_ERROR = "'%s' mixes array and dict value"

    @property
    def table_columns(self):
        raise NotImplementedError

    @property
    def create_sql(self):
        return "CREATE TABLE %s %s" % (self.table, self.table_columns)

    @property
    def select_sql(self):
        return "SELECT %s, %s FROM %s" % (self.key_col, self.value_col, self.table)

    @property
    def delete_sql(self):
        return "DELETE FROM %s" % self.table

    @property
    def values_sql_format(self):
        """
        :return: formatting of values in sql insert query, depending on the database
        connector
        """
        raise NotImplementedError

    @property
    def insert_sql(self):
        return "INSERT INTO %s (%s, %s) VALUES %s" % \
               (self.table, self.key_col, self.value_col, self.values_sql_format)

    @property
    def drop_sql(self):
        return "DROP TABLE %s" % self.table

    def _connect(self):
        """
        :return: a connection to the database, using self.cnx_info
        """
        raise NotImplementedError

    def _create(self):
        cnx = self._connect()
        try:
            cursor = cnx.cursor()
            cursor.execute(self.create_sql)
            cnx.commit()
            cursor.close()
        finally:
            if cnx:
                cnx.close()

    def _query(self):
        """
        :return: an iterator on table configuration rows
        """
        cnx = self._connect()
        try:
            cursor = cnx.cursor()
            cursor.execute(self.select_sql)
            yield from cursor.fetchall()
            cursor.close()
        finally:
            if cnx:
                cnx.close()

    def _delete_insert(self, values):
        """
        replace table content with values
        :param values: rows to write in table
        """
        cnx = self._connect()
        try:
            cursor = cnx.cursor()
            cursor.execute(self.delete_sql)
            cursor.executemany(self.insert_sql, values)
            cnx.commit()
            cursor.close()
        finally:
            if cnx:
                cnx.close()

    def _drop(self):
        cnx = self._connect()
        try:
            cursor = cnx.cursor()
            cursor.execute(self.drop_sql)
            cnx.commit()
            cursor.close()
        finally:
            if cnx:
                cnx.close()

    def create(self):
        self._create()

    def load(self):
        cfg = {}
        for key, value in self._query():
            if self.value_coercion:
                value = coerce_str(value)
            flat_set(cfg, key, value, self.sep)
        return cfg

    def dump(self, cfg):
        self._delete_insert(flat_items(cfg, self.sep))

    def destroy(self):
        self._drop()
