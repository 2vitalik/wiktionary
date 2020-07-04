import re
from collections import defaultdict

from core.reports.lib.large_report.base import BaseLargeReport
from core.reports.lib.large_report.plurals import PluralVerbs
from libs.utils.classes import derive
from libs.utils.collection import chunks
from libs.utils.wikicode import bold
from core.reports.lib.mixins.key_title import KeyTitle
from core.reports.lib.mixins.reversed_index import ReversedIndex


def get_aspect(page):
    # вид: совершенный, несовершенный, неизвестный
    # unknown = False
    perfective = False
    imperfective = False
    for tpl in page.ru.templates(re='гл ru').last_list():
        if tpl.name == 'гл ru':
            # unknown = True
            continue
        if 'НСВ' in tpl.name:
            imperfective = True
        elif 'СВ' in tpl.name:
            perfective = True
        else:
            imperfective = True
    # aspect = []
    if perfective:
        # aspect.append('сов.')
        return 'сов'
    if imperfective:
        # aspect.append('нес.')
        return 'несов'
    # if unknown:
    #     aspect.append('??')
    # aspect = ', '.join(aspect)
    return '???'


def get_stress(page):
    # ударение из шаблона {{по-слогам}}
    stress = set()
    for tpl in page.ru.templates('по-слогам', 'по слогам').last_list():
        value = tpl.params.replace('|', '').replace('.', '')
        if not value:
            continue
        vowel_count = len(re.findall('[аеёиоуыэюя]', value,
                                     re.IGNORECASE))
        if vowel_count == 1 and 'ё' not in value:
            value = re.sub('([аеиоуыэюя])', '\\1́', value)
        stress.add(value)
    return ', '.join(sorted(stress))


class CustomDetails:
    separator = ': '

    @classmethod
    def convert_details(cls, details):
        aspect, stress, impersonal = details  # unpack
        return f'<code>{aspect}</code> {stress}'


class VerbsReversedIndex(KeyTitle, CustomDetails, ReversedIndex,
                         PluralVerbs, BaseLargeReport):
    path = 'Отчёты/ru/Глаголы/Обратный индекс'
    base_class = derive()

    keys = [
        '-ать', '-аться',
        '-ереть', '-ереться',
        '-еть', '-еться',
        '-ить', '-иться',
        '-оть', '-оться',
        '-уть', '-уться',
        '-ыть', '-ыться',
        '-ять', '-яться',
        '-ресть', '-ресться',
        '-честь', '-честься',
        '-сть', '-сться',
        '-сти', '-стись',
        '-чь', '-чься',
        '-зти', '-зтись',
        '-зть', '-зться',
        '-йти', '-йтись',
        '-???',
        '(безличные)',
        '(через дефис)',
    ]

    def get_description(self, report_key):  # todo: move to short_title and make it smarter
        return f'''
            Обратный индекс глаголов на "{bold(report_key)}" 
        '''
        # if sub-page then:
        # ... (начиная на "-лать")

    def group_entries(self):
        grouped = defaultdict(list)
        for title, details in self.entries.items():
            aspect, stress, impersonal = details  # unpack
            if impersonal:
                res_key = '(безличные)'
            elif '-' in title:
                res_key = '(через дефис)'
            else:
                res_key = '-???'
                for key in self.keys:
                    if key.startswith('-') and title.endswith(key[1:]):
                        res_key = key
                        break
            grouped[res_key].append(title)

        for key, entries in grouped.copy().items():
            max_size = 2000
            # todo: implement хитрый алгоритм, разделения на подразделы по удобным разделяющим буквам...
            if len(entries) > max_size:

                for i, chunk in enumerate(chunks(entries, max_size)):
                    new_key = f'{key} @{i+1}'
                    grouped[new_key] = chunk
                del grouped[key]

        def sort_key(pair):
            check_key, value = pair
            if check_key in self.keys:
                return self.keys.index(check_key), 0
            m = re.search('(.*) @(\d+)$', check_key)
            if m:
                check_key, page = m.groups()
                if check_key in self.keys:
                    return self.keys.index(check_key), page
            return float('inf'), check_key

        return dict(sorted(grouped.items(), key=sort_key))

    def check_page(self, page):
        if not page.ru or not page.data.ru.has_verb():
            return
        impersonal = page.data.ru.is_impersonal_verb_only()
        aspect = get_aspect(page)  # todo: use from parsed data algo
        stresses = get_stress(page)
        return aspect, stresses, impersonal


# * -ать
#   * -лать
#   * -рать
#   ...
# * -аться


# * -ать  -- 14234 глаголов
#   * -ать
#   * -лать
#   * -рать
#   ...
# * -аться


# * -ать  -- 14234 глаголов
#   * -ать ... -лать  -- 1234 глагола
#   * -мать ... -пать  -- 231 глагола
#   * -рать ...
#   ...
# * -аться


'''
па-
пб- ... пд-
пе-
пж-
'''
