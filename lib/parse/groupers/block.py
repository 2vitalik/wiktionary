from lib.parse.groupers.base import BaseGrouper


class BlocksGrouper(BaseGrouper):
    fields = ('lang', 'homonym', 'block')

    def __init__(self, page, header):
        super(BlocksGrouper, self).__init__()
        self.page = page
        self.header = header

    def __iter__(self):
        for (lang, homonym_header, header), block in self.page.deep(3):
            if header == self.header:
                key = (lang, homonym_header, None)
                yield key, block
                continue
            for sub_header, sub_block in block:
                if sub_header == self.header:
                    key = (lang, homonym_header, header)
                    yield key, sub_block

    def all(self):
        return self.grouped(like_items=True, unique=True)
