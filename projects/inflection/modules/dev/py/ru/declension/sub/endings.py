from projects.inflection.modules.dev.py import a
from projects.inflection.modules.dev.py import mw
from projects.inflection.modules.dev.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...noun import endings as noun_endings
from ...adj import endings as adj_endings
from ...pronoun import endings as pronoun_endings


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'declension.endings'  # local


# Схлопывание: Выбор окончаний в зависимости от рода и типа основы
@a.starts(module)
def get_base_endings(func, gender, base_stem_type, adj, pronoun):
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
        keys = ['nom_sg', 'gen_sg', 'dat_sg', 'ins_sg', 'prp_sg', 'srt_sg']
        for i, key in enumerate(keys):
            standard_endings['common'][base_stem_type][key] = ''
        # end
        _.ends(module, func)
        return standard_endings['common'][base_stem_type]
    # end

    # INFO: Заполнение из общих данных для всех родов:
    for key, value in standard_endings['common'][base_stem_type].items():
        standard_endings[gender][base_stem_type][key] = value
    # end

    # INFO: Возвращение соответствующих окончаний
    _.ends(module, func)
    return standard_endings[gender][base_stem_type]
# end


# Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
@a.starts(module)
def choose_endings_stress(func, endings, gender, base_stem_type, stress_schema, adj, pronoun):
    # local stress, keys

    if adj:
        stress = stress_schema['ending']['nom_sg'] and stressed or unstressed

        if gender == 'm' and base_stem_type == 'hard':
            endings['nom_sg'] = endings['nom_sg'][stress]
        # end

        stress = stress_schema['ending']['srt_sg_n'] and stressed or unstressed

        if gender == 'n' and base_stem_type == 'soft':
            endings['srt_sg'] = endings['srt_sg'][stress]
        # end
    elif pronoun:  # TODO: может применить такой подход для всех случаев вообще?
        keys = ['nom_sg', 'gen_sg', 'dat_sg', 'ins_sg', 'prp_sg']  # list
        for i, key in enumerate(keys):
            if type(endings[key]) == 'table':
                stress = stress_schema['ending'][key] and stressed or unstressed
                endings[key] = endings[key][stress]
            # end
        # end
    else:
        stress = stress_schema['ending']['dat_sg'] and stressed or unstressed

        if gender == 'f' and base_stem_type == 'soft':
            endings['dat_sg'] = endings['dat_sg'][stress]
        # end

        stress = stress_schema['ending']['prp_sg'] and stressed or unstressed

        endings['prp_sg'] = endings['prp_sg'][stress]

        stress = stress_schema['ending']['ins_sg'] and stressed or unstressed

        if base_stem_type == 'soft':
            endings['ins_sg'] = endings['ins_sg'][stress]
        # end

        stress = stress_schema['ending']['gen_pl'] and stressed or unstressed

        endings['gen_pl'] = endings['gen_pl'][stress]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def get_endings(func, data):  # export
    # INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')
    # local endings

    endings = get_base_endings(data.gender, data.base_stem_type, data.adj, data.pronoun)

    # INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
    if data.adj:  # or data.pronoun
        adj_endings.fix_adj_pronoun_endings(endings, data.gender, data.stem_type, data.stress_schema, data.adj, False)
    elif data.pronoun:
        pronoun_endings.fix_pronoun_noun_endings(endings, data.gender, data.stem_type, data.stress_schema)
    else:
        noun_endings.fix_noun_endings(endings, data.gender, data.stem_type, data.stress_schema)
    # end

    # apply special cases (1) or (2) in index
    if not data.adj and not data.pronoun:
        noun_endings.apply_noun_specific_1_2(endings, data.gender, data.stem_type, data.base_stem_type, data.rest_index)
    # end

    # Resolve stressed/unstressed cases of endings
    choose_endings_stress(endings, data.gender, data.base_stem_type, data.stress_schema, data.adj, data.pronoun)

    # INFO: Особые случаи: `копьё с d*` и `питьё с b*`
    if data.gender == 'n' and data.base_stem_type == 'soft' and _.endswith(data.word, 'ё'):
        endings['nom_sg'] = 'ё'
    # end

    _.ends(module, func)
    return endings
# end


# return export
