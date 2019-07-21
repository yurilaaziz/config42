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

        self.parser = argparse.ArgumentParser(**argparge_kwargs)

        for item in schema:
            flags_name = item.get('source', {}).get('argv', ['--' + item['key'].replace('.', '-')])
            argv_options = item.get('source', {}).get('argv_options', {})
            if flags_name:
                options = dict(help=item.get('description'),
                               dest=item.get('key')
                               )
                if item.get('type'):
                    options['type'] = {'string': str,
                                       'integer': int,
                                       'float': float,
                                       'boolean': bool
                                       }.get(item.get('type'), str)
                if item.get('choices'):
                    options['choices'] = item.get('choices')
                elif not argv_options.get("action", '') == 'count':
                    options['metavar'] = item.get('name')
                if argv_options:
                    options.update(argv_options)
                self.parser.add_argument(*flags_name, **options)

        args = self.parser.parse_args(argv)
        configmanager = ConfigManager()
        configmanager.set_many(vars(args))

        self.in_memory_config = configmanager.as_dict()
        self.config = self.in_memory_config
