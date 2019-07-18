import json

from .base import FileHandlerBase


class JsonHandler(FileHandlerBase):
    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def dump(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f)
        return True
