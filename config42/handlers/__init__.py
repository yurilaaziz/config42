import logging

LOGGER = logging.getLogger('config-manger')
LOGGER.addHandler(logging.NullHandler())


class ConfigHandlerBase:

    def __init__(self, **kwargs):
        """
            Initialize the handler data store.
            :param kwargs: generic params forwarded from the Configmanager
            :type key: dict
        """
        self._config = {}
        self._updated = False

    def load(self):
        """
            Load all configuration key values from the data store. Returns a nested dict.
            :rtype: dict
        """
        return {}

    def dump(self):
        """
            Serialize and store the configuration key, values to the data store.
            :rtype: bool (success)
        """
        # Reset this flag to False, to respect the concept
        self._updated = False
        return True

    def flush(self):
        """
            flush in memory configuration.
            :rtype: bool (success)
        """
        self._config = {}
        return True

    def as_dict(self):
        """
            Serialize the current configuration key, values.
            :rtype: dict
        """
        if self._updated:
            # Listen to yourself
            # Always read from the data store
            self.dump()
            self._config = self.load()
        return self._config
