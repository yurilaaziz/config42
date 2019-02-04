from config42 import flat_set
from config42.handlers import ConfigHandler
from config42.utils import coerce_str, flat_items

try:
    from etcd import Client
except ImportError:
    raise ImportError("Etcd handler requires 'python-etcd' package\n"
                      "Install it with 'pip install python-etcd'")


class Etcd(ConfigHandler):
    def __init__(self, *, keyspace="/config", value_coercion=True, **client_info):
        """
            Initialize the handler data store.
            :param keyspace: etcd keyspace for configuration map starting with /
            :type keyspace: string
            :param client_info: generic params forwarded from the Configmanager
        """
        super().__init__()
        self.keyspace = keyspace + ("/" if not keyspace[-1] == "/" else "")
        self.value_coercion = value_coercion
        self.client = Client(**client_info)

    def create(self):
        self.client.write(self.keyspace, None, dir=True)

    def load(self):
        cfg = {}
        for leaf in self.client.read(self.keyspace, recursive=True).leaves:
            key = leaf.key[len(self.keyspace):]
            value = coerce_str(leaf.value) if self.value_coercion else leaf.value
            flat_set(cfg, key, value, "/")
        return cfg

    def dump(self, cfg):
        for key, value in flat_items(cfg, sep="/"):
            self.client.set(self.keyspace + key, str(value))

    def destroy(self):
        self.client.delete(self.keyspace, recursive=True, dir=True)
