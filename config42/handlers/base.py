class ConfigHandlerBase:

    def __init__(self):
        """
            Initialize the handler data store.
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
            rest self._updated flag to False
            self._updated = False
            :rtype: bool (success)
        """
        raise NotImplementedError

    def flush(self):
        """
            flush in memory configuration.
            :rtype: bool (success)
        """
        self._config = {}
        self._updated = True
        return True

    def destroy(self):
        """
            destroys persistent configuration. configuration is removed from disk or database
            :rtype: bool (success)
        """
        raise NotImplementedError

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
