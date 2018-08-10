from libs.storage.error import StorageError
from libs.utils.io import read


class BaseBlockIterator:
    def __init__(self, path):
        # print(path)
        self.path = path
        self.contents = None  # should be set in inheritors
        self.titles = None  # should be set in inheritors

        self.block_content = read(self.path)
        if not self.block_content:
            raise StorageError(f'Block is empty: "{self.path}"')

    def __iter__(self):
        if self.titles is None or self.contents is None:
            raise NotImplementedError('`titles` or `contents` is empty')
        for index, title in enumerate(self.titles):
            yield title, self.get(index)

    def get(self, index):
        raise NotImplementedError()
