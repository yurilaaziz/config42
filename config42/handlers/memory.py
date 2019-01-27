from . import ConfigHandlerBase

class Memory(ConfigHandlerBase):
    def load(self):
        """
            As it is stored in memory, returns current configuration dict.
            :rtype: dict
        """
        return self._config

    def dump(self):
        """
            As it is stored in memory, returns True.
            :rtype: bool (success)
        """
        return True