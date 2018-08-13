import re

from pywikibot import NoPage

from libs.utils.wikibot import load_page, save_page


def remove_stress(value):
    return value.replace('́', '').replace('̀', '').replace('ѐ', 'е').\
        replace('ѝ', 'и')


skip = True
lines = load_page('User:Vesailok/verb4').split('\n')
for line in lines:
    # print(line)
    verb, aspect, verb_stressed = \
        re.match('# \[\[([^]]+)\]\] \((сов|несов)\) (.+)$', line).groups()
    # if verb in ['']:
    #     continue
    if verb != remove_stress(verb_stressed).strip() \
            or '́' not in verb_stressed and 'ё' not in verb_stressed:
        print(verb, verb_stressed)
        raise Exception("Ошибка в данных.")

    # if verb == '...':
    #     skip = False
    # if skip:
    #     continue

    verb_stem = verb_stressed[:-2]  # откусили "ть"
    participle_1 = f'{verb_stem}в'    # добавили "в"
    participle_2 = f'{verb_stem}вши'  # добавили "вши"

    cases = ((participle_1, participle_2), (participle_2, participle_1))
    for first, second in cases:
        title = remove_stress(first)
        content = '{{подст:Участник:Cinemantique/дее|' + \
                  f'{verb}||{first}|{aspect}|{remove_stress(second)}' + \
                  '}}'
        try:
            load_page(title)
            continue
            # desc = 'Обновление деепричастий'
        except NoPage:
            desc = 'Заливка деепричастий'
        save_page(title, content, desc)
