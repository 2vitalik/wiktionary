import os
from os.path import join


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

STORAGE_PATH = join(ROOT_PATH, 'storage')

MAIN_STORAGE_PATH = join(STORAGE_PATH, 'main')
REPORTS_PATH = join(STORAGE_PATH, 'reports')
SYNC_PATH = join(STORAGE_PATH, 'sync')


try:
    from .local_conf import *
except ImportError:
    pass
