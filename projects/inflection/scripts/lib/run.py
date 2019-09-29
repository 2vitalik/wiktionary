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
            ('Им.', 'm_nom_sg', 'n_nom_sg', 'f_nom_sg', 'nom_pl'),
            ('Р. ', 'm_gen_sg', 'n_gen_sg', 'f_gen_sg', 'gen_pl'),
            ('Д. ', 'm_dat_sg', 'n_dat_sg', 'f_dat_sg', 'dat_pl'),
            ('В. ', 'm_acc_sg', 'n_acc_sg', 'f_acc_sg', 'acc_pl'),
            ('Тв.', 'm_ins_sg', 'n_ins_sg', 'f_ins_sg', 'ins_pl'),
            ('Пр.', 'm_prp_sg', 'n_prp_sg', 'f_prp_sg', 'prp_pl'),
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
