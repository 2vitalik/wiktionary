from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...data.endings import adj as adj_endings
from ...data.endings import pronoun as pronoun_endings
from ...data.endings import noun as noun_endings
from ...modify.transform.circles import noun as noun_circles


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'modify.prepare.endings'  # local


# Схлопывание: Выбор окончаний в зависимости от рода и типа основы
@a.starts(module)
def get_base_endings(func, i):
    # local standard_endings, keys

    # INFO: Получение списка всех стандартных окончаний
    if i.adj:
        standard_endings = adj_endings.get_standard_adj_endings()
    elif i.pronoun:
        standard_endings = pronoun_endings.get_standard_pronoun_noun_endings()
    else:
        standard_endings = noun_endings.get_standard_noun_endings()
    # end

    if i.adj and i.gender == '':  # INFO: Случай с множественным числом
        keys = ['nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg', 'srt-sg']
        for j, key in enumerate(keys):
            standard_endings['common'][i.stem.base_type][key] = ''
        # end
        _.ends(module, func)
        return standard_endings['common'][i.stem.base_type]
    # end

    # INFO: Заполнение из общих данных для всех родов:
    for key, value in standard_endings['common'][i.stem.base_type].items():
        standard_endings[i.gender][i.stem.base_type][key] = value
    # end

    # INFO: Возвращение соответствующих окончаний
    _.ends(module, func)
    return standard_endings[i.gender][i.stem.base_type]
# end


# Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
@a.starts(module)
def choose_endings_stress(func, i):
    # local stress
    d = i.data  # local

    if adj:
        stress = stress_schema['ending']['nom-sg'] and stressed or unstressed

        if i.gender == 'm' and i.stem.base_type == 'hard':
            d.endings['nom-sg'] = d.endings['nom-sg'][stress]
        # end

        stress = i.stress_schema['ending']['srt-sg-n'] and stressed or unstressed

        if i.gender == 'n' and i.stem.base_type == 'soft':
            d.endings['srt-sg'] = d.endings['srt-sg'][stress]
        # end
    elif i.pronoun:  # TODO: может применить такой подход для всех случаев вообще?
        keys = ['nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg']  # list  # local
        for j, key in enumerate(keys):
            if type(d.endings[key]) == 'table':
                stress = i.stress_schema['ending'][key] and stressed or unstressed
                d.endings[key] = d.endings[key][stress]
            # end
        # end
    else:
        stress = i.stress_schema['ending']['dat-sg'] and stressed or unstressed

        if i.gender == 'f' and i.stem.base_type == 'soft':
            d.endings['dat-sg'] = d.endings['dat-sg'][stress]
        # end

        stress = i.stress_schema['ending']['prp-sg'] and stressed or unstressed

        d.endings['prp-sg'] = d.endings['prp-sg'][stress]

        stress = i.stress_schema['ending']['ins-sg'] and stressed or unstressed

        if i.stem.base_type == 'soft':
            d.endings['ins-sg'] = d.endings['ins-sg'][stress]
        # end

        stress = i.stress_schema['ending']['gen-pl'] and stressed or unstressed

        d.endings['gen-pl'] = d.endings['gen-pl'][stress]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def get_endings(func, i):  # export
    # INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')

    d = i.data  # local

    d.endings = get_base_endings(i)

    # INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
    if i.adj:  # or info.pronoun
        adj_endings.fix_adj_pronoun_endings(i, False)
    elif i.pronoun:
        pronoun_endings.fix_pronoun_noun_endings(i)
    else:
        noun_endings.fix_noun_endings(i)
    # end

    # apply special cases (1) or (2) in index
    if not i.adj and not i.pronoun:  # todo: move outside here (into `modify` package)
        noun_circles.apply_noun_specific_1_2(i)
    # end

    # Resolve stressed/unstressed cases of endings
    choose_endings_stress(i)

    # INFO: Особые случаи: `копьё с d*` и `питьё с b*`
    if i.gender == 'n' and i.stem.base_type == 'soft' and _.endswith(i.word.unstressed, 'ё'):
        d.endings['nom-sg'] = 'ё'
    # end

    _.ends(module, func)
# end


# return export
