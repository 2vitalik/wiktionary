import os
from os.path import join


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

STORAGE_PATH = join(ROOT_PATH, 'storage')
LOGS_PATH = join(ROOT_PATH, 'logs')
DATA_PATH = join(ROOT_PATH, 'data')

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

MAIN_STORAGE_PATH = join(STORAGE_PATH, 'main')
AUTHORS_STORAGE_PATH = join(STORAGE_PATH, 'authors')
HTMLS_STORAGE_PATH = join(STORAGE_PATH, 'htmls')
PARSED_STORAGE_PATH = join(STORAGE_PATH, 'parsed')
REPORTS_PATH = join(STORAGE_PATH, 'reports')
SYNC_PATH = join(STORAGE_PATH, 'sync')

try:
    from .local_paths import *  # we can change storage sub-paths here
except ImportError:
    pass
