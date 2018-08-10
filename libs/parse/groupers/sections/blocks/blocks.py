from libs.parse.groupers.sections.blocks.base_blocks import BaseBlocksGrouper


class BlocksGrouper(BaseBlocksGrouper):
    def __init__(self, base, header=None):
        super().__init__(base, header, no_sub_blocks=True)

    def __iter__(self):
        for path, block in self.base.deep(self.level):
            # `path` is (lang, homonym_header, header) here
            if self.header:  # если мы что-то ищем:
                header = path[-1]
                if header == self.header:
                    return_path = path[:-1]  # без header
                    # `return_path` is (lang, homonym_header) here
                    yield return_path, block
                    continue
            else:  # если хотим получить все заголовки:
                yield path, block
