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

from datetime import datetime

from core.reports.reports.ru.verbs.without_participles import get_aspect, \
    get_stress
from core.storage.main import MainStorage
from libs.utils.collection import chunks
from libs.utils.io import write, read
from libs.utils.wikibot import save_page

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
            aspect = get_aspect(page)

            # ударение из шаблона {{по-слогам}}
            stress = get_stress(page)

            # группировка по окончаниям
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
