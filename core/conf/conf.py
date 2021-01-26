import os
from os.path import join


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

storage_path = join(ROOT_PATH, 'storage')
logs_path = join(ROOT_PATH, 'logs')
data_path = join(ROOT_PATH, 'data')

TELEGRAM_TOKEN = None  # should be set in `local_conf.py`

MAIN_GROUP_CHAT_ID = None  # should be set in `local_conf.py`
NEW_CHANNEL_ID = None  # should be set in `local_conf.py`
DEV_CHAT_ID = None  # should be set in `local_conf.py`

ADMINS = []  # should be set in `local_conf.py`

DEBUGGING = False

try:
    from .local_conf import *
except ImportError:
    pass

MAIN_STORAGE_PATH = join(storage_path, 'main')
AUTHORS_STORAGE_PATH = join(storage_path, 'authors')
HTMLS_STORAGE_PATH = join(storage_path, 'htmls')
PARSED_STORAGE_PATH = join(storage_path, 'parsed')
REPORTS_PATH = join(storage_path, 'reports')
SYNC_PATH = join(storage_path, 'sync')

try:
    from .local_paths import *  # we can change storage sub-paths here
except ImportError:
    pass
