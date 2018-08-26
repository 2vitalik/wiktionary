import re

from core.storage.main import storage
from libs.parse.storage_page import StoragePage
from libs.utils.classes import derive
from libs.utils.wikibot import load_page
from libs.utils.wikicode import bold
from core.reports.lib.complex_report.base import BaseComplexReport
from core.reports.lib.mixins.key_title import KeyTitle
from core.reports.lib.mixins.reversed_index import ReversedIndex


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
        '(безличные)',
        '(через дефис)',
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

    def try_process_source_verb(self, title):
        verb_candidate = self.try_source_verb(title)
        if not verb_candidate:
            return False
        self.process_page(StoragePage(verb_candidate, silent=True),
                          via_recent=False)
        return True

    def process_page(self, page, via_recent):
        if via_recent and self.try_process_source_verb(page.title):
            return
        if '{{гл ru' not in page.ru.content:
            return
        if page.data.ru.is_impersonal_verb_only():
            self.remove_page(page.title, via_recent=False)
            self.process_verb(page, '(безличные)', skip_candidates=True)
            return
        if '-' in page.title:
            self.remove_page(page.title, via_recent=False)
            self.process_verb(page, '(через дефис)', skip_candidates=True)
            return
        for report_key in self.report_keys:
            if report_key.startswith('-') \
                    and page.title.endswith(report_key[1:]):
                self.process_verb(page, report_key)
                break
        else:
            self.process_verb(page, '-???')

    def remove_page(self, title, via_recent):
        super().remove_page(title, via_recent)
        if via_recent:
            self.try_process_source_verb(title)

    @classmethod
    def try_source_verb(cls, title):
        replaces = {
            'в': 'ть',
            'вши': 'ть',
            'вшись': 'ться',
            'йдя': 'йти',
            'шедши': 'йти',
            'йдясь': 'йтись',
            'чтя': 'честь',
            'чётши': 'честь',
            'чтясь': 'честься',
        }
        for ends, replace in replaces.items():
            if title.endswith(ends):
                stem = title[:-len(ends)]
                return f'{stem}{replace}'

    @classmethod
    def process_candidates(cls, title):
        if re.search('[аеиоуыя]ть$', title):
            stem = title[:-2]
            return [f'{stem}в', f'{stem}вши']
        if re.search('[аеиоуыя]ться$', title):
            stem = title[:-4]
            return [f'{stem}вшись']
        if title.endswith('йти'):
            stem = title[:-3]
            return [f'{stem}йдя', f'{stem}шедши']
        if title.endswith('йтись'):
            stem = title[:-5]
            return [f'{stem}йдясь']
        if title.endswith('честь'):
            stem = title[:-5]
            return [f'{stem}чтя', f'{stem}чётши']
        if title.endswith('честься'):
            stem = title[:-7]
            return [f'{stem}чтясь', '???']
        return []

    def process_verb(self, page, report_key, skip_candidates=False):
        aspect = self.get_aspect(page)
        stresses = self.get_stress(page)

        if re.search('[аеиоуыя]ть$', page.title):
            if aspect == '???':
                aspect = self.aspects.get(page.title, '???')
        elif re.search('[аеиоуыя]ться$', page.title):
            if aspect == '???':
                base_verb = page.title[:-2]
                aspect = self.aspects.get(base_verb, '???')

        participles_candidates = self.process_candidates(page.title)
        if participles_candidates and not skip_candidates:
            participles = []
            for participle in participles_candidates:
                if participle not in storage.titles_set:  # todo: отдельный отчёт для articles_set (т.е. когда редирект)
                    participles.append(participle)
            if not participles:
                self.set(report_key, page.title, None)
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
        return ', '.join(sorted(stress))


# todo: дополнительно проверять (возможно, для других подотчётов):
# todo:   - страница-редирект, а не полноценная статья
# todo:   - страница есть, но нет омонима-деепричастия
# todo:   - деепричастие есть, но только в виде словоформы
