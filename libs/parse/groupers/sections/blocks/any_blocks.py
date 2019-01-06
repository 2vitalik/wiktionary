from libs.parse.groupers.sections.blocks.base_blocks import BaseBlocksGrouper
from libs.utils.debug import debug


class AnyBlocksGrouper(BaseBlocksGrouper):
    def __iter__(self):
        self._debug_iter()
        for path, block in self.base.deep(self.level):
            # `path` is (lang, homonym_header, header) here
            if self.header:  # если мы что-то ищем:
                header = path[-1]
                if header == self.header:
                    return_path = path[:-1] + (None, )
                    # `return_path` is (lang, homonym_header, None) here
                    yield return_path, block
                    continue
                for sub_header, sub_block in block:
                    if sub_header == self.header:
                        yield path, sub_block
            else:  # если хотим получить все заголовки и подзаголовки:
                return_path = path + (None, )
                # `return_path` is (lang, homonym_header, header, None) here
                yield return_path, block
                for sub_header, sub_block in block:
                    if sub_header == self.header:
                        return_path = path + (sub_header, )
                        # (lang, homonym_header, header, sub_header)
                        yield return_path, sub_block

    @debug
    def _debug_iter(self):
        print('- Iterating through AnyBlocksGrouper()')
