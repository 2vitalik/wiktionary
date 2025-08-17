import os
from os.path import join

from shared_utils.conf import conf as shared_conf


root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

storage_path = join(root_path, 'storage')  # should be changed in local_conf.py
logs_path = join(root_path, 'logs')  # should be changed in local_conf.py
data_path = join(root_path, 'data')  # should be changed in local_conf.py
slack_path = f'{logs_path}/slack'

telegram_token = None  # should be set in `local_conf.py`

main_group_id = None  # should be set in `local_conf.py`
new_channel_id = None  # should be set in `local_conf.py`
new_group_id = None  # should be set in `local_conf.py`
dev_chat_id = None  # should be set in `local_conf.py`
bot_chat_id = None  # should be set in `local_conf.py`

admin_user_id = None  # should be set in `local_conf.py`
admin_ids = []  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'all_pages-changed': None,
    'all_pages-deleted': None,
    'all_pages-errors': None,
    'all_pages-status': None,
    'recent-changed': None,
    'recent-deleted': None,
    'recent-errors': None,
    'recent-status': None,
    'recent-titles': None,
    'bot-errors': None,
    'bot-status': None,
    'bot-messages': None,
    'bot-callbacks': None,
}

DEBUGGING = False

try:
    from .local_conf import *
except ImportError:
    pass

ws1_jobs_path = '../words/files'

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


shared_conf.slack_hooks = slack_hooks
shared_conf.slack_path = slack_path
