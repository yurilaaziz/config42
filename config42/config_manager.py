import inspect
import logging
from importlib import import_module

from jinja2 import Environment, BaseLoader

from config42.handlers.base import ConfigHandlerBase
from config42.handlers.memory import Memory
from config42.init_apps import InitApp
from config42.utils import recursive
from config42.validator import DefaultValidator


class ConfigManager:
    def __init__(self, application=None, nested_configuration_key=None, defaults=None, validator=None,
                 **handler_kwargs):
        self.logger = logging.getLogger()
        self.jinja2_recurse_limit = 10
        self.jinja2_env = Environment(loader=BaseLoader())
        self.validator = validator
        schema = handler_kwargs.get('schema')
        if self.validator is None and schema:
            self.validator = DefaultValidator(schema)

        self.defaults = defaults if defaults else {}
        self.nested_configuration_key = nested_configuration_key if nested_configuration_key else "config42"
        # Implicit load of handlers

        self.handler = self.load_handler(**handler_kwargs)
        if schema:
            self.load_defaults(schema)
        self.load_nested()
        self.validate()
        if application:
            self.init_app(application)

    def validate(self):
        if self.validator:
            return self.validator.validate(self)

    def load_defaults(self, schema):
        for item in schema:
            if item.get('default'):
                self.set(item.get('key'), item.get('default'), default=True)

    def load_handler(self, handler=None, **kwargs):
        if handler is None:
            if kwargs.get('path'):
                from config42.handlers import FileHandler
                handler = FileHandler
            elif kwargs.get('keyspace'):
                from config42.handlers.etcd import Etcd
                handler = Etcd
            elif kwargs.get('prefix'):
                from config42.handlers.environment import Environment as EnvironmentHandler
                handler = EnvironmentHandler
            else:
                handler = Memory

        return handler(**kwargs)

    def load_nested(self):
        nested = {}
        handlers = self.get(self.nested_configuration_key)

        if not handlers:
            return

        while handlers:
            name, item = handlers.popitem()
            if name not in nested:
                nested[name] = item
                handler = item.pop('handler', None)
                if not handler:
                    handler_obj = self.load_handler(**item)
                elif isinstance(handler, str):
                    handler_package = handler.split(':')[0]
                    handler_class = handler.split(':')[1]
                    handler_obj = getattr(import_module(handler_package), handler_class)(**item)
                elif inspect.isclass(handler) and issubclass(handler, ConfigHandlerBase):
                    handler_obj = self.load_handler(handler=handler, **item)

                new_configuration = handler_obj.config

                new_handlers = new_configuration.pop(self.nested_configuration_key, {})
                handlers.update(new_handlers)
                self.set_many(new_configuration)
        self.set_many({self.nested_configuration_key: nested})

    def get_defaults(self, key):
        return self.operate(key, obj=self.defaults)

    def operate(self, *args, **kwargs):
        # TODO: rework recursive operation
        return recursive(*args, **kwargs)

    def get(self, key, render=True):
        """
            Gets config value for a given key from the data store. Returns the value that matches the supplied key.
            If the value is not set, a default value will be returned as set by set_defaults.
            :param key: The configuration key to return a config value for
            :type key: str
            :param render: render Jinja2 templates, default True
            :type render: bool
            :rtype: Any supported (str, int, bool, list-of-supported-types)
        """
        value = self.operate(key, obj=self.handler.config)
        if value is None:
            value = self.get_defaults(key)
        return self.render_recursive(value) if render else value

    def set(self, key, value, default=False, trigger_commit=True):
        """
            Sets config value for a given key in the data store.
            :param key: The configuration key to set
            :type key: str
            :param value: The value to set the configuration key to
            :type value: Any supported (str, int, bool, list-of-supported-types)
            :param default: update default variables instead of current configuration
            :type default: bool
            :param trigger_commit: Flag whether to trigger a config commit after all values are set.
            :type trigger_commit: bool
            :rtype: bool (success)
        """
        obj = self.defaults if default else self.handler.config
        if self.operate(key, obj) == value:
            self.logger.debug("`{}` is already set to `{}`".format(key, value))
            return False  # Not updating

        self.operate(key, obj, value=value, update=True)
        self.logger.debug("`{}{}` is updated to `{}`".format("default/" if default else "", key, value))
        if not default:
            self.handler.updated = True
        if trigger_commit:
            self.commit()
            self.logger.debug("commit is triggered")

        return self.handler.updated

    def replace(self, config, trigger_commit=True):
        """
        Completely reset the config with a set of key values.
        It is the equivalent of unsetting all keys, followed by a
        set_many. Anything not in the supplied config will revert to default.
        :param config: A dictionary of keys and values to set as defaults
        :type config: dict
        :param trigger_commit: Flag whether to trigger a config commit after all values are set.
        :type trigger_commit: bool
        """
        self.handler.flush()
        self.set_many(config, trigger_commit)

    def set_many(self, config, trigger_commit=True):
        """
        Sets the value of multiple config settings simultaneously.
        This postpones the
        triggering of the commit signal after all values are set.
        :param config: A dictionary of keys and values to set.
        :type key: dict
        :param trigger_commit: Flag whether to trigger a config commit after all values are set.
        :type trigger_commit: bool
        """
        has_been_updated = False
        for key, value in config.items():
            updated = self.set(key, value, trigger_commit=False)
            has_been_updated = has_been_updated or updated

        if has_been_updated and trigger_commit:
            self.commit()

    def render(self, template):
        """
         Render recursively a Jinja2 template at runtime the current configuration as context.
         :param template: A Jinja2 template
         :type template: string
         """
        rendered_value = template
        rendered_template = None
        count = 0
        while rendered_value != rendered_template and count < self.jinja2_recurse_limit:
            rendered_template = rendered_value
            rendered_value = self.jinja2_env.from_string(rendered_template).render(self.as_dict())
            count += 1

        if count == self.jinja2_recurse_limit:
            self.logger.warning(
                "Reach recursive limit while rendering '{}', final '{}'".format(template, rendered_value))
            return None
        return rendered_value

    def render_recursive(self, obj):
        if isinstance(obj, str):
            return self.render(obj)
        elif isinstance(obj, dict):
            return {key: self.render_recursive(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.render_recursive(item) for item in obj]
        else:
            return obj

    def commit(self):
        return self.handler.dump()

    def init_app(self, app):
        return InitApp.init_app(self.as_dict(), app)

    def as_dict(self):
        return self.handler.config
