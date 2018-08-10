from libs.storage.blocks.iterators.base import BaseBlockIterator
from libs.storage.const import SEPARATOR


class ContentsBlockIterator(BaseBlockIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = self.block_content.split(SEPARATOR)
        self.titles = self.contents[0].split('\n')[1:]

    def get(self, index):
        return self.contents[index + 1]
