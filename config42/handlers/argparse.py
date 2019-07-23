import argparse

from config42.handlers.memory import Memory
from config42.utils import recursive, builtin_types


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
                if item.get('type') in ('string', 'integer', 'float'):
                    options['type'] = builtin_types.get(item.get('type'), str)
                if item.get('choices'):
                    options['choices'] = item.get('choices')
                elif not argv_options.get("action", '') == 'count':
                    options['metavar'] = item.get('name')
                if argv_options:
                    options.update(argv_options)
                self.parser.add_argument(*flags_name, **options)

        args = self.parser.parse_args(argv)
        self.in_memory_config = {}
        for key, value in vars(args).items():
            if value is not None:
                recursive(key, self.in_memory_config, value,
                          update=True)
        self.config = self.in_memory_config
