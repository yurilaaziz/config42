import os

from config42.handlers import ConfigHandlerBase


class FileHandlerBase(ConfigHandlerBase):
    def __init__(self, path, **kwargs):
        super().__init__()
        self.path = path
        try:
            config = self.load()
        except Exception:
            config = None
        self.config = config if config is not None else {}

    def destroy(self):
        """
            remove persistent configuration file.
            :rtype: bool (success)
        """
        try:
            os.remove(self.path)
            return True
        except FileNotFoundError:
            return False
