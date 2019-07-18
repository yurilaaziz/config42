import os

from config42 import ConfigManager
from config42.handlers.memory import Memory


class Environment(Memory):
    def __init__(self, prefix, **kwargs):
        """
            Initialize the handler data store.
            :param prefix: environment prefix for configuration map
            :type key: string
        """
        super().__init__()
        configmanager = ConfigManager()
        for key, value in os.environ.items():
            if key.startswith(prefix + "_"):
                configmanager.set(
                    key.replace(prefix + "_", "").replace("_", ".").lower(),
                    value)

        self.in_memory_config = configmanager.as_dict()
        self.config = self.in_memory_config
