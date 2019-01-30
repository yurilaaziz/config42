from .. import ConfigHandlerBase


class DatabaseHandler(ConfigHandlerBase):
    def __init__(self, *, table, key_col="key", value_col="value", **cnx_info):
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
        raise NotImplemented

    @property
    def insert_sql(self):
        return "INSERT INTO %s (%s, %s) VALUES %s" % \
               (self.table, self.key_col, self.value_col, self.values_sql_format)

    def _connect(self):
        raise NotImplemented

    def _query(self):
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
    def _rec_load(keys, value, cfg, index=0):
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
        cfg[key] = DatabaseHandler._rec_load(keys, value, next_cfg, index + 1)
        return cfg

    def load(self):
        config = {}
        for key, value in self._query():
            config = DatabaseHandler._rec_load(key.split('.'), value, config)
        return config

    @staticmethod
    def _rec_dump(cfg):
        if isinstance(cfg, dict):
            items = cfg.items()
        elif isinstance(cfg, list):
            items = enumerate(cfg)
        else:
            yield ([], cfg)
            return
        for key, value in items:
            for keys, final_value in DatabaseHandler._rec_dump(value):
                yield ([str(key)] + keys, final_value)

    def dump(self):
        values = [(".".join(keys), value)
                  for keys, value in DatabaseHandler._rec_dump(self._config)]
        self._delete_insert(values)
        return True
