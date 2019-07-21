import json

import yaml

from config42 import ConfigManager
from config42.handlers.argparse import ArgParse

ACTION_APPLY = "apply"
ACTION_MERGE = "merge"
ACTION_READ = "read"
ACTION_DESTROY = "destroy"

schema = [
    dict(
        name="Main configuration ",
        key="configuration",
        source=dict(argv=["-c"]),
        description="configuration file to manipulate, or handler type (etcd, raw)",
        required=False
    ), dict(
        name="Exported configuration",
        key="from_configuration",
        source=dict(argv=["-f", "--from"]),
        description="Configuration file where additional configuration could be read"
                    " or handler type (etcd, raw).",
        required=False,
    ), dict(
        name="Output format",
        key="output_format",
        source=dict(argv=["-o"]),
        description="Output format",
        choices=["yaml", "json"],
        default="yaml",
        required=False,
    ), dict(
        name="Action",
        key="action",
        source=dict(argv=["-a", "--action"]),
        choices=[ACTION_APPLY, ACTION_MERGE, ACTION_READ, ACTION_DESTROY],
        description="action to apply",
        required=False
    ), dict(
        name="Etcd host",
        key="etcd.host",
        description="ETCD Host",
        type="string",
        required=False

    ), dict(
        name="Etcd port",
        key="etcd.port",
        description="ETCD server port ",
        type="string",
        required=False

    ), dict(
        name="Etcd Keyspace",
        key="etcd.keyspace",
        description="ETCD keyspace where configuration will be stored, ie : /config ",
        default="/config",
        type="string",
        required=False

    ), dict(
        name="Raw directory",
        key="raw.path",
        description="Directory each element will be stored in a separate file  ",
        type="string",
        required=False

    ), dict(
        name="Literal value",
        key="literals",
        source=dict(argv=['-l', '--from-literal'], argv_options=dict(nargs='+')),
        description="Specify a key and literal value to insert in the configuration (i.e. mykey=somevalue)",
        type="list",
        required=False

    )
]

config = None


def read_from_configuration(configuration):
    parsed_config = {}
    if configuration in ('etcd', 'raw'):
        config_manager = ConfigManager(**config.get(configuration))
        parsed_config = config_manager.as_dict()
    elif configuration in ('yaml', 'json'):
        import sys
        content = sys.stdin.read()
        if configuration == 'yaml':
            parsed_config = yaml.load(content)
        elif configuration == 'json':
            parsed_config = json.loads(content)
    elif configuration:
        config_manager = ConfigManager(path=configuration)
        parsed_config = config_manager.as_dict()
    elif config.get('literals'):
        for literal in config.get('literals'):
            key, value = literal.split('=', 1)
            parsed_config[key] = value

    return parsed_config


def update_config(action, config_input, parsed_config):
    if config_input in ('etcd', 'raw'):
        config_manager = ConfigManager(**config.get(config_input))
    else:
        config_manager = ConfigManager(path=config_input)
        # Erase data store before
    if action in (ACTION_APPLY, ACTION_DESTROY):
        config_manager.handler.flush()
        config_manager.handler.destroy()
        print("destroyed")
    # update a configuration
    if action in (ACTION_APPLY, ACTION_MERGE):
        config_manager.set_many(parsed_config)
        config_manager.commit()
    print("{}/configuration has been updated, {}".format(config_input.capitalize(), config.get(config_input)))


def load_configmanager(configuration):
    if configuration in ('etcd', 'raw'):
        config_manager = ConfigManager(**config.get(configuration))
    else:
        config_manager = ConfigManager(path=configuration)
    return config_manager


def main():
    global config
    try:
        config = ConfigManager(handler=ArgParse, schema=schema, prog="config42")
        print(config.as_dict())

        configuration = config.get('configuration')
        from_configuration = config.get('from_configuration')

        action = config.get('action')
        if not action:
            if configuration and not from_configuration and not config.get('literals'):
                action = ACTION_READ
            else:
                action = ACTION_MERGE

        if action == ACTION_READ:
            parsed_config = read_from_configuration(configuration)
            output_format = config.get('output_format')
            if output_format == 'json':
                print(json.dumps(parsed_config, indent=2))
            elif output_format == 'yaml':
                print(json.dumps(parsed_config, indent=2))
        else:
            config_manager = load_configmanager(configuration)
            if action == ACTION_DESTROY:
                config_manager.handler.destroy()
                print("{}/configuration has been destroyed, {}".format(configuration.capitalize(),
                                                                       config.get(configuration)))
            elif action == ACTION_APPLY:
                parsed_config = read_from_configuration(from_configuration)
                config_manager.handler.flush()
                config_manager.handler.destroy()
                config_manager.set_many(parsed_config)
                config_manager.commit()
                print("{}/ previous configuration has been flushed, {}".format(configuration.capitalize(),
                                                                               config.get(configuration)))

            elif action in ACTION_MERGE:
                # update a configuration
                parsed_config = read_from_configuration(from_configuration)
                config_manager.set_many(parsed_config)
                config_manager.commit()
                print("{}/configuration has been updated, {}".format(configuration.capitalize(),
                                                                     config.get(configuration)))

    except Exception as exc:
        raise exc
        print(exc)
        exit(1)


if __name__ == "__main__":
    main()
