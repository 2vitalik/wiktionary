from libs.storage.blocks.iterators.base import BaseBlockIterator


class SimpleBlockIterator(BaseBlockIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = self.block_content.split('\n')
        self.titles = [line.split('\t')[0] for line in self.contents]

    def get(self, index):
        return self.contents[index].split('\t', maxsplit=1)[1]
