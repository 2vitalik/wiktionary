import os


ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


try:
    from .local_conf import *
except ImportError:
    pass
