import platform

from libs.utils.parse import remove_stress
from projects.inflection.modules.py.ru.adj import adj
from projects.inflection.modules.py.ru.noun import noun


def replace_stress(value):
    return value.replace('́', "'")


run_adj = True
# run_adj = False


def run(word, index):
    if run_adj:
        result = adj.forms(remove_stress(word),
                           {'индекс': index, 'слово': word}, None)
    else:
        result = noun.forms(remove_stress(word),
                            {'индекс': index, 'слово': word}, None)

    if run_adj:
        keys = [
            ('Им.', 'nom_sg_m', 'nom_sg_n', 'nom_sg_f', 'nom_pl'),
            ('Р. ', 'gen_sg_m', 'gen_sg_n', 'gen_sg_f', 'gen_pl'),
            ('Д. ', 'dat_sg_m', 'dat_sg_n', 'dat_sg_f', 'dat_pl'),
            ('В. ', 'acc_sg_m', 'acc_sg_n', 'acc_sg_f', 'acc_pl'),
            ('Тв.', 'ins_sg_m', 'ins_sg_n', 'ins_sg_f', 'ins_pl'),
            ('Пр.', 'prp_sg_m', 'prp_sg_n', 'prp_sg_f', 'prp_pl'),
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
    width = max(cases_width, word_width, index_width) + 2 + (6 if run_adj else 0)
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
