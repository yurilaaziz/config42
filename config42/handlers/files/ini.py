from configparser import ConfigParser

from config42.handlers.files.handler import FileHandler


class Ini(FileHandler):
    def load(self):
        cfg_parser = ConfigParser()
        file_read = cfg_parser.read(self._path)
        if not file_read:
            raise IOError("An error occured while trying to read INI file '" +
                          self._path + "'")
        return {s: dict(cfg_parser.items(s)) for s in cfg_parser.sections()}

    def dump(self, cfg):
        cfg_parser = ConfigParser()
        cfg_parser.read_dict(cfg)
        with open(self._path, "w") as f:
            cfg_parser.write(f)
