from os.path import join

from lib.utils.dt import dtf
from lib.utils.io import ensure_parent_dir, append


def log(filename, line, path=None):
    if path:
        filename = join(path, filename)
    ensure_parent_dir(filename)
    append(filename, line)


def log_day(slug, value, path=None):
    log(f"{slug}/{dtf('Ym')}/{dtf('Ymd')}.txt", value, path=path)


def log_hour(slug, value, path=None):
    log(f"{slug}/{dtf('Ym')}/{dtf('dh')}.txt", value, path=path)
