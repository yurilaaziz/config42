from .. import ConfigHandlerBase


class FileHandler(ConfigHandlerBase):
    def __init__(self, *, path):
        """
            :param path: path of the config file
        """
        super().__init__()
        self._path = path
