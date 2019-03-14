import re

from libs.parse.data.blocks.detailed.noun import NounData
from libs.parse.sections.template import Template
from libs.utils.lock import locked_repeat
from libs.utils.log import log_exception
from projects.mass_updaters.base import BaseMassUpdater


class NounMorphologyMassUpdater(BaseMassUpdater):
    slug = 'morfol'
    data_page = f"User:Cinemantique/{slug}"
    desc = u'Заполнение шаблона {сущ-ru}'

    allow_several_lines = False

    def check_entry(self, value):
        return re.fullmatch('{{сущ-ru\|[^}]+\}\}', value)

    def process_page(self, page, title, values):
        homonym = page.ru.homonyms.last_list()[0]
        tpls = homonym.morphology.templates(re='сущ ru.*').last_list()
        if not tpls:
            self.report.error(title, 'нет шаблонов {сущ ru}')
            return
        if len(tpls) > 1:
            self.report.error(title, 'несколько шаблонов {сущ ru}')
            return
        tpl = tpls[0]
        if tpl.name not in NounData.tpls_no_index:
            self.report.error(title, 'заполненный шаблон {сущ ru}')
            return

        new_tpl = Template('сущ-ru', values[0])

        new_indexes = {
            'сущ ru m a': 'мо ',
            'сущ ru m ina': 'м ',
            'сущ ru f a': 'жо ',
            'сущ ru f ina': 'ж ',
            'сущ ru n a': 'со ',
            'сущ ru n ina': 'с ',
        }
        if new_tpl[1].startswith(('мо ', 'м ', 'жо ', 'ж ', 'со ', 'с ')):
            new_index = new_indexes.get(tpl.name, '')
            if not new_tpl[1].startswith(new_index):
                self.report.error(title,
                                  'несоответствие рода или одушевлённости')
                return

        if 'слоги' in tpl.kwargs:
            new_tpl['слоги'] = tpl['слоги'].strip()
            del tpl.kwargs['слоги']
        else:
            new_tpl['слоги'] = '{{по-слогам|' + new_tpl[0] + '}}'

        for key in ['основа', 'основа1', 'основа2']:
            if key in tpl.kwargs:
                del tpl.kwargs[key]
        if tpl.kwargs:
            self.report.error(title, 'дополнительные параметры в {сущ ru}')
            return

        homonym.content = homonym.content.replace(
            tpl.content,
            new_tpl.constructed_content()
        )
        return True


@log_exception('loaders/noun_morphology')
@locked_repeat('loaders/noun_morphology')
def noun_morphology_mass_update():
    NounMorphologyMassUpdater().start()


if __name__ == '__main__':
    noun_morphology_mass_update()
