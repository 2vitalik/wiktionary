import traceback
from os.path import join

from shared_utils.api.slack.core import post_to_slack

from core.conf.conf import LOGS_PATH
from libs.utils.dt import dtf, dt
from libs.utils.io import ensure_parent_dir, append


def log(filename, line, path=None):
    if path:
        filename = join(path, filename)
    ensure_parent_dir(filename)
    append(filename, f'{dt()}: {line}')


def log_day(slug, value, path=None):
    log(f"{slug}/{dtf('Ym/Ymd')}.txt", value, path=path)


def log_hour(slug, value, path=None):
    log(f"{slug}/{dtf('Ym/dh')}.txt", value, path=path)


def log_exception(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log(f"exceptions/{slug}/{dtf('Ym/Ymd')}.txt",
                    traceback.format_exc(), path=LOGS_PATH)
                post_to_slack(slug, traceback.format_exc())
                raise
        return wrapped
    return decorator
