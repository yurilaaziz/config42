from .ini import IniHandler
from .json import JsonHandler
from .yaml import YamlHandler


class FileHandler(object):
    def __new__(cls, *, path, extension=None, **kwargs):
        """
            :param path: path of the config file
        """
        handler_map = {
            'yaml': YamlHandler,
            'yml': YamlHandler,
            'json': JsonHandler,
            'ini': IniHandler
        }
        path = path.lower()
        if not extension:
            extension = path.split('.')[-1]

        if handler_map.get(extension):
            return handler_map.get(extension)(path=path, **kwargs)
        else:
            raise NotImplementedError("Only {} extensions are supported".format(", ".join(handler_map.keys())))
