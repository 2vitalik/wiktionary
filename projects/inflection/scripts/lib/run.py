import platform

from libs.utils.parse import remove_stress
from projects.inflection.modules.py.ru.declension import declension


def replace_stress(value):
    return value.replace('́', "'")


def noun(word, index):
    run('noun',  word, index)


def adj(word, index):
    run('adj',  word, index)


def run(unit, word, index):
    result = declension.forms(
        remove_stress(word),
        {'lang': 'ru',
         'unit': unit,
         'индекс': index,
         'слово': word},
        None,
    )

    if unit == 'adj':
        keys = [
            ('Им.', 'nom-sg-m',   'nom-sg-n', 'nom-sg-f',  'nom-pl'),
            ('Р. ', 'gen-sg-m',   'gen-sg-n', 'gen-sg-f',  'gen-pl'),
            ('Д. ', 'dat-sg-m',   'dat-sg-n', 'dat-sg-f',  'dat-pl'),
            ('В. ', 'acc-sg-m-a', 'acc-sg-n', 'acc-sg-f',  'acc-pl-a'),
            ('В2.', 'acc-sg-m-n', '',         '',          'acc-pl-n'),
            ('Тв.', 'ins-sg-m',   'ins-sg-n', 'ins-sg-f',  'ins-pl'),
            ('Тв2', '',           '',         'ins-sg2-f', ''),
            ('Пр.', 'prp-sg-m',   'prp-sg-n', 'prp-sg-f',  'prp-pl'),
            ('Кр.', 'srt-sg-m',   'srt-sg-n', 'srt-sg-f',  'srt-pl'),
        ]
        lens = [0] * 4
    else:
        keys = [
            ('Им.', 'nom-sg', 'nom-pl'),
            ('Р. ', 'gen-sg', 'gen-pl'),
            ('Д. ', 'dat-sg', 'dat-pl'),
            ('В. ', 'acc-sg', 'acc-pl'),
            ('Тв.', 'ins-sg', 'ins-pl'),
            ('Пр.', 'prp-sg', 'prp-pl'),
        ]
        lens = [0] * 2

    for _, *sub_keys in keys:
        for i, key in enumerate(sub_keys):
            lens[i] = max(lens[i], len(result.get(key, '-')))

    word_width = len("Слово:  ") + len(word)
    index_width = len("Индекс: ") + len(index)
    cases_width = sum(lens) + 9
    width = max(cases_width, word_width, index_width) + 2 + (6 if unit == 'adj' else 0)
    # len2 = max(len2, width - len1 - 9 - 2)  # fixme

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
    print(f'{vl}{h * 5}', end='')
    for i in range(len(keys[0]) - 1):
        print(f'{ht}{h * (lens[i] + 2)}', end='')
    print(f'{vr}')
    for key, *sub_keys in keys:
        print(f'{v} {key} ', end='')
        for i, sub_key in enumerate(sub_keys):
            print(f'{vm} {replace_stress(result.get(sub_key, "-")).ljust(lens[i])} ', end='')
        print(f'{v}')
    print(f'{bl}{h * 5}', end='')
    for i in range(len(keys[0]) - 1):
        print(f'{hb}{h * (lens[i] + 2)}', end='')
    print(f'{br}')
    print()
