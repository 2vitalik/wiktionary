import os
from os.path import dirname, exists


def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


def write(filename, content):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def append(filename, line):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'{line}\n')


def ensure_dir(path):
    if not path:
        return
    if not exists(path):
        os.makedirs(path)


def ensure_parent_dir(filename):
    ensure_dir(dirname(filename))
