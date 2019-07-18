class FileHandler(object):
    def __new__(cls, *, path, extension=None, **kwargs):
        """
            :param path: path of the config file
        """

        path = path.lower()
        if not extension and len(path.split('.')) > 1:
            extension = path.split('.')[-1]
        else:
            extension = ""

        if extension.lower() in ("yaml", "yml"):
            from config42.handlers.files.yaml import YamlHandler as Handler
        elif extension.lower() == "json":
            from config42.handlers.files.json import JsonHandler as Handler
        elif extension.lower() == "ini":
            from config42.handlers.files.ini import IniHandler as Handler
        else:
            from config42.handlers.raw import RawHandler as Handler

        return Handler(path=path, **kwargs)
