import pytest

import config42
from config42.handlers.argparse import ArgParse

SCHEMA = [
    dict(
        name="Key one",
        description="First Key long description",
        source=dict(argv=["-k", "--keyone"]),
        key="keyone",
        choices=None,
        default=None,
        required=True,
        freezed=False,
        type=str

    ), dict(
        name="Key two",
        description="Second Key long description",
        source=dict(argv=["-j", "--keytwo"]),
        key="key.two",
    ), dict(
        name="optional_key",
        description="optional_key long description",
        source=dict(argv=["-o", "--optional1"]),
        key="optional_key"
    ), dict(
        name="absent_key1",
        description="optional_key long description",
        source=dict(argv=["--optional-key"]),
        key="nested.optional_key",
        choices=["value1", "value2"]
    ),
    dict(
        name="absent_key2",
        description="optional_key2 long description",
        source=dict(argv=["--optional-key2"]),
        key="nested.optional_key",
        choices=["value1", "value2"]
    ),
    dict(
        name="absent_key_default",
        description="optional_key2 long description",
        source=dict(argv=["--optional-key-default"]),
        key="nested.absent_key_default"
    ),
    dict(
        name="key_source_omitted",
        description="key_source_omitted long description",
        key="key_source_omitted"
    )
]


def test_load_empty_config():
    with pytest.raises(TypeError):
        _ = config42.ConfigManager(handler=ArgParse)

    config_manager = config42.ConfigManager(handler=ArgParse, schema=[], argv=[])
    assert config_manager.handler.load() is not None


def test_load_configuration():
    argv = "-k value1 --keytwo value2 -o value3 --optional-key2 value1" \
           " --key_source_omitted=value".split(" ")
    config_manager = config42.ConfigManager(handler=ArgParse, schema=SCHEMA, argv=argv)
    assert config_manager.get('keyone') == "value1"
    assert config_manager.get('key.two') == "value2"
    assert config_manager.get('optional_key') == "value3"
    assert config_manager.get('absent_key1') is None
    assert config_manager.get('nested.optional_key') == "value1"
    assert config_manager.get('key_source_omitted') == "value"
