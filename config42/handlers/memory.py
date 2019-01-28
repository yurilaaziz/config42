from . import ConfigHandlerBase

class Memory(ConfigHandlerBase):
    def load(self):
        """
            As it is stored in memory, returns current configuration dict.
            :rtype: dict
        """
        return self._config
