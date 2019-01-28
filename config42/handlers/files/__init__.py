from .. import ConfigHandlerBase


class FileHandler(ConfigHandlerBase):
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
