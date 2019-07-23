from config42.handlers.base import ConfigHandlerBase
from config42.utils import flatten, recursive

try:
    from etcd import Client, EtcdKeyNotFound, EtcdNotDir
except ImportError:
    raise ImportError("Please install python-etcd package")


class Etcd(ConfigHandlerBase):
    def __init__(self, keyspace=None, **kwargs):
        """
            Initialize the handler data store.
            :param keyspace: etcd keyspace for configuration map starting with /
            :type key: string
            :param kwargs: generic params forwarded from the Configmanager
            :type key: dict
        """
        super().__init__()
        self.client = Client(**kwargs)
        self.keyspace = keyspace if keyspace else '/config'
        if not self.keyspace.startswith('/'):
            self.keyspace = '/' + self.keyspace
        self.config = self.load()

    def load(self):
        """
            Load all configuration key values from the Etcd data store. Returns a nested dict.
            :rtype: dict
        """
        try:
            directory = self.client.read(self.keyspace, recursive=True)
            items = {}
            for item in directory.leaves:
                recursive(item.key.replace(self.keyspace + '/', '').replace('/', '.'), items, item.value,
                          update=True)
            return items
        except EtcdKeyNotFound:
            return {}

    def dump(self):
        """
            Serialize and store the configuration key, values to the Etcd data store.
            :rtype: bool (success)
        """
        flat_dict = flatten(self.config, parent_key=self.keyspace, separator='/')
        for key, value in flat_dict.items():
            try:
                self.client.set(key, value)
            except EtcdNotDir as exc:
                directory_not_created = exc.payload['cause']
                self.client.write(directory_not_created, None, dir=True)
                self.client.set(key, value)
        self.updated = False
        return True

    def destroy(self):
        """
            destroys given keyspace in etcd
            :rtype: bool (success)
        """
        try:
            self.client.delete(self.keyspace, recursive=True, dir=True)
            return True
        except EtcdKeyNotFound:
            return False
