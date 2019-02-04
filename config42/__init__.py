from config42.handlers.defaults import Defaults
from config42.utils import flat_del, flat_get, flat_merge, flat_set


class ConfigManager:
    """
    Manages a "configuration" represented by a nested dict/list.
    Access can be made by using dot-separated keys (like "hosts.3.name").
    Read/write action from different sources are handled by manager's "handler(s)".
    """

    def __init__(self, handler=None, sep=".", *, defaults=None, autoload=True,
                 load_handlers=None, dump_handlers=None):
        """
        :param handler: Unique handler for reading/writing configuration
        :param sep: separator of keys for value access
        :param defaults: defaults configuration
        :param autoload: if the configuration is load from handler(s) at the init step
        :param load_handlers: when 'handler' is None, reader handlers listed by priority;
        values will first be searched in the first handler then in the next ones.
        :param dump_handlers: when 'handler' is None, writer handlers
        """
        if handler is not None:
            load_handlers = [handler]
            dump_handlers = [handler]
        if defaults is not None:
            if load_handlers is None:
                load_handlers = []
            load_handlers += [Defaults(defaults)]
        self._load_handlers = load_handlers if load_handlers is not None else []
        self._dump_handlers = dump_handlers if dump_handlers is not None else []
        self._updated = False
        self.cfg = None
        self.sep = sep
        if autoload:
            self.load()

    def create(self, loader=True, dumper=True):
        """
        Creates the source to a configuration for load/dump handlers (for example,
        with a relational database handler, create the configuration table)
        :param loader: if the creation is done for reader handler(s)
        :param dumper: if the creation is done for writer handler(s)
        """
        handlers = set()
        if loader:
            handlers |= set(self._load_handlers)
        if dumper:
            handlers |= set(self._dump_handlers)
        for h in handlers:
            h.create()

    def load(self):
        """
        Loads the configuration from the sources by the handler(s)
        """
        self.cfg = flat_merge({}, *(h.load() for h in reversed(self._load_handlers)))
        self._updated = False

    def dump(self, *, if_updated=False):
        """
        Dumps the configuration to the sources by the handler(s)
        :param if_updated: dumps only if the configuration has been updated since the
        last load
        """
        if not if_updated or self._updated:
            for handler in self._dump_handlers:
                handler.dump(self.cfg)
            self._updated = False

    def destroy(self, loader=True, dumper=True):
        """
        Destroy the configuration source for load/dump handlers (for example,
        with a relational database handler, destroy the configuration table)
        :param loader: if the creation is done for reader handler(s)
        :param dumper: if the creation is done for writer handler(s)
        """
        handlers = set()
        if loader:
            handlers |= set(self._load_handlers)
        if dumper:
            handlers |= set(self._dump_handlers)
        for h in handlers:
            h.destroy()

    def __getitem__(self, item):
        return flat_get(self.cfg, item, self.sep)

    def __setitem__(self, key, value):
        self._updated = self._updated or flat_set(self.cfg, key, value, self.sep)

    def __delitem__(self, key):
        self._updated = self._updated or flat_del(self.cfg, key, self.sep)
