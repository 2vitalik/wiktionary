import re

from core.storage.main import storage
from libs.parse.storage_page import StoragePage
from libs.utils.classes import derive
from libs.utils.wikibot import load_page
from libs.utils.wikicode import bold
from core.reports.lib.complex_report.base import BaseComplexReport
from core.reports.lib.mixins.key_title import KeyTitle
from core.reports.lib.mixins.reversed_index import ReversedIndex


def remove_stress(value):
    return value.replace('́', '').replace('̀', '').replace('ѐ', 'е'). \
        replace('ѝ', 'и')


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


def case_ch(title):  # -чь
    if title.endswith(('ячь', 'я́чь')):
        stem = title[:-2]
        return [f'{stem}гши']
    if title.endswith(('ичь', 'и́чь')):
        stem = title[:-2]
        return [f'{stem}гши']
    if title.endswith(('мочь', 'мо́чь')):
        stem = title[:-2]
        return [f'{stem}гши']
    if title.endswith(('очь', 'о́чь')):
        stem = title[:-2]
        return [f'{stem}кши']
    if title.endswith(('ечь', 'е́чь')):
        vowel = 'е' if title.startswith('вы') else 'ё'
        cases = {
            'жечь': f'ж{vowel}гши',
            'блечь': f'бл{vowel}кши',
            'влечь': f'вл{vowel}кши',
            'лечь': f'л{vowel}гши',
            'печь': f'п{vowel}кши',
            'еречь': f'ер{vowel}гши',
            'речь': f'р{vowel}кши',
            'сечь': f'с{vowel}кши',
            'течь': f'т{vowel}кши',
        }
        for end, replace in cases.items():
            if title.endswith(end):
                stem = title[:-len(end)]
                return [f'{stem}{replace}']
            end_stressed = end.replace('ечь', 'е́чь')
            if title.endswith(end_stressed):
                if vowel != 'ё':
                    raise Exception('Never should happen? Or process with it?')
                stem = title[:-len(end_stressed)]
                return [f'{stem}{replace}']
        return ['???']
    return ['???']


def case_zti(title, aspect='???'):  # -зти
    if title.endswith('лзти'):
        stem = title[:-4]
        return [f'{stem}лзши']
    if title.endswith('езти'):
        stem = title[:-4]
        if aspect == 'несов':
            return [f'{stem}ёзши']
        if aspect == 'сов':
            if title.startswith(('вы', 'повы')):
                return [f'{stem}езя', f'{stem}езши']
            else:
                return [f'{stem}езя́', f'{stem}ёзши']
        return ['???']
    return ['???']


def get_participles(title, aspect='???'):
    if re.search('[аеиоуыя]ть$', title):
        stem = title[:-2]
        return [f'{stem}в', f'{stem}вши']
    if re.search('[аеиоуыя]ться$', title):
        stem = title[:-4]
        return [f'{stem}вшись']

    if re.search('зть$', title):
        stem = title[:-3]
        return [f'{stem}зши']
    if re.search('зться$', title):
        stem = title[:-5]
        return [f'{stem}зшись']

    # if title.endswith('йти'):
    #     stem = title[:-3]
    #     return [f'{stem}йдя', f'{stem}шедши']
    if title.endswith('йтись'):
        stem = title[:-5]
        return [f'{stem}йдясь']

    # if title.endswith('честь'):
    #     stem = title[:-5]
    #     return [f'{stem}чтя', f'{stem}чётши']
    # if title.endswith('честься'):
    #     stem = title[:-7]
    #     return [f'{stem}чтясь', '???']

    if title.endswith('чь'):
        return case_ch(title)

    if title.endswith('чься'):
        entries = case_ch(title[:-2])
        for i, entry in enumerate(entries):
            if entry != '???':
                entries[i] += 'сь'
        return entries

    if title.endswith('зти'):
        return case_zti(title, aspect)

    if title.endswith('зтись'):
        entries = case_zti(title[:-2], aspect)
        for i, entry in enumerate(entries):
            if entry != '???':
                entries[i] += 'сь'
        return entries

    return []


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

    def process_page(self, page):
        if '{{гл ru' not in page.ru.content:
            return
        if page.data.ru.is_impersonal_verb_only():
            self.remove_page(page.title)
            self.process_verb(page, '(безличные)', skip_candidates=True)  # todo: move inside `process_verb, чтобы как-то показывать кандидатов всегда?
            return
        if '-' in page.title:
            self.remove_page(page.title)
            self.process_verb(page, '(через дефис)', skip_candidates=True)  # todo: move inside `process_verb, но кандидатов не показывать по проверке на дефис
            return
        for report_key in self.report_keys:
            if report_key.startswith('-') \
                    and page.title.endswith(report_key[1:]):
                self.process_verb(page, report_key)
                break
        else:
            self.process_verb(page, '-???')

    def process_verb(self, page, report_key, skip_candidates=False):
        aspect = get_aspect(page)
        stresses = get_stress(page)

        if re.search('[аеиоуыя]ть$', page.title):
            if aspect == '???':
                aspect = self.aspects.get(page.title, '???')
        elif re.search('[аеиоуыя]ться$', page.title):
            if aspect == '???':
                base_verb = page.title[:-2]
                aspect = self.aspects.get(base_verb, '???')

        participles_candidates = get_participles(page.title, aspect)
        if participles_candidates and not skip_candidates:
            participles = []
            for participle in participles_candidates:
                participle = remove_stress(participle)
                if participle not in storage.titles_set:  # todo: отдельный отчёт для articles_set (т.е. когда редирект)
                    participles.append(participle)
            if not participles:
                self.set(report_key, page.title, None)
                return
        else:
            participles = '?'

        self.set(report_key, page.title, (aspect, stresses, participles))


# todo: дополнительно проверять (возможно, для других подотчётов):
# todo:   - страница-редирект, а не полноценная статья
# todo:   - страница есть, но нет омонима-деепричастия
# todo:   - деепричастие есть, но только в виде словоформы
