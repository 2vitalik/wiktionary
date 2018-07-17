from lib.parse.groupers.base import BaseGrouper


class BlockGrouper(BaseGrouper):
    fields = ('lang', 'homonym', 'block')

    def __init__(self, langs, header):
        super(BlockGrouper, self).__init__()
        self.langs = langs
        self.header = header
        
    def __iter__(self):
        for lang, language in self.langs.items():
            for homonym_header, homonym in language.homonyms.items():
                for header, block in homonym.blocks.items():
                    if header == self.header:
                        key = (lang, homonym_header, None)
                        yield key, block
                        continue
                    for sub_header, sub_block in block.sub_blocks.items():
                        if sub_header == self.header:
                            key = (lang, homonym_header, header)
                            yield key, sub_block

    def all(self):
        return self.grouped(like_items=True, unique=True)
