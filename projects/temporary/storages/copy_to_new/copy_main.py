import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(dirname(abspath(__file__)))))))

from core.conf import conf
from core.storage.main import MainStorage, storage
from projects.temporary.storages.copy_to_new.base_copy_to_new_storage import \
    copy_storage

if __name__ == '__main__':
    old_main_storage = \
        MainStorage(path=f'{conf.MAIN_STORAGE_PATH}_old')

    copy_storage(old_main_storage, storage, 'info',
                 'simple', 'multi')
    copy_storage(old_main_storage, storage, 'content',
                 'content', 'multi')
