import pytest


@pytest.fixture
def cwd():
    from os.path import dirname, realpath
    cwd = dirname(realpath(__file__)) + "/.."
    return cwd


@pytest.fixture
def default_config():
    return {
        'defaultkey1': 'simple',
        'defaultkey2': {'defaultkey2': 'simple'}}


@pytest.fixture
def sample_config():
    return {
        'simple': 'value',
        'bool': True,
        'simple_dict': {'key': 'value'},
        'nested_dict': {'key': 'value', 'nested': {'key': 'value'}},
        'nested_list': [[''], ['value']]}


@pytest.fixture
def sample_config_ini_with_sections():
    return {
        'section1': {'key1': 'value'},
        'section2': {'key2': 'value'}, }
