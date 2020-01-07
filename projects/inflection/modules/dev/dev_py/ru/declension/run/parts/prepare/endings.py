from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from shared_utils.io.json import json_load
from ....run.parts.transform.circles import noun as noun_circles


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'run.parts.prepare.endings'  # local


# Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
@a.starts(module)
def choose_endings_stress(func, i):
    p = i.parts  # local

    keys = [  # local
        'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',  # 'srt-sg',
        'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',  # 'srt-pl',
    ]  # list
    for j, key in enumerate(keys):
        if _.has_key(p.endings, key) and type(p.endings[key]) == list:  # type
            stress = i.stress_schema['ending'][key] and stressed or unstressed  # local
            p.endings[key] = p.endings[key][stress]
        # end
    # end

    if i.adj and i.gender == 'n':
        stress = i.stress_schema['ending']['srt-sg-n'] and stressed or unstressed  # local
        p.endings['srt-sg'] = p.endings['srt-sg'][stress]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def get_endings(func, i):  # export
    # INFO: Выбор базовых окончаний по роду и типу основы ('1-hard' или '2-soft')

    p = i.parts  # local

    unit = ''  # todo: get from i.unit ?
    if i.adj:
        unit = 'adj'
    elif i.pronoun:
        unit = 'pronoun'
    else:
        unit = 'noun'
    # end
    _.log_value(unit, 'unit')
    _.log_value(i.unit, 'i.unit')

    all_endings = json_load('../modules/dev/dev_py/ru/declension/data/endings/' + unit + '.json')
    endings = all_endings[i.gender][i.stem.type]  # local

    # клонирование окончаний
    # через mw.clone не работает, ошибка: "table from mw.loadData is read-only"
    p.endings = dict()  # dict
    for key, value in endings.items():
        p.endings[key] = value
    # end

    if i.unit == 'noun' and i.adj:
        # для случая адъективного склонения существительных
        # нужно добавить не только текущий род, но и множественное число
        for key, value in all_endings['pl'][i.stem.type].items():
            p.endings[key] = value
        # end
    # end

    # стр. 29: для 8-го типа склонения:
    # после шипящих `я` в окончаниях существительных заменяется на `а`
    if i.stem.type == '8-third' and _.endswith(i.stem.unstressed, '[жчшщ]'):
        p.endings['dat-pl'] = 'ам'
        p.endings['ins-pl'] = 'ами'
        p.endings['prp-pl'] = 'ах'
    # end

    # apply special cases (1) or (2) in index
    if not i.adj and not i.pronoun:  # todo: move outside here (into `modify` package)
        noun_circles.apply_noun_specific_1_2(i)
    # end

    # Resolve stressed/unstressed cases of endings
    choose_endings_stress(i)

    # INFO: Особые случаи: `копьё с d*` и `питьё с b*`
    if i.gender == 'n' and i.stem.base_type == '2-soft' and _.endswith(i.word.unstressed, 'ё'):
        p.endings['nom-sg'] = 'ё'
    # end

    _.ends(module, func)
# end


# return export
