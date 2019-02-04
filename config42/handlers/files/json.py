import json

from config42.handlers.files.handler import FileHandler


class Json(FileHandler):
    def load(self):
        with open(self._path, "r") as f:
            return json.load(f)

    def dump(self, cfg):
        with open(self._path, "w") as f:
            json.dump(cfg, f)
