import os
from os.path import join


ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

STORAGE_PATH = join(ROOT_PATH, 'storage')


try:
    from .local_conf import *
except ImportError:
    pass