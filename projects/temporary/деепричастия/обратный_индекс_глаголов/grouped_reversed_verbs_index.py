"""
Описание:
    Глаголы, сгруппированные
Для:
    Vesailok
Результат:
    https://ru.wiktionary.org/wiki/u:Vitalik/reports/verbs (подстраницы)
Тип:
    Отчёты/списки
"""
import json
import re

from datetime import datetime

from core.storage.main import MainStorage
from lib.utils.collection import chunks
from lib.utils.io import write, read
from lib.utils.wikibot import save_page

storage = MainStorage()

endings = {
    'сти': [],
    'стись': [],
    'сть': [],
    'сться': [],

    'чь': [],
    'чься': [],

    'ать': [],
    'еть': [],
    'ить': [],
    'оть': [],
    'уть': [],
    'ыть': [],
    'ють': [],
    'ять': [],
    'аться': [],
    'еться': [],
    'иться': [],
    'оться': [],
    'уться': [],
    'ыться': [],
    'ються': [],
    'яться': [],

    'нуть': [],
    'нуться': [],
    'ереть': [],
    'ереться': [],

    '?': [],
}


def generate_lists():
    started = datetime.now()
    for title, page in storage.iterate_pages(silent=True):
        if ' ' in title:  # пропускаем словосочетания
            continue
        if '{{гл ru' in page.ru.content:
            print(title)

            # вид: совершенный, несовершенный, неизвестный
            unknown = False
            perfective = False
            imperfective = False
            for tpl in page.ru.templates(re='гл ru').values():
                if tpl.name == 'гл ru':
                    unknown = True
                    continue
                if 'СВ' in tpl.name:
                    perfective = True
                else:
                    imperfective = True
            aspect = []
            if perfective:
                aspect.append('сов.')
            if imperfective:
                aspect.append('нес.')
            if unknown:
                aspect.append('??')
            aspect = ', '.join(aspect)

            # ударение из шаблона {{по-слогам}}
            stress = set()
            for tpl in page.ru.templates('по-слогам', 'по слогам').values():
                value = tpl.params.replace('|', '').replace('.', '')
                if not value:
                    continue
                vowel_count = len(re.findall('[аеёиоуыэюя]', value,
                                             re.IGNORECASE))
                if vowel_count == 1 and 'ё' not in value:
                    value = re.sub('([аеиоуыэюя])', '\\1́', value)
                stress.add(value)
            stress = ', '.join(stress)

            # группировка по ударениям
            value = f"# [[{title}]] ({aspect}) {stress}\n"
            added = False
            for ending in endings:
                if title.endswith(ending):
                    endings[ending].append((title, value))
                    added = True
            if not added:
                endings['?'].append((title, value))

    print(datetime.now() - started)
    write('endings_ru_new.json', json.dumps(endings, indent=4))


def save_pages():
    endings = json.loads(read('endings_ru_new.json'))
    for ending, entries in endings.items():
        entries.sort(key=lambda x: x[0][::-1])
        values = [entry[1] for entry in entries]
        for i, chunk in enumerate(chunks(values, 3700)):
            # content = f"= Глаголы на '''-{ending}''' =\n" \
            #           f'<div class="reverseindex">\n' + \
            #           f''.join(chunk) + \
            #           f'</div>'
            content = f"= Глаголы на '''-{ending}''' =\n" + f''.join(chunk)
            save_page(f'User:Vitalik/reports/verbs/-{ending}/{i+1}', content,
                      'Обратный список глаголов по окончаниям')
            print(ending, len(chunk))


if __name__ == '__main__':
    generate_lists()
    save_pages()
