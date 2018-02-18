from collections import Counter

from lib.utils.timing import timing
from lib.utils.unicode import char_info
from lib.storage.const import MAX_DEPTH


class StructureBuilder:
    def __init__(self, titles, max_count):
        self.titles = titles
        self.max_count = max_count
        self.char_info = {}
        self.structure = {}

        # counters:
        self.categories = Counter()
        self.names = Counter()
        self.prefixes = {i: Counter() for i in range(1, MAX_DEPTH)}

        self.calculate_counters()
        self.build_structure()
        self.fill_structure()

    @timing
    def calculate_counters(self):
        for title in self.titles:
            letter = title[0]
            category, name = char_info(letter)
            self.char_info[letter] = (category, name)

            self.categories[category] += 1
            self.names[(category, name)] += 1

            for i in range(1, MAX_DEPTH):
                if len(title) >= i:
                    prefix = title[:i]
                    self.prefixes[i][prefix] += 1

    @timing
    def build_structure(self):
        for category, count in self.categories.items():
            if count > self.max_count:
                self.structure[category] = {}

        for (category, name), count in self.names.items():
            category_dict = self.structure.get(category)
            if count > self.max_count:
                category_dict[name] = {}

        for i in range(1, MAX_DEPTH):
            for prefix, count in self.prefixes[i].items():
                if i == 1:
                    base_dict = self.name_dict(prefix)
                else:
                    base_dict = self.prefix_dict(prefix)
                if count > self.max_count:
                    base_dict[prefix] = {}

    def name_dict(self, letter):
        category, name = self.char_info[letter]
        category_dict = self.structure.get(category) or {}
        return category_dict.get(name)

    def prefix_dict(self, prefix):
        i = len(prefix)
        base_prefix = prefix[:(i - 1)]
        if i == 2:
            base_dict = self.name_dict(base_prefix) or {}
        else:
            base_dict = self.prefix_dict(base_prefix) or {}
        return base_dict.get(base_prefix)

    @timing
    def fill_structure(self):
        for title in self.titles:
            block = self.get_block(title)
            if block is None:  # todo: remove this?
                continue
            block.append(title)

    def get_block(self, title):
        def is_block(_dict, key):
            if key not in _dict:
                _dict[key] = list()
            return type(_dict[key]) == list

        category, name = self.char_info[title[0]]
        if is_block(self.structure, category):
            return self.structure[category]

        names = self.structure[category]
        if is_block(names, name):
            return names[name]

        prefixes = names[name]
        for i in range(1, MAX_DEPTH):
            prefix = title[:i]
            if is_block(prefixes, prefix):
                return prefixes[prefix]

            prefixes = prefixes[prefix]

        # todo: return `prefixes`?
