from libs.utils.debug import debug


class DeepIterator:
    def deep(self, levels=1):
        self._debug(levels)
        if levels == 1:
            yield from self.deep_iterate_1()
        elif levels == 2:
            yield from self.deep_iterate_2()
        elif levels == 3:
            yield from self.deep_iterate_3()
        elif levels == 4:
            yield from self.deep_iterate_4()

    def deep_iterate_1(self):
        for key1, value1 in self:
            yield key1, value1

    def deep_iterate_2(self):
        for key1, value1 in self:
            for key2, value2 in value1:
                yield (key1, key2), value2

    def deep_iterate_3(self):
        for key1, value1 in self:
            for key2, value2 in value1:
                for key3, value3 in value2:
                    yield (key1, key2, key3), value3

    def deep_iterate_4(self):
        for key1, value1 in self:
            for key2, value2 in value1:
                for key3, value3 in value2:
                    for key4, value4 in value3:
                        yield (key1, key2, key3, key4), value4

    @debug
    def _debug(self, levels):
        class_name = type(self).__name__
        print(f'- Started DeepIterator.deep() for {class_name}'
              f' with levels={levels}')
