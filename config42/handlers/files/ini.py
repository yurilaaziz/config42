from configparser import ConfigParser

from .base import FileHandlerBase


class IniHandler(FileHandlerBase):
    def load(self):
        cfg = ConfigParser()
        file_read = cfg.read(self.path)
        if not file_read:
            raise Exception("An error occurred while trying to read INI file '" +
                            self.path + "'")
        return {s: dict(cfg.items(s)) for s in cfg.sections()}

    def dump(self):
        cfg = ConfigParser()
        for key, value in self.config.items():
            if not isinstance(value, dict):
                raise AttributeError(
                    "INI configuration do not support nesting. section {} should contain dict".format(key))

        cfg.read_dict(self.config)
        with open(self.path, "w") as f:
            cfg.write(f)
        return True
