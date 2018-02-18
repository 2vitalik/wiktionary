from datetime import datetime

import functools


def timing(func=None, *, desc=None):  # info: measure time of function work
    if func is None:
        return lambda f: timing(f, desc=desc)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started_at = datetime.now()
        result = func(*args, **kwargs)
        delta = datetime.now() - started_at
        print('@', delta, desc or func.__name__)
        return result
    return wrapper
