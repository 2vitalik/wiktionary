from libs.utils.exceptions import SkipSlackErrorMixin


class StorageError(Exception):
    pass


class PageNotFound(StorageError):
    pass


class BlockNotFound(StorageError):
    pass


class StorageAlreadyLocked(StorageError, SkipSlackErrorMixin):
    pass
