import os
from os.path import dirname, exists


def encoded_filename(func):
    def wrapped(*args, **kwargs):
        filename = args[0]
        if type(filename) == str:
            args = (filename.encode(), *args[1:])
        return func(*args, **kwargs)
    return wrapped


@encoded_filename
def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


@encoded_filename
def write(filename, content):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


@encoded_filename
def append(filename, line):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'{line}\n')


@encoded_filename
def ensure_dir(path):
    if not path:
        return
    if not exists(path):
        os.makedirs(path)


@encoded_filename
def ensure_parent_dir(filename):
    ensure_dir(dirname(filename))


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
