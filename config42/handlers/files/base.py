from config42.handlers import ConfigHandlerBase
import os


class FileHandlerBase(ConfigHandlerBase):
    def __init__(self, *, path):
        super().__init__()
        self._path = path

    def destroy(self):
        """
            remove persistent configuration file.
            :rtype: bool (success)
        """
        os.remove(self._path)
        return True