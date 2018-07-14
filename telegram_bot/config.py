import os

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

TELEGRAM_BOT_TOKEN = None  # should be secure set in `local_config.py`

MAIN_GROUP_CHAT_ID = None  # should be secure set in `local_config.py`
DEV_CHAT_ID = None  # should be secure set in `local_config.py`

try:
    from .local_config import *
except ImportError:
    pass
