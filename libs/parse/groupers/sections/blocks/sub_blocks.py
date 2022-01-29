from libs.parse.groupers.sections.blocks.base_blocks import BaseBlocksGrouper


class SubBlocksGrouper(BaseBlocksGrouper):
    def __iter__(self):
        for _, block in self.iterate():
            yield block

    def iterate(self):
        for path, block in self.base.deep(self.level):
            # `path` is (lang, homonym_header, header) here
            if self.header:  # если мы что-то ищем:
                for sub_header, sub_block in block:
                    if sub_header == self.header:
                        yield path, sub_block
            else:  # если хотим получить все *под*заголовки:
                for sub_header, sub_block in block:
                    if sub_header == self.header:
                        return_path = path + (sub_header, )
                        # (lang, homonym_header, header, sub_header)
                        yield return_path, sub_block
