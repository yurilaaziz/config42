import collections

import etcd

from . import ConfigHandlerBase


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
        self.client = etcd.Client(**kwargs)
        self.keyspace = keyspace if keyspace else '/config'

    def load(self):
        """
            Load all configuration key values from the Etcd data store. Returns a nested dict.
            :rtype: dict
        """
        try:
            directory = self.client.read(self.keyspace, recursive=True)
            return self.recursive(directory, prefix=self.keyspace)
        except etcd.EtcdKeyNotFound:
            return {}

    def dump(self):
        """
            Serialize and store the configuration key, values to the Etcd data store.
            :rtype: bool (success)
        """
        # Reset this flag to False, to respect the concept
        flat_dict = self.flatten(self._config,parent_key=self.keyspace, seperator='/')
        for key, value in flat_dict.items():
            self.client.set(key, value)
        self._updated = False
        return True

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
            new_key = parent_key + seperator + key if parent_key else key
            if isinstance(value, collections.MutableMapping):
                items.extend(self.flatten(value, parent_key=new_key, seperator=seperator).items())
            else:
                items.append((new_key, value))
        return dict(items)
