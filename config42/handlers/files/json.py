import json

from .base import FileHandlerBase


class JsonHandler(FileHandlerBase):
    def load(self):
        with open(self._path, "r") as f:
            return json.load(f)

    def dump(self):
        with open(self._path, "w") as f:
            json.dump(self._config, f)
        return True
