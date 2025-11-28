import traceback
from os.path import join

import telegram
from shared_utils.api.slack.core import post_to_slack

from core.conf import conf
from core.conf.conf import logs_path
from libs.utils.dt import dtf, dt
from libs.utils.exceptions import SkipSlackErrorMixin
from libs.utils.io import ensure_parent_dir, append
from wiktionary_bot.src.utils import send


class Logger:
    slug = None


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
                Logger.slug = slug
                result = func(*args, **kwargs)
                Logger.slug = None
                return result
            except Exception as e:
                log(f"exceptions/{slug}/{dtf('Ym/Ymd')}.txt",
                    traceback.format_exc(), path=logs_path)
                if not isinstance(e, SkipSlackErrorMixin):
                    post_to_slack('recent-errors',
                                  f':no_entry: `{slug}` Error in command\n\n' +
                                  traceback.format_exc())
                    bot = telegram.Bot(conf.telegram_token)
                    send(bot, conf.main_group_id,
                         f'⛔ <code>{slug}</code>  <b>{type(e).__name__}</b>: {e}')
                raise
        return wrapped
    return decorator
