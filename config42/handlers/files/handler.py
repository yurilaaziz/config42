import os

from config42.handlers import ConfigHandler


class FileHandler(ConfigHandler):
    def __init__(self, *, path):
        """
        :param path: path of the config file
        """
        super().__init__()
        self._path = path

    def create(self):
        basedir = os.path.dirname(self._path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        self.dump({})

    def destroy(self):
        if os.path.exists(self._path):
            os.remove(self._path)
