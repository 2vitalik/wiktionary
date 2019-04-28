from libs.storage.builder import SimpleStorageBuilder, ContentsStorageBuilder
from libs.utils.io import append
from libs.utils.timing import timing


class StorageCopier:
    def __init__(self, old_storage, new_storage, table, *args, **kwargs):
        self.old_storage = old_storage
        self.table = table
        kwargs['path'] = new_storage.handlers[table].path
        kwargs['titles'] = old_storage.titles
        kwargs['max_count'] = old_storage.handlers[table].max_count
        super().__init__(*args, **kwargs)


class StorageCopierSingleData(StorageCopier):
    def data(self, title):
        append('copier_log.txt', title)
        return self.old_storage.get(title)


class StorageCopierMultiData(StorageCopier):
    def data(self, title):
        return self.old_storage.get(title, self.table)


class SimpleStorageCopierSingleData(StorageCopierSingleData,
                                    SimpleStorageBuilder):
    ...


class ContentStorageCopierSingleData(StorageCopierSingleData,
                                     ContentsStorageBuilder):
    ...


class SimpleStorageCopierMultiData(StorageCopierMultiData,
                                   SimpleStorageBuilder):
    ...


class ContentStorageCopierMultiData(StorageCopierMultiData,
                                    ContentsStorageBuilder):
    ...


@timing
def copy_storage(old_storage, new_storage, table, type1, type2):
    """
    :param type1: 'simple' or 'content'
    :param type2: 'single' or 'multi'
    """
    if type1 == 'simple' and type2 == 'single':
        cls = SimpleStorageCopierSingleData
    elif type1 == 'simple' and type2 == 'multi':
        cls = SimpleStorageCopierMultiData
    elif type1 == 'content' and type2 == 'single':
        cls = ContentStorageCopierSingleData
    elif type1 == 'content' and type2 == 'multi':
        cls = ContentStorageCopierMultiData
    else:
        raise Exception('Wrong values for `type1` and `type2`.')

    cls(old_storage, new_storage, table)
