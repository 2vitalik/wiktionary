from lib.parse.groupers.blocks.base_blocks import BaseBlocksGrouper


class BlocksGrouper(BaseBlocksGrouper):
    def __init__(self, base, header=None):
        super().__init__(base, header, no_sub_blocks=True)

    def __iter__(self):
        for (lang, homonym_header, header), block in self.base.deep(self.level):
            if self.header:  # если мы что-то ищем:
                if header == self.header:
                    key = (lang, homonym_header)
                    yield key, block
                    continue
            else:  # если хотим получить все заголовки:
                key = (lang, homonym_header, header)
                yield key, block
