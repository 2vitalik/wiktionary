import os
from os.path import join, exists

from core.conf import conf
from libs.utils.dt import dt
from libs.utils.io import write


def locked_repeat(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            lock_file = join(conf.ROOT_PATH, 'sys', 'lock', slug)
            if exists(lock_file):
                print(dt(), f'Already locked: `{slug}`')
                return
            write(lock_file, '')
            try:
                return func(*args, **kwargs)
            finally:
                os.remove(lock_file)
        return wrapped
    return decorator
