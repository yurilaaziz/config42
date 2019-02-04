from config42.handlers.files.handler import FileHandler

try:
    import yaml
except ImportError:
    raise ImportError("files.Yaml handler requires 'PyYAML' package\n"
                      "Install it with 'pip install pyyaml'")


class Yaml(FileHandler):
    def load(self):
        with open(self._path, "r") as f:
            return yaml.load(f)

    def dump(self, cfg):
        with open(self._path, "w") as f:
            yaml.dump(cfg, f)
