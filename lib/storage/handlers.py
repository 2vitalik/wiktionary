from lib.storage.blocks.content import ContentsBlock
from lib.storage.blocks.simple import SimpleBlock


class BaseStorageHandler:
    block_class = None

    def __init__(self, path, max_count):
        self.path = path
        self.max_count = max_count

    def block(self, title):
        if not self.block_class:
            raise NotImplementedError('You need set `block_class` attribute')
        return self.block_class(title, self)

    def get(self, title):
        return self.block(title).get()

    def update(self, title, value):
        self.block(title).update(value)

    def delete(self, title):
        self.block(title).delete()


class ContentStorageHandler(BaseStorageHandler):
    block_class = ContentsBlock

    # todo: Использовать `cache` для ускорения массового считывания


class SimpleStorageHandler(BaseStorageHandler):
    block_class = SimpleBlock
