import yaml

from . import FileHandler


class Yaml(FileHandler):
    def load(self):
        with open(self._file_path, "r") as f:
            return yaml.load(f)

    def dump(self):
        with open(self._file_path, "w") as f:
            yaml.dump(self._config, f)
        return True
