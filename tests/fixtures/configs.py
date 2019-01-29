import pytest

@pytest.fixture
def default_config():
    return {
        'defaultkey1': 'simple',
        'defaultkey2': {'defaultkey2': 'simple'}
    }


@pytest.fixture
def sample_config():
    return {
        'simple': 'value',
        'bool': True,
        'simple_dict': {'key': 'value'},
        'nested_dict': {'key': 'value', 'nested': {'key': 'value'}},
        'nested_list': [[''], ['value']]
    }

