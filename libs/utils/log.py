from os.path import join

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
