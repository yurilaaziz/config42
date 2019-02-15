from config42.handlers import ConfigHandlerBase

try:
    from etcd import Client, EtcdKeyNotFound
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
        self._config = self.load()

    def load(self):
        """
            Load all configuration key values from the Etcd data store. Returns a nested dict.
            :rtype: dict
        """
        try:
            directory = self.client.read(self.keyspace, recursive=True)
            return self.recursive(directory, prefix=self.keyspace)
        except EtcdKeyNotFound:
            return {}

    def dump(self):
        """
            Serialize and store the configuration key, values to the Etcd data store.
            :rtype: bool (success)
        """
        flat_dict = self.flatten(self._config, parent_key=self.keyspace, seperator='/')
        for key, value in flat_dict.items():
            self.client.set(key, value)
        self._updated = False
        return True

    def destroy(self):
        """
            destroys given keyspace in etcd
            :rtype: bool (success)
        """
        try:
            self.client.delete(self.keyspace, recursive=True, dir=True)
            return True
        except KeyError:
            return False

    def recursive(self, directory, prefix='', seperator='/'):
        items = {}
        for item in directory.leaves:
            if item.dir:
                items.update(self.recursive(item), prefix=item.key, seperator=seperator)
            else:
                items[item.key.replace(prefix, '').replace(seperator, '')] = item.value
        return dict(items)

    def flatten(self, dict_, parent_key='', seperator='/'):
        items = []
        for key, value in dict_.items():
            new_key = (parent_key + seperator + key) if parent_key else key
            if isinstance(value, dict):
                items.extend(self.flatten(value, parent_key=new_key, seperator=seperator).items())
            else:
                items.append((new_key, value))
        return dict(items)
