import re

from core.storage.main import storage
from libs.utils.classes import derive
from libs.utils.wikibot import load_page
from libs.utils.wikicode import bold
from projects.reports.lib.complex_report.base import BaseComplexReport
from projects.reports.lib.mixins.key_title import KeyTitle
from projects.reports.lib.mixins.reversed_index import ReversedIndex


class CustomDetails:
    separator = ' '

    @classmethod
    def convert_details(cls, details):
        aspect, stress, participles = details  # unpack
        participles_text = ''
        if participles and participles != '?':
            participles_text = \
                ' → ' + ', '.join([f'[[{participle}]]'
                                   for participle in participles])
        return f'({aspect}) {stress}{participles_text}'


class VerbsWithoutParticiples(BaseComplexReport):
    base_path = 'Отчёты/ru/Глаголы/Без созданных деепричастий'
    base_class = derive(KeyTitle, CustomDetails, ReversedIndex)

    report_keys = [
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
    ]

    def __init__(self):
        super().__init__()
        self.aspects = {}
        for i in range(11):
            if i == 7:
                continue
            lines = load_page(f'User:Vesailok/verb{i}').split('\n')
            for line in lines:
                verb, aspect, verb_stressed = \
                    re.match('# \[\[([^]]+)\]\] \((сов|несов)\) (.+)$', line).\
                    groups()
                # if verb != self.remove_stress(verb_stressed).strip() \
                #         or '́' not in verb_stressed and 'ё' not in verb_stressed:
                #     if verb != verb_stressed:
                #         raise Exception()
                #     print('-', verb)
                #     # raise ImpossibleError(f"Ошибка в данных: {i}/{verb}")
                self.aspects[verb] = aspect

    @classmethod
    def remove_stress(cls, value):
        return value.replace('́', '').replace('̀', '').replace('ѐ', 'е'). \
            replace('ѝ', 'и')

    def description(self, report_key):
        return f'''
            Глаголы на "{bold(report_key)}" без созданных статей-деепричастий, 
            при этом пока учитывается только факт создания статьи, но не её 
            содержимое.
        '''

    def process_page(self, page):
        if '{{гл ru' not in page.ru.content:
            return
        for report_key in self.report_keys:
            if page.title.endswith(report_key[1:]):
                self.process_verb(page, report_key)
                break
        else:
            self.process_verb(page, '-???')

    def process_verb(self, page, report_key):
        aspect = self.get_aspect(page)
        stresses = self.get_stress(page)
        participles_candidates = []

        if re.search('[аеиоуыя]ть$', page.title):
            if aspect == '???':
                aspect = self.aspects.get(page.title, '???')
            stem = page.title[:-2]
            participles_candidates = [f'{stem}в', f'{stem}вши']

        elif re.search('[аеиоуыя]ться$', page.title):
            if aspect == '???':
                base_verb = page.title[:-2]
                aspect = self.aspects.get(base_verb, '???')
            stem = page.title[:-4]
            participles_candidates = [f'{stem}вшись']

        elif page.title.endswith('йти'):
            stem = page.title[:-2]
            participles_candidates = [f'{stem}дя']

        elif page.title.endswith('йтись'):
            stem = page.title[:-4]
            participles_candidates = [f'{stem}дясь']

        elif page.title.endswith('честь'):
            stem = page.title[:-4]
            participles_candidates = [f'{stem}тя']

        elif page.title.endswith('честься'):
            stem = page.title[:-6]
            participles_candidates = [f'{stem}тясь']

        if participles_candidates:
            participles = []
            for participle in participles_candidates:
                if participle not in storage.titles_set:
                    participles.append(participle)
            if not participles:
                return
        else:
            participles = '?'

        self.set(report_key, page.title, (aspect, stresses, participles))

    @classmethod
    def get_aspect(cls, page):
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

    @classmethod
    def get_stress(cls, page):
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
        return ', '.join(stress)


# todo: дополнительно проверять (возможно, для других подотчётов):
# todo:   - страница-редирект, а не полноценная статья
# todo:   - страница есть, но нет омонима-деепричастия
# todo:   - деепричастие есть, но только в виде словоформы
