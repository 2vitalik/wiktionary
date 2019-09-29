import platform

from libs.utils.parse import remove_stress
from projects.inflection.modules.py.ru.adj import adj
from projects.inflection.modules.py.ru.noun import noun


def replace_stress(value):
    return value.replace('́', "'")


def run(word, index):
    # result = \
    #     noun.forms(remove_stress(word), {'индекс': index, 'слово': word}, None)
    result = \
        adj.forms(remove_stress(word), {'индекс': index, 'слово': word}, None)

    keys = [
        ('Им.', 'nom-sg', 'nom-pl'),
        ('Р. ', 'gen-sg', 'gen-pl'),
        ('Д. ', 'dat-sg', 'dat-pl'),
        ('В. ', 'acc-sg', 'acc-pl'),
        ('Тв.', 'ins-sg', 'ins-pl'),
        ('Пр.', 'prp-sg', 'prp-pl'),
    ]

    len1 = 0
    len2 = 0
    for _, key1, key2 in keys:
        len1 = max(len1, len(result.get(key1, '-')))
        len2 = max(len2, len(result.get(key2, '-')))

    word_width = len("Слово:  ") + len(word)
    index_width = len("Индекс: ") + len(index)
    cases_width = len1 + len2 + 9
    width = max(cases_width, word_width, index_width) + 2
    len2 = max(len2, width - len1 - 9 - 2)

    # print(platform.platform())
    if platform.platform().startswith('...'):  # just in case, for old OS/font
        tl = '='  # top-left corner
        tr = '='  # top-right corner
        bl = '='  # bottom-left corner
        br = '='  # bottom-right corner
        v = '|'   # vertical line
        vm = '|'  # middle vertical line
        h = '='   # horizontal line
        vl = '|'  # left vertical tee
        vr = '|'  # right vertical tee
        ht = '='  # top horizontal tee
        hb = '='  # bottom horizontal tee
    else:
        tl = '╔'  # top-left corner
        tr = '╗'  # top-right corner
        bl = '╚'  # bottom-left corner
        br = '╝'  # bottom-right corner
        v = '║'   # vertical line
        vm = '│'  # middle vertical line
        h = '═'   # horizontal line
        vl = '╠'  # left vertical tee
        vr = '╣'  # right vertical tee
        ht = '╤'  # top horizontal tee
        hb = '╧'  # bottom horizontal tee

    print()
    print(f'{tl}{h * width}{tr}')
    print(f'{v} Слово:  {replace_stress(word)}{" " * (width-9-len(word))}{v}')
    print(f'{v} Индекс: {index}{" " * (width-9-len(index))}{v}')
    print(f'{vl}{h * 5}{ht}{h * (len1 + 2)}{ht}{h * (len2 + 2)}{vr}')
    for key, key1, key2 in keys:
        print(f'{v} {key} '
              f'{vm} {replace_stress(result.get(key1, "-")).ljust(len1)} '
              f'{vm} {replace_stress(result.get(key2, "-")).ljust(len2)} '
              f'{v}')
    print(f'{bl}{h * 5}{hb}{h * (len1 + 2)}{hb}{h * (len2 + 2)}{br}')
    print()
