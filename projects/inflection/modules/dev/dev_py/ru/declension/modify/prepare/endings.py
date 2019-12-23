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
def get_base_endings(func, gender, stem_base_type, adj, pronoun):
    # local standard_endings, keys

    # INFO: Получение списка всех стандартных окончаний
    if adj:
        standard_endings = adj_endings.get_standard_adj_endings()
    elif pronoun:
        standard_endings = pronoun_endings.get_standard_pronoun_noun_endings()
    else:
        standard_endings = noun_endings.get_standard_noun_endings()
    # end

    if adj and gender == '':  # INFO: Случай с множественным числом
        keys = ['nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg', 'srt-sg']
        for i, key in enumerate(keys):
            standard_endings['common'][stem_base_type][key] = ''
        # end
        _.ends(module, func)
        return standard_endings['common'][stem_base_type]
    # end

    # INFO: Заполнение из общих данных для всех родов:
    for key, value in standard_endings['common'][stem_base_type].items():
        standard_endings[gender][stem_base_type][key] = value
    # end

    # INFO: Возвращение соответствующих окончаний
    _.ends(module, func)
    return standard_endings[gender][stem_base_type]
# end


# Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
@a.starts(module)
def choose_endings_stress(func, endings, gender, stem_base_type, stress_schema, adj, pronoun):
    # local stress, keys

    if adj:
        stress = stress_schema['ending']['nom-sg'] and stressed or unstressed

        if gender == 'm' and stem_base_type == 'hard':
            endings['nom-sg'] = endings['nom-sg'][stress]
        # end

        stress = stress_schema['ending']['srt-sg-n'] and stressed or unstressed

        if gender == 'n' and stem_base_type == 'soft':
            endings['srt-sg'] = endings['srt-sg'][stress]
        # end
    elif pronoun:  # TODO: может применить такой подход для всех случаев вообще?
        keys = ['nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg']  # list
        for i, key in enumerate(keys):
            if type(endings[key]) == 'table':
                stress = stress_schema['ending'][key] and stressed or unstressed
                endings[key] = endings[key][stress]
            # end
        # end
    else:
        stress = stress_schema['ending']['dat-sg'] and stressed or unstressed

        if gender == 'f' and stem_base_type == 'soft':
            endings['dat-sg'] = endings['dat-sg'][stress]
        # end

        stress = stress_schema['ending']['prp-sg'] and stressed or unstressed

        endings['prp-sg'] = endings['prp-sg'][stress]

        stress = stress_schema['ending']['ins-sg'] and stressed or unstressed

        if stem_base_type == 'soft':
            endings['ins-sg'] = endings['ins-sg'][stress]
        # end

        stress = stress_schema['ending']['gen-pl'] and stressed or unstressed

        endings['gen-pl'] = endings['gen-pl'][stress]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def get_endings(func, info):  # export
    # INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')
    # local endings

    endings = get_base_endings(info.gender, info.stem.base_type, info.adj, info.pronoun)

    # INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
    if info.adj:  # or info.pronoun
        adj_endings.fix_adj_pronoun_endings(endings, info.gender, info.stem.type, info.stress_schema, info.adj, False)
    elif info.pronoun:
        pronoun_endings.fix_pronoun_noun_endings(endings, info.gender, info.stem.type, info.stress_schema)
    else:
        noun_endings.fix_noun_endings(endings, info.gender, info.stem.type, info.stress_schema)
    # end

    # apply special cases (1) or (2) in index
    if not info.adj and not info.pronoun:  # todo: move outside here (into `modify` package)
        noun_circles.apply_noun_specific_1_2(endings, info.gender, info.stem.type, info.stem.base_type, info.rest_index)
    # end

    # Resolve stressed/unstressed cases of endings
    choose_endings_stress(endings, info.gender, info.stem.base_type, info.stress_schema, info.adj, info.pronoun)

    # INFO: Особые случаи: `копьё с d*` и `питьё с b*`
    if info.gender == 'n' and info.stem.base_type == 'soft' and _.endswith(info.word.unstressed, 'ё'):
        endings['nom-sg'] = 'ё'
    # end

    _.ends(module, func)
    return endings
# end


# return export
