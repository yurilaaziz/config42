try:
    from ruamel.yaml import YAML
except ImportError:
    raise ImportError("files.Yaml handler requires 'ruamel.yaml' package\n"
                      "Install it with 'pip install ruamel.yaml'")

from .base import FileHandlerBase


class YamlHandler(FileHandlerBase):
    def load(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            return YAML().load(f)

    def dump(self):
        with open(self.path, "w", encoding=self.encoding) as f:
            YAML().dump(self.config, f)
        return True
