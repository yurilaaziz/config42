import argparse

from config42 import ConfigManager
from config42.handlers.memory import Memory


class ArgParse(Memory):
    def __init__(self, schema, argv=None, **argparge_kwargs):
        """
            Initialize the argparse handler.
            Retrieve parameters from command line arguments
        """
        super().__init__()
        # Validate with cerberus
        # validator = Validate(schema) :

        parser = argparse.ArgumentParser(**argparge_kwargs)

        for item in schema:
            flags_name = item.get('source', {}).get('argv', ['--' + item['key']])
            if flags_name:
                parser.add_argument(*flags_name,
                                    type=item.get('type'),
                                    choices=item.get('choices'),
                                    help=item.get('description'),
                                    metavar=item.get('name'),
                                    dest=item.get('key'))

        args = parser.parse_args(argv)
        configmanager = ConfigManager()
        configmanager.set_many(vars(args))

        self.in_memory_config = configmanager.as_dict()
        self._config = self.in_memory_config
