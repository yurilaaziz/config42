builtin_types = {'string': str,
                 'integer': int,
                 'float': float,
                 'boolean': bool,
                 'dict': dict,
                 'list': list,
                 'set': set
                 }


def recursive(key, obj, value=None, update=False):
    _keys = key.split('.')
    assert len(_keys) > 0

    if isinstance(obj, list):
        _base = int(_keys[0])
    else:
        _base = _keys[0]

    if isinstance(obj, dict) and _base not in obj and not update:
        return None
    if isinstance(obj, list) and _base >= len(obj) and not update:
        return None
    elif isinstance(obj, list) and update:
        raise AttributeError("Insertion in list is not allowed")

    if isinstance(obj, str) and _base and not update:
        raise AttributeError("Cannot get {}' key from string.".format(_base))

    if len(_keys) == 1:
        if update:
            obj[_base] = value
        return obj[_base]
    else:
        if isinstance(obj, dict) and _base not in obj:
            obj[_base] = dict()

        return recursive('.'.join(_keys[1:]), obj[_base], value, update)


def flatten(dict_, parent_key='', separator='/'):
    if isinstance(dict_, dict):
        rst = {}
        for key, value in dict_.items():
            rst.update(flatten(value, "{}{}{}".format(parent_key, separator, key), separator))
        return rst
    elif isinstance(dict_, list):
        return flatten({k: v for k, v in enumerate(dict_)}, parent_key, separator)
    else:
        return {parent_key: dict_}
