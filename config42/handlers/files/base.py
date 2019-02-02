from config42.handlers import ConfigHandlerBase


class FileHandlerBase(ConfigHandlerBase):
    def __init__(self, *, path):
        super().__init__()
        self._path = path
