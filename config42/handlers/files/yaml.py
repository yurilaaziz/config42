try:
    import yaml
except ImportError:
    raise ImportError("files.Yaml handler requires 'PyYAML' package\n"
                      "Install it with 'pip install pyyaml'")

from .base import FileHandlerBase


class YamlHandler(FileHandlerBase):
    def load(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def dump(self):
        with open(self.path, "w", encoding=self.encoding) as f:
            yaml.dump(self.config, f)
        return True
