from os.path import join, exists, isfile

from core import conf
from lib.common.io import read
from lib.common.unicode import char_info


class StorageError(Exception):
    pass


MAX_DEPTH = 7
SEPARATOR = '\n<%s>\n' % ('~' * 78)


def block_path(title):
    path = conf.STORAGE_PATH
    category, name = char_info(title[0])

    candidates = [
        join(path, category),
        join(path, category, name),
    ]

    path = candidates[-1]
    for i in range(min(len(title), MAX_DEPTH)):
        key = str(ord(title[i]))  # код соответствующего символа
        path = join(path, key)
        candidates.append(path)

    for candidate in candidates:
        if not exists(candidate):
            raise StorageError(f"Path does't exist: '{candidate}'")
        if isfile(candidate):
            return candidate

    raise StorageError(f"Path does't exist for title '{title}'")


def get_content(title):
    # todo: Использовать `cache` для ускорения массового считывания

    contents = read(block_path(title)).split(SEPARATOR)
    titles = contents[0].split('\n')
    pos = titles.index(title)
    return contents[pos]


if __name__ == '__main__':
    print(get_content('привет'))
