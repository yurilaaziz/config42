import json
import logging

import yaml

from config42 import ConfigManager
from config42.handlers.argparse import ArgParse

ACTION_APPLY = "apply"
ACTION_MERGE = "merge"
ACTION_READ = "read"
ACTION_DESTROY = "destroy"

schema = [
    dict(
        name="Main configuration",
        key="configuration",
        source=dict(argv=["-c"]),
        description="configuration file or handler type like (etcd, raw) to manipulate",
        required=False
    ), dict(
        name="Import configuration",
        key="from_configuration",
        source=dict(argv=["-f", "--from"]),
        description="Import from configuration file or handler type (etcd, raw)",
        required=False,
    ), dict(
        name="Output format",
        key="output_format",
        source=dict(argv=["-o"]),
        description="Export format",
        choices=["yaml", "json"],
        default="yaml",
        required=False,
    ), dict(
        name="Action",
        key="action",
        source=dict(argv=["-a", "--action"]),
        choices=[ACTION_APPLY, ACTION_MERGE, ACTION_READ, ACTION_DESTROY],
        description="Action to apply",
        required=False
    ), dict(
        name="Etcd host",
        key="etcd.host",
        description="Specify the ETCD Host",
        type="string",
        required=False,
        default='127.0.0.1',

    ), dict(
        name="Etcd port",
        key="etcd.port",
        description="Specify the ETCD server port ",
        type="integer",
        required=False,
        default=4001,

    ), dict(
        name="Etcd Keyspace",
        key="etcd.keyspace",
        description="Specify the ETCD keyspace where configuration is stored, ie : /config",
        default="/config",
        type="string",
        required=False

    ), dict(
        name="Raw directory",
        key="raw.path",
        description="Specify a directory path where configuration is stored in a separate raw files",
        type="string",
        required=False

    ), dict(
        name="Literal value",
        key="literals",
        source=dict(argv=['-l', '--from-literal'], argv_options=dict(nargs='+')),
        description="Specify a key and literal value to insert in the configuration (i.e. mykey=somevalue)",
        type="list",
        required=False

    ), dict(
        name="Verbosity",
        key="verbosity",
        source=dict(argv=['-v'], argv_options=dict(action='count')),
        description="verbosity level -v = INFO, -vv == DEBUG",
        required=False

    )
]

config = None


def read_from_configuration(configuration):
    if configuration in ('yaml', 'json'):
        import sys
        content = sys.stdin.read()
        if configuration == 'yaml':
            parsed_config = yaml.load(content, Loader=yaml.FullLoader)
        elif configuration == 'json':
            parsed_config = json.loads(content)
    else:
        config_manager = load_configmanager(configuration)
        parsed_config = config_manager.as_dict()

    if config.get('literals'):
        for literal in config.get('literals'):
            key, value = literal.split('=', 1)
            parsed_config[key] = value

    return parsed_config


def load_configmanager(configuration):
    if configuration == 'etcd':
        from config42.handlers.etcd import Etcd
        return ConfigManager(handler=Etcd, **config.get(configuration))

    elif configuration == 'raw':
        from config42.handlers.raw import RawHandler
        return ConfigManager(handler=RawHandler, **config.get(configuration))

    else:
        return ConfigManager(path=configuration)


def main():
    global config
    try:
        config = ConfigManager(handler=ArgParse, schema=schema, prog="config42")
        if not config.get('verbosity'):
            level = 100  # Disbaled
        elif config.get('verbosity') == 1:
            level = logging.INFO
        else:
            level = logging.DEBUG

        logging.basicConfig(level=level, format="[%(name)s/%(levelname)s] - %(message)s")

        configuration = config.get('configuration')
        from_configuration = config.get('from_configuration')
        action = config.get('action')

        if not action:
            if configuration and (from_configuration or config.get('literals')):
                action = ACTION_MERGE
            elif not configuration and not from_configuration and not config.get('literals'):
                config.handler.parser.print_help()
                raise SystemExit
            else:
                action = ACTION_READ

        if action == ACTION_READ:
            parsed_config = read_from_configuration(configuration)
            if config.get('output_format') == 'json':
                print(json.dumps(parsed_config, indent=2))
            else:
                print(yaml.dump(parsed_config))
        else:
            config_manager = load_configmanager(configuration)
            if action == ACTION_DESTROY:
                config_manager.handler.destroy()
                logging.info("{}/configuration has been destroyed, {}".format(configuration.capitalize(),
                                                                              config.get(configuration)))
            elif action == ACTION_APPLY:
                parsed_config = read_from_configuration(from_configuration)
                config_manager.handler.destroy()
                config_manager.replace(parsed_config)
                config_manager.commit()
                logging.info("{}/ previous configuration has been flushed, {}".format(configuration.capitalize(),
                                                                                      config.get(configuration)))
            elif action in ACTION_MERGE:
                # update a configuration
                parsed_config = read_from_configuration(from_configuration)
                config_manager.set_many(parsed_config)
                config_manager.commit()
                logging.info("{}/configuration has been updated, {}".format(configuration.capitalize(),
                                                                            config.get(configuration)))
    except SystemExit:
        exit(1)
    except KeyboardInterrupt:
        exit(127)
    except Exception as exc:
        logging.exception(exc)
        exit(1)


if __name__ == "__main__":
    main()
