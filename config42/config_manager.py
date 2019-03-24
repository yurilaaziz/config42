from config42.init_apps import InitApp


class ConfigManager:
    def __init__(self, application=None, defaults=None, handler=None, **handler_kwargs):
        self.defaults = defaults if defaults else {}
        # Implicit load of handlers
        if handler_kwargs.get('path'):
            from config42.handlers.files import FileHandler
            handler = FileHandler
        elif handler_kwargs.get('keyspace'):
            from config42.handlers.etcd import Etcd
            handler = Etcd
        elif handler_kwargs.get('prefix'):
            from config42.handlers.environment import Environment
            handler = Environment
        if not handler:
            from config42.handlers.memory import Memory
            handler = Memory
        self.handler = handler(**handler_kwargs)

        if application:
            self.init_app(application)

    def get_defaults(self, key):
        return self.recursive(key, obj=self.defaults)

    def recursive(self, key, obj, value=None):
        _keys = key.split('.')
        assert len(_keys) > 0

        if isinstance(obj, list):
            _base = int(_keys[0])
        else:
            _base = _keys[0]

        if isinstance(obj, dict) and _base not in obj and not value:
            return None
        if isinstance(obj, list) and _base >= len(obj) and not value:
            return None
        elif isinstance(obj, list) and value:
            raise AttributeError("Insertion in list is not allowed")

        if len(_keys) == 1:
            if value:
                obj[_base] = value
            return obj[_base]
        else:
            if isinstance(obj, dict) and _base not in obj:
                obj[_base] = dict()

            return self.recursive('.'.join(_keys[1:]), obj[_base], value)

    def get(self, key):
        """
            Gets config value for a given key from the data store. Returns the value that matches the supplied key.
            If the value is not set, a default value will be returned as set by set_defaults.
            :param key: The configuration key to return a config value for
            :type key: str
            :rtype: Any supported (str, int, bool, list-of-supported-types)
        """
        value = self.recursive(key, obj=self.handler.as_dict())
        return value if value is not None else self.get_defaults(key)

    def set(self, key, value, trigger_commit=True):
        """
            Sets config value for a given key in the data store.
            :param key: The configuration key to set
            :type key: str
            :param value: The value to set the configuration key to
            :type value: Any supported (str, int, bool, list-of-supported-types)
            :param trigger_commit: Flag whether to trigger a config commit after all values are set.
            :type trigger_commit: bool
            :rtype: bool (success)
        """
        if self.recursive(key, obj=self.handler._config) == value:
            return False  # Not updating

        self.recursive(key, obj=self.handler._config, value=value)
        self.handler._updated = True
        if trigger_commit:
            self.commit()

        return self.handler._updated

    def replace(self, config, trigger_commit=True):
        """
        Completely reset the config with a set of key values.
        It is the equivalent of unsetting all keys, followed by a
        set_many. Anything not in the supplied config will revert to default.
        :param config: A dictionary of keys and values to set as defaults
        :type config: dict
        :param trigger_commit: Flag whether to trigger a config commit after all values are set.
        :type trigger_commit: bool
        """
        self.handler.flush()
        self.set_many(config, trigger_commit)

    def set_many(self, config, trigger_commit=True):
        """
        Sets the value of multiple config settings simultaneously.
        This postpones the
        triggering of the commit signal after all values are set.
        :param config: A dictionary of keys and values to set.
        :type key: dict
        :param trigger_commit: Flag whether to trigger a config commit after all values are set.
        :type trigger_commit: bool
        """
        has_been_updated = False
        for key, value in config.items():
            updated = self.set(key, value, trigger_commit=False)
            has_been_updated = has_been_updated or updated

        if has_been_updated and trigger_commit:
            self.commit()

    def commit(self):
        return self.handler.dump()

    def init_app(self, app):
        return InitApp.init_app(self.handler.as_dict(), app)

    def as_dict(self):
        return self.handler.as_dict()
