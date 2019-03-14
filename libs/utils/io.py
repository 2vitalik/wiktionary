import hashlib
import json
import os
import sys
from os.path import dirname, exists

from libs.utils.dt import dt
from libs.utils.exceptions import LockError, UnlockError


def md5(value):
    return hashlib.md5(value.encode()).hexdigest()


def encoded_filename(func):
    def wrapped(*args, **kwargs):
        filename = args[0]
        if type(filename) == str:
            args = (filename.encode(), *args[1:])  # need for Cyrl in Linux etc.
        return func(*args, **kwargs)
    return wrapped


@encoded_filename
def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


@encoded_filename
def read_lines(filename, ignore_absent=False):
    if ignore_absent and not exists(filename):
        # todo: также писать куда-нибудь в логи?
        print(f"[read_lines] File doesn't exist: {filename}", file=sys.stderr)
        return []
    return read(filename).split('\n')


@encoded_filename
def write(filename, content):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


@encoded_filename
def write_lines(filename, lines):
    return write(filename, '\n'.join(lines))


@encoded_filename
def append(filename, line):
    ensure_parent_dir(filename)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'{line}\n')


def compare(filename1, filename2):
    return read(filename1) == read(filename2)


@encoded_filename
def ensure_dir(path):
    if not path:
        return
    if not exists(path):
        os.makedirs(path)


@encoded_filename
def ensure_parent_dir(filename):
    ensure_dir(dirname(filename))


@encoded_filename
def json_dump(filename, data):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@encoded_filename
def json_load(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)


@encoded_filename
def is_locked(filename):
    return exists(filename + b'.lock')


@encoded_filename
def lock_file(filename):  # todo: возможно попробовать сделать context manager `with locked(...):`
    if is_locked(filename):
        raise LockError(filename)
    write(filename + b'.lock', dt())


@encoded_filename
def unlock_file(filename):
    if not is_locked(filename):
        raise UnlockError(filename)
    os.remove(filename + b'.lock')


def fix_path(path):
    return '/'.join(fix_filename(name) for name in path.split('/'))


def fix_filename(filename):
    if filename.lower() in ['con', 'nul']:
        filename += '{}'
    return filename.\
        replace('?', '{question}').\
        replace(':', '{colon}').\
        replace('/', '{slash}').\
        replace('"', '{quot}').\
        replace('|', '{pipe}').\
        replace('*', '{asterisk}').\
        replace('<', '{lt}').\
        replace('>', '{gt}')


def unfix_filename(filename):
    if filename.lower() in ['con{}', 'nul{}']:
        return filename[:-2]
    return filename.\
        replace('{question}', '?').\
        replace('{colon}', ':').\
        replace('{slash}', '/').\
        replace('{quot}', '"').\
        replace('{pipe}', '|').\
        replace('{asterisk}', '*').\
        replace('{lt}', '<').\
        replace('{gt}', '>')
