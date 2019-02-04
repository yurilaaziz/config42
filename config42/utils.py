from functools import reduce


def flat_get(store, key, sep="."):
    """
    Gets an element in a nested dict/list from a dot-separated key (or other separator)
    Keys are string, automatically casted to int for nested list access
    :param store: nested dict/list
    :param key: keys joined with a separator
    :param sep: separator of the keys, '.' by default
    :return: the element indexed by the key or None if it doesn't exist
    """
    assert store is not None and key
    for k in key.split(sep):
        if k.isnumeric():
            k = int(k)
            assert isinstance(store, list)
            if k >= len(store):
                return None
        else:
            assert isinstance(store, dict)
            if k not in store:
                return None
        store = store[k]
    return store


def flat_set(store, key, value, sep="."):
    """
    Sets an element in a nested dict/list with a dot-separated key (or other separator)
    Keys are string, automatically casted to int for nested list access
    :param store: nested dict/list
    :param key: keys joined with a separator
    :param value: the value indexed by the key
    :param sep: separator of the string, '.' by default
    """
    assert store is not None and key
    prev_k, prev_store = None, None
    for k in key.split(sep):
        if k.isnumeric():
            k = int(k)
            if not isinstance(store, list):
                store = [None] * (k + 1)
                prev_store[prev_k] = store
            elif k >= len(store):
                store += [None] * (k + 1 - len(store))
        else:
            if not isinstance(store, dict):
                store = {k: None}
                prev_store[prev_k] = store
            elif k not in store:
                store[k] = None
        prev_k, prev_store = k, store
        store = store[k]
    if prev_store[prev_k] == value:
        return False
    else:
        prev_store[prev_k] = value
        return True


def flat_del(store, key, sep="."):
    """
    Deletes an element in a nested dict/list with a dot-separated key (or other separator)
    Keys are string, automatically casted to int for nested list access
    :param store: nested dict/list
    :param key: keys joined with a separator
    :param sep: separator of the string, '.' by default
    """
    assert store is not None and key
    keys = key.split(sep)
    for k in keys[:-1]:
        if k.isnumeric():
            k = int(k)
            assert isinstance(store, list)
            if k >= len(store):
                return
        else:
            assert isinstance(store, dict)
            if k not in store:
                return
        store = store[k]
    k = keys[-1]
    if k.isnumeric():
        k = int(k)
        if k < len(store):
            del store[k]
            return True
    else:
        if k in store:
            del store[k]
            return True
    return False


def flat_items(store, sep="."):
    """
    Iterates on a nested dict/list items (dot-separated key, value)
    Nested lists indexes are automatically casted to string
    :param store: nested dict/list
    :param sep: separator of the string, '.' by default
    """

    def rec_items(store, keys):
        if isinstance(store, dict):
            items = store.items()
        elif isinstance(store, list):
            items = enumerate(store)
        else:
            yield (keys, store)
            return
        for key, value in items:
            yield from rec_items(value, keys + [str(key)])

    assert store is not None
    for keys, value in rec_items(store, []):
        yield sep.join(keys), value


def flat_merge(*stores):
    """
    Merge nested dict/list (not in place)
    :param stores: list of nested dict/list
    :return: the arguments merged in a new nested dict/list
    """

    def merge(base_store, new_store):
        """
        Return a new store, overriding base_store with new_store value
        """
        if type(base_store) != type(new_store):
            return new_store
        elif isinstance(base_store, dict):
            res = {k: v for k, v in base_store.items() if k not in new_store}
            for key in new_store:
                if key in base_store:
                    res[key] = merge(base_store[key], new_store[key])
                else:
                    res[key] = new_store[key]
            return res
        elif isinstance(base_store, list):
            min_len = min(len(base_store), len(new_store))
            res = [merge(base_store[key], new_store[key])
                   for key in range(min_len)]
            remain = base_store[min_len:] + new_store[min_len:]
            for elt in remain:
                res.append(elt)
            return res
        else:
            return new_store

    return reduce(merge, stores)


def coerce_str(s):
    """
    Coerce a string value to another type according to its content,
    Examples::
    >>> coerce_str("42")
    42
    >>> coerce_str("yes")
    True
    >>> coerce_str("FALSE")
    False
    """
    if s.isnumeric():
        return int(s)
    elif s.lower() in ("yes", "true", "ok"):
        return True
    elif s.lower() in ("no", "false", "ko"):
        return False
    else:
        return s
