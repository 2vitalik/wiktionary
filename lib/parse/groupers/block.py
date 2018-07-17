from lib.utils.collection import group


class BlockGrouper:
    fields = ('lang', 'homonym', 'block')

    def __init__(self, langs, header):
        self.langs = langs
        self.header = header
        self._cache = {}

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

    def values(self, *args, unique=False):
        return self.grouped(*args, like_items=False, unique=unique)

    def items(self, *args, unique=False):
        return self.grouped(*args, like_items=True, unique=unique)

    def grouped(self, *args, like_items, unique):
        if args == ('*', ):
            args = self.fields
        if like_items and len(args) == len(self.fields):
            # last layers will be redundant
            args = args[:-1]
        if self._cache.get(args) is None:
            indexes = [self.fields.index(arg) for arg in args]
            self._cache[args] = group(self, indexes, like_items, unique)
        return self._cache[args]
