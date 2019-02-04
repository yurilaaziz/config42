import pytest

from config42.utils import (coerce_str, flat_del, flat_get, flat_items, flat_merge,
                            flat_set)


@pytest.fixture
def store():
    return {
        "simple":      "v1",
        "bool":        True,
        "simple_dict": {"key": "v2"},
        "nested_dict": {"key": "v3", "nested": {"key": "v4"}},
        "simple_list": ["", "v5"],
        "nested_list": [[""], ["v6"]]
    }


@pytest.fixture
def flat_store():
    return {
        ("simple", "v1"),
        ("bool", True),
        ("simple_dict.key", "v2"),
        ("nested_dict.key", "v3"),
        ("nested_dict.nested.key", "v4"),
        ("simple_list.0", ""),
        ("simple_list.1", "v5"),
        ("nested_list.0.0", ""),
        ("nested_list.1.0", "v6"),
    }


def test_flat_get(store, flat_store):
    for key, value in flat_store:
        assert flat_get(store, key) == value
    assert flat_get(store, "absent_key") is None


def test_flat_set():
    store = {}
    flat_set(store, "k1", "v1")
    assert store == {"k1": "v1"}
    flat_set(store, "k1.1", "v1")
    assert store == {"k1": [None, "v1"]}
    flat_set(store, "k1.0.k2", "v2")
    assert store == {"k1": [{"k2": "v2"}, "v1"]}


def test_flat_del():
    store = {"k1": [{"k2": "v2"}, "v1"]}
    flat_del(store, "k1.0")
    assert store == {"k1": ["v1"]}
    flat_del(store, "k1")
    assert store == {}


def test_flat_items(store, flat_store):
    assert set(flat_items(store)) == flat_store


def test_merge_dicts(store):
    assert flat_merge(store) == store
    assert flat_merge(store, True)
    assert flat_merge(store, {"simple": "v1b"}, {"simple_dict": {"key": "v2b"}}) == {
        "simple":      "v1b",
        "bool":        True,
        "simple_dict": {"key": "v2b"},
        "nested_dict": {"key": "v3", "nested": {"key": "v4"}},
        "simple_list": ["", "v5"],
        "nested_list": [[""], ["v6"]]
    }
    assert flat_merge(store, {"nested_list": [["v7"]]}) == {
        "simple":      "v1",
        "bool":        True,
        "simple_dict": {"key": "v2"},
        "nested_dict": {"key": "v3", "nested": {"key": "v4"}},
        "simple_list": ["", "v5"],
        "nested_list": [["v7"], ["v6"]]
    }


def test_coerce_str():
    values = {"": "", "false": False, "TRUE": True, "0": 0, "42": 42, "string": "string"}
    for s, res in values.items():
        assert coerce_str(s) == res
