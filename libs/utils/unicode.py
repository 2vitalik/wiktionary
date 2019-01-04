import unicodedata

from pyuca import Collator


def char_info(char):
    category = unicodedata.category(char)
    try:
        name = unicodedata.name(char).split(' ')[0]
    except ValueError:
        name = 'UNKNOWN'
    return category, name


def unicode_sorted(iterable):
    return sorted(iterable, key=Collator().sort_key)


if __name__ == '__main__':
    print(unicode_sorted(['Arcis', 'Ārčis', 'Ārcīš', 'Ardī', 'Arcz']))
