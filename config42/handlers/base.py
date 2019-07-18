class ConfigHandlerBase:

    def __init__(self):
        """
            Initialize the handler data store.
        """
        self.config = {}
        self.updated = False

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
        self.config = {}
        self.updated = True
        return True

    def destroy(self):
        """
            destroys persistent configuration. configuration is removed from disk or database
            :rtype: bool (success)
        """
        raise NotImplementedError
