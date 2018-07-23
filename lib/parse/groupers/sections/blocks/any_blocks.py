from lib.parse.groupers.sections.blocks.base_blocks import BaseBlocksGrouper


class AnyBlocksGrouper(BaseBlocksGrouper):
    def __iter__(self):
        for (lang, homonym_header, header), block in self.base.deep(self.level):
            if self.header:  # если мы что-то ищем:
                if header == self.header:
                    path = (lang, homonym_header, None)
                    yield path, block
                    continue
                for sub_header, sub_block in block:
                    if sub_header == self.header:
                        path = (lang, homonym_header, header)
                        yield path, sub_block
            else:  # если хотим получить все заголовки и подзаголовки:
                path = (lang, homonym_header, header, None)
                yield path, block
                for sub_header, sub_block in block:
                    if sub_header == self.header:
                        path = (lang, homonym_header, header, sub_header)
                        yield path, sub_block
