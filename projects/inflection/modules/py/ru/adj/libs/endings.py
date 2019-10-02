from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


# constants:
# local unstressed, stressed
unstressed = 0
stressed = 1


# Данные: все стандартные окончания для двух типов основ
def get_standard_adj_endings():
    _.log_func('endings', 'get_standard_adj_endings')

    # TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
    return dict(
        m = dict(
            hard = dict(
                nom_sg = ['ый', 'ой'],
                gen_sg = 'ого',
                dat_sg = 'ому',
                ins_sg = 'ым',
                prp_sg = 'ом',
                srt_sg = '',
            ),  # dict
            soft = dict(
                nom_sg = 'ий',
                gen_sg = 'его',
                dat_sg = 'ему',
                ins_sg = 'им',
                prp_sg = 'ем',
                srt_sg = 'ь',
            ),  # dict
        ),  # dict
        f = dict(
            hard = dict(
                nom_sg = 'ая',
                gen_sg = 'ой',
                dat_sg = 'ой',
                acc_sg = 'ую',
                ins_sg = 'ой',
                prp_sg = 'ой',
                srt_sg = 'о',
            ),  # dict
            soft = dict(
                nom_sg = 'яя',
                gen_sg = 'ей',
                dat_sg = 'ей',
                acc_sg = 'юю',
                ins_sg = 'ей',
                prp_sg = 'ей',
                srt_sg = ['е', 'ё'],
            ),  # dict
        ),  # dict
        n = dict(
            hard = dict(
                nom_sg = 'ое',
                gen_sg = 'ого',
                dat_sg = 'ому',
                ins_sg = 'ым',
                prp_sg = 'ом',
                srt_sg = 'а',
            ),  # dict
            soft = dict(
                nom_sg = 'ее',
                gen_sg = 'его',
                dat_sg = 'ему',
                ins_sg = 'им',
                prp_sg = 'ем',
                srt_sg = 'я',
            ),  # dict
        ),  # dict
        common = dict(  # common endings
            hard = dict(
                nom_pl = 'ые',
                gen_pl = 'ых',
                dat_pl = 'ым',
                ins_pl = 'ыми',
                prp_pl = 'ых',
                srt_pl = 'ы',
            ),  # dict
            soft = dict(
                nom_pl = 'ие',
                gen_pl = 'их',
                dat_pl = 'им',
                ins_pl = 'ими',
                prp_pl = 'их',
                srt_pl = 'и',
            ),  # dict
        ),  # dict
    )  # dict
    # todo: сразу преобразовать в дефисы
# end


# Схлопывание: Выбор окончаний в зависимости от рода и типа основы
def get_base_endings(gender, base_stem_type, adj, pronoun):
    _.log_func('endings', 'get_base_endings')

    # local standard_endings, keys

    # INFO: Получение списка всех стандартных окончаний
    if adj:
        standard_endings = get_standard_adj_endings()
    elif pronoun:
        standard_endings = get_standard_pronoun_noun_endings()  # fixme
    else:
        standard_endings = get_standard_noun_endings()  # fixme
    # end

    if adj and gender == '':  # INFO: Случай с множественным числом
        keys = ['nom_sg', 'gen_sg', 'dat_sg', 'ins_sg', 'prp_sg', 'srt_sg']
        for i, key in enumerate(keys):
            standard_endings['common'][base_stem_type][key] = ''
        # end
        return standard_endings['common'][base_stem_type]
    # end

    # INFO: Заполнение из общих данных для всех родов:
    for key, value in standard_endings['common'][base_stem_type].items():
        standard_endings[gender][base_stem_type][key] = value
    # end

    # INFO: Возвращение соответствующих окончаний
    return standard_endings[gender][base_stem_type]
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
def fix_adj_pronoun_endings(endings, gender, stem_type, stress_schema, adj, pronoun):
    _.log_func('endings', 'fix_adj_pronoun_endings')

    # INFO: Replace "ы" to "и"
    if _.equals(stem_type, ['velar', 'sibilant']):
        if gender == 'm':
            if adj:
                endings['nom_sg'][unstressed] = 'ий'
            # end
            endings['ins_sg'] = 'им'
        # end
        if gender == 'n':
            endings['ins_sg'] = 'им'
        # end

        if adj:
            endings['nom_pl'] = 'ие'
        elif pronoun:
            endings['nom_pl'] = 'и'
        # end
        endings['gen_pl'] = 'их'
        endings['dat_pl'] = 'им'
        endings['ins_pl'] = 'ими'
        endings['prp_pl'] = 'их'
        if adj:
            endings['srt_pl'] = 'и'
        # end
    # end

    # INFO: Replace unstressed "о" to "е"
    if _.equals(stem_type, ['sibilant', 'letter-ц']):
        if not stress_schema['ending']['sg']:
            if gender == 'm':
                if adj:
                    endings['nom_sg'][stressed] = 'ей'
                # end
                endings['gen_sg'] = 'его'
                endings['dat_sg'] = 'ему'
                endings['prp_sg'] = 'ем'
            # end
            if gender == 'n':
                endings['nom_sg'] = 'ее'
                endings['gen_sg'] = 'его'
                endings['dat_sg'] = 'ему'
                endings['prp_sg'] = 'ем'
            # end
            if gender == 'f':
                endings['gen_sg'] = 'ей'
                endings['dat_sg'] = 'ей'
                endings['ins_sg'] = 'ей'
                endings['prp_sg'] = 'ей'
            # end
        # end
        if not stress_schema['ending']['srt_sg_n']:
            if gender == 'n':
                if adj:
                    endings['srt_sg'] = 'е'
                # end
            # end
        # end
    # end

    # INFO: Replace "ь" to "й"
    if _.equals(stem_type, {'vowel'}):
        if gender == 'm':
            if adj:
                endings['srt_sg'] = 'й'
            # end
        # end
    # end
# end


# Изменение окончаний для случаев (1), (2), (3)
def apply_specific_1_2(endings, gender, stem_type, base_stem_type, rest_index, adj, pronoun):
    _.log_func('endings', 'apply_specific_1_2')

    if adj or pronoun:
        pass  # TODO

    else:
        pass  # nouns part deleted from here
    # end
# end


# Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
def choose_endings_stress(endings, gender, base_stem_type, stress_schema, adj, pronoun):
    _.log_func('endings', 'choose_endings_stress')

    # local stress

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
        # local keys = ['nom_sg', 'gen_sg', 'dat_sg', 'ins_sg', 'prp_sg', 'srt_sg']
        for i, key in keys.items():
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
# end


def get_endings(data):  # export
    _.log_func('endings', 'get_endings')

    # INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')
    # local endings

    endings = get_base_endings(data.gender, data.base_stem_type, data.adj, data.pronoun)

    # INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
    if data.adj:  # or data.pronoun
        fix_adj_pronoun_endings(endings, data.gender, data.stem_type, data.stress_schema, data.adj, False)
    elif data.pronoun:
        fix_pronoun_noun_endings(endings, data.gender, data.stem_type, data.stress_schema)  # fixme
    else:
        fix_noun_endendings(endings, data.gender, data.stem_type, data.stress_schema)  # fixme
    # end

    # apply special cases (1) or (2) in index
    apply_specific_1_2(endings, data.gender, data.stem_type, data.base_stem_type, data.rest_index, data.adj, data.pronoun)

    # Resolve stressed/unstressed cases of endings
    choose_endings_stress(endings, data.gender, data.base_stem_type, data.stress_schema, data.adj, data.pronoun)

    # INFO: Особые случаи: `копьё с d*` и `питьё с b*`
    if data.gender == 'n' and data.base_stem_type == 'soft' and _.endswith(data.word, 'ё'):
        endings['nom_sg'] = 'ё'
    # end

    return endings
# end


# return export
