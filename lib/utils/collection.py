
def chunks(items, chunk_len):
    """
    Yield successive n-sized chunks from items
    """
    for i in range(0, len(items), chunk_len):
        yield items[i:i+chunk_len]


def rest_path(path, indexes):
    """
    Build new `path` without parts with indexes from `indexes`.
    This function is used in `group` function only.

    Arguments:
    - `path`: tuple of keys
    - `indexes`: indexes to be filtered

    Examples:
        rest_path(('a', 'b', 'c'), (0, )) -> ('b', 'c')
        rest_path(('a', 'b', 'c'), (0, 1)) -> 'c'
        rest_path(('a', 'b', 'c', 'd'), (2, 1)) -> ('a', 'd')
    """
    indexes = tuple(filter(lambda x: x != -1, indexes))  # exclude `-1` values
    result = tuple([val for ind, val in enumerate(path) if ind not in indexes])
    if len(indexes) == len(path) - 1:
        result = result[0]  # because we have only one value in tuple
    return result


def group(data, indexes, like_items, unique):
    """
    Group `data` in a hierarchical dictionary.

    Arguments:
    - `data`: iterable, each entry is (`key`, `value`), `key` is tuple of keys
    - `indexes`: indexes of parts of `key` used as keys of hierarchical dicts
    - `like_items`: if True: last layer will be a dict, otherwise -- list
    - `unique`: if False: last layer will be a list, otherwise -- single value

    Example input:
        - `keys` is like ('A', 'a'), ('A', 'b'), ('B', ...)
        - `values` is like 1, 2, 3, ...
        - `indexes` is (0, )  # group by first part of the `key`
    Example results:
        - like_items=True, unique=False:  # .items()
            {'A': {'a': [1, 2, 3], 'b': [4]}, 'B': ...}
        - like_items=True, unique=True:  # .items()
            {'A': {'a': 1, 'b': 4}, 'B': ...}
        - like_items=False, unique=False:  # .values()
            {'A': [1, 2, 3, 4]}, 'B': ...}
        - like_items=False, unique=True:  # .values()
            {'A': 1, 'B': ...}
    """
    result = {}

    if like_items:
        indexes += (-1, )  # additional layer that will be a dict with rest keys

    if len(indexes) == 0:  # fixme: написать для чего `len(indexes) == 0`
        result = []

    for path, value in data:
        curr = result
        for i, index in enumerate(indexes):
            # prepare current key to use in dicts:
            if index == -1:
                if not like_items:
                    raise Exception("Index '-1' should be used only when "
                                    "`like_items=True`")
                key = rest_path(path, indexes)  # latest key for `items`
            else:
                key = path[index]  # next key to go deeper

            if not unique:  # use list() on the last layer
                if i < len(indexes) - 1:
                    default = dict()  # not a last step, so create a new dict()
                else:
                    default = list()  # last step, so create a list()
                curr = curr.setdefault(key, default)  # go deeper

            else:  # use unique values on the last layer
                if i < len(indexes) - 1:
                    default = dict()  # not a last step, so create a new dict()
                    curr = curr.setdefault(key, default)  # go deeper
                else:  # last step
                    if key in curr:
                        raise Exception("When `unique=True` entries can't be "
                                        "duplicated inside a grouped block")
                    curr[key] = value  # write single unique value here

        if not unique or len(indexes) == 0:  # fixme: написать для чего `len(indexes) == 0`
            # let's fill list() on the last layer
            curr.append(value)

    return result
