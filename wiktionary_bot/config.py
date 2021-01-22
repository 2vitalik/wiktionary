import os

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

TELEGRAM_BOT_TOKEN = None  # should be secure set in `local_config.py`

MAIN_GROUP_CHAT_ID = None  # should be secure set in `local_config.py`
NEW_CHANNEL_ID = None  # should be secure set in `local_config.py`
DEV_CHAT_ID = None  # should be secure set in `local_config.py`

TELEGRAM_ADMIN = None  # should be secure set in `local_config.py`
ADMINS = [
    # should be secure set in `local_config.py`
]

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

data_path = 'data'
logs_path = 'logs'

try:
    from .local_config import *
except ImportError:
    pass
