from config42.handlers.base import ConfigHandlerBase


class Memory(ConfigHandlerBase):
    def __init__(self, **kwargs):
        """
            Initializes the handler data store.
            :param kwargs: generic params forwarded from the Configmanager
            :type key: dict
        """
        super().__init__()
        self.in_memory_config = {}
        self.config = {}

    def load(self):
        """
            As it is stored in memory, returns the last committed dict.
            :rtype: dict
        """
        return self.in_memory_config

    def dump(self):
        """
            Affects current configuration .
            :rtype: bool (success)
        """
        self.in_memory_config = self.config
        self.updated = False
        return True

    def destroy(self):
        """
            Destroys the committed configuration
            :rtype: bool (success)
        """
        self.in_memory_config = {}
        return True
