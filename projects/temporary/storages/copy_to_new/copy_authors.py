import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(dirname(abspath(__file__)))))))

from core.conf import conf
from projects.authors.authors_storage import AuthorsStorage, authors_storage
from projects.temporary.storages.copy_to_new.base_copy_to_new_storage import \
    copy_storage

if __name__ == '__main__':
    old_authors_storage = \
        AuthorsStorage(path=f'{conf.AUTHORS_STORAGE_PATH}_old')

    copy_storage(old_authors_storage, authors_storage, 'created',
                 'simple', 'single')
