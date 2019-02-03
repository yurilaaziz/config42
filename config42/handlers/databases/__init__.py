from .. import ConfigHandlerBase


class DatabaseHandler(ConfigHandlerBase):
    def __init__(self, *, table, key_col="key", value_col="value", **cnx_info):
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

    MIXED_KEYS_ERROR = "'%s' mixes array and dict value"

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

    def _connect(self):
        """
        :return: a connection to the database, using self.cnx_info
        """
        raise NotImplementedError

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

    @staticmethod
    def _rec_config_build(keys, value, cfg, index=0):
        """
        :param keys: key list contains in key_col
        :param value: value
        :param cfg: current config at index
        :param index: index of current key in key list iteration
        :return: config tree build from keys
        """
        if index == len(keys):
            return value
        key = keys[index]
        if key.isnumeric():
            key = int(key)
            if not cfg:
                cfg = [None] * (key + 1)
            elif not isinstance(cfg, list):
                raise TypeError(DatabaseHandler.MIXED_KEYS_ERROR % ".".join(keys[:index]))
            else:
                cfg += [None] * (key + 1 - len(cfg))
            next_cfg = cfg[key]
        else:
            if not cfg:
                cfg = {key: None}
            elif not isinstance(cfg, dict):
                raise TypeError(DatabaseHandler.MIXED_KEYS_ERROR % ".".join(keys[:index]))
            next_cfg = cfg.get(key, None)
        cfg[key] = DatabaseHandler._rec_config_build(keys, value, next_cfg, index + 1)
        return cfg

    def load(self):
        config = {}
        for key, value in self._query():
            config = DatabaseHandler._rec_config_build(key.split('.'), value, config)
        return config

    @staticmethod
    def _rec_config_flat(cfg):
        """
        :param cfg: config tree to flat
        :return: iterator on flatten config rows with dot-separated keys
        """
        if isinstance(cfg, dict):
            items = cfg.items()
        elif isinstance(cfg, list):
            items = enumerate(cfg)
        else:
            yield ([], cfg)
            return
        for key, value in items:
            for keys, final_value in DatabaseHandler._rec_config_flat(value):
                yield ([str(key)] + keys, final_value)

    def dump(self):
        values = [(".".join(keys), value)
                  for keys, value in DatabaseHandler._rec_config_flat(self._config)]
        self._delete_insert(values)
        return True
