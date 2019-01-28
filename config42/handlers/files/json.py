import json

from . import FileHandler


class Json(FileHandler):
    def load(self):
        with open(self._file_path, "r") as f:
            return json.load(f)

    def dump(self):
        with open(self._file_path, "w") as f:
            json.dump(self._config, f)
        return True
