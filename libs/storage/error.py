
class StorageError(Exception):
    pass


class PageNotFound(StorageError):
    pass


class BlockNotFound(StorageError):
    pass
