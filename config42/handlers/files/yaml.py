try:
    import yaml
except ImportError:
    raise ImportError("files.Yaml handler requires 'PyYAML' package\n"
                      "Install it with 'pip install pyyaml'")

from .base import FileHandlerBase


class YamlHandler(FileHandlerBase):
    def load(self):
        with open(self._path, "r") as f:
            return yaml.load(f)

    def dump(self):
        with open(self._path, "w") as f:
            yaml.dump(self._config, f)
        return True
