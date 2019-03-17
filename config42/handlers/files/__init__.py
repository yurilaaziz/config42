class FileHandler(object):
    def __new__(cls, *, path, extension=None, **kwargs):
        """
            :param path: path of the config file
        """

        path = path.lower()
        if not extension:
            extension = path.split('.')[-1]

        if extension.lower() in ("yaml", "yml"):
            from .yaml import YamlHandler as Handler
        elif extension.lower() == "json":
            from .json import JsonHandler as Handler
        elif extension.lower() == "ini":
            from .ini import IniHandler as Handler
        else:
            raise NotImplementedError("Only yaml, json, ini extensions are supported")

        return Handler(path=path, **kwargs)
