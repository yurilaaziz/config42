import os

from config42.handlers import ConfigHandlerBase


class FileHandlerBase(ConfigHandlerBase):
    def __init__(self, *, path):
        super().__init__()
        self._path = path
        try:
            config = self.load()
        except Exception:
            config = None
        self._config = config if config is not None else {}

    def destroy(self):
        """
            remove persistent configuration file.
            :rtype: bool (success)
        """
        os.remove(self._path)
        return True
