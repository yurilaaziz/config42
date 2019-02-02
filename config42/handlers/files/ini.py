from configparser import ConfigParser

from .base  import FileHandlerBase

class IniHandler(FileHandlerBase):
    def load(self):
        cfg = ConfigParser()
        file_read = cfg.read(self._path)
        if not file_read:
            raise IOError("An error occured while trying to read INI file '" +
                          self._path + "'")
        return {s: dict(cfg.items(s)) for s in cfg.sections()}

    def dump(self):
        cfg = ConfigParser()
        cfg.read_dict(self._config)
        with open(self._path, "w") as f:
            cfg.write(f)
        return True
