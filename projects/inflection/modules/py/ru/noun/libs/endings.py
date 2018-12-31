from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


# constants:
# local unstressed, stressed
unstressed = 0
stressed = 1


# Данные: все стандартные окончания для двух типов основ
def get_standard_noun_endings():
    # TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
    return dict(
        m = dict(  # стандартные окончания мужского рода
            hard = dict(
                nom_sg = '',
                gen_sg = 'а',
                dat_sg = 'у',
                ins_sg = 'ом',
                nom_pl = 'ы',
                gen_pl = ['ов', 'ов'],  # TODO: possibly we can join them together again: m_hard_gen_pl stressed and unstressed
            ),  # dict
            soft = dict(
                nom_sg = 'ь',
                gen_sg = 'я',
                dat_sg = 'ю',
                ins_sg = ['ем', 'ём'],
                nom_pl = 'и',
                gen_pl = ['ей', 'ей'],
            ),  # dict
        ),  # dict
        f = dict(  # стандартные окончания женского рода
            hard = dict(
                nom_sg = 'а',
                gen_sg = 'ы',
                dat_sg = 'е',
                acc_sg = 'у',
                ins_sg = 'ой',
                nom_pl = 'ы',
                gen_pl = ['', ''],
            ),  # dict
            soft = dict(
                nom_sg = 'я',
                gen_sg = 'и',
                dat_sg = ['е', 'е'],
                acc_sg = 'ю',
                ins_sg = ['ей', 'ёй'],
                nom_pl = 'и',
                gen_pl = ['ь', 'ей'],
            ),  # dict
        ),  # dict
        n = dict(  # стандартные окончания среднего рода
            hard = dict(
                nom_sg = 'о',
                gen_sg = 'а',
                dat_sg = 'у',
                ins_sg = 'ом',
                nom_pl = 'а',
                gen_pl = ['', ''],
            ),  # dict
            soft = dict(
                nom_sg = 'е',  # was: ['е', 'ё']
                gen_sg = 'я',
                dat_sg = 'ю',
                ins_sg = ['ем', 'ём'],
                nom_pl = 'я',
                gen_pl = ['ь', 'ей'],
            ),  # dict
        ),  # dict
        common = dict(  # common endings
            hard = dict(
                prp_sg = ['е', 'е'],
                dat_pl = 'ам',
                ins_pl = 'ами',
                prp_pl = 'ах',
            ),  # dict
            soft = dict(
                prp_sg = ['е', 'е'],
                dat_pl = 'ям',
                ins_pl = 'ями',
                prp_pl = 'ях',
            ),  # dict
        )  # dict
    )  # dict
    # todo: сразу преобразовать в дефисы
# end


# Данные: все стандартные окончания для двух типов основ
def get_standard_adj_endings():
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


def get_standard_pronoun_endings():

    # TODO: Пока что не используется

    # TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
    return dict(
        m = dict(
            hard = dict(
                nom_sg = '',
                gen_sg = 'ого',
                dat_sg = 'ому',
                ins_sg = 'ым',
                prp_sg = 'ом',
            ),  # dict
            soft = dict(
                nom_sg = 'ь',
                gen_sg = 'его',
                dat_sg = 'ему',
                ins_sg = 'им',
                prp_sg = ['ем', 'ём'],
            ),  # dict
        ),  # dict
        f = dict(
            hard = dict(
                nom_sg = 'а',
                gen_sg = 'ой',
                dat_sg = 'ой',
                acc_sg = 'у',
                ins_sg = 'ой',
                prp_sg = 'ой',
            ),  # dict
            soft = dict(
                nom_sg = 'я',
                gen_sg = 'ей',
                dat_sg = 'ей',
                acc_sg = 'ю',
                ins_sg = 'ей',
                prp_sg = 'ей',
            ),  # dict
        ),  # dict
        n = dict(
            hard = dict(
                nom_sg = 'о',
                gen_sg = 'ого',
                dat_sg = 'ому',
                ins_sg = 'ым',
                prp_sg = 'ом',
            ),  # dict
            soft = dict(
                nom_sg = ['е', 'ё'],
                gen_sg = 'его',
                dat_sg = 'ему',
                ins_sg = 'им',
                prp_sg = 'ем',
            ),  # dict
        ),  # dict
        common = dict(  # common endings
            hard = dict(
                nom_pl = 'ы',
                gen_pl = 'ых',
                dat_pl = 'ым',
                ins_pl = 'ыми',
                prp_pl = 'ых',
            ),  # dict
            soft = dict(
                nom_pl = 'и',
                gen_pl = 'их',
                dat_pl = 'им',
                ins_pl = 'ими',
                prp_pl = 'их',
            ),  # dict
        ),  # dict
    )  # dict
    # todo: сразу преобразовать в дефисы
# end

def get_standard_pronoun_noun_endings():
    # TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
    return dict(
        m = dict(
            hard = dict(
                nom_sg = '',
                gen_sg = 'а',
                dat_sg = 'у',
                ins_sg = 'ым',
                prp_sg = 'е',
            ),  # dict
            soft = dict(
                nom_sg = 'ь',
                gen_sg = 'я',
                dat_sg = 'ю',
                ins_sg = 'им',
                prp_sg = ['ем', 'ём'],
            ),  # dict
        ),  # dict
        f = dict(
            hard = dict(
                nom_sg = 'а',
                gen_sg = 'а',
                dat_sg = 'ой',
                acc_sg = 'у',
                ins_sg = 'ой',
                prp_sg = 'ой',
            ),  # dict
            soft = dict(
                nom_sg = 'я',
                gen_sg = 'ей',
                dat_sg = 'ей',
                acc_sg = 'ю',
                ins_sg = 'ей',
                prp_sg = 'ей',
            ),  # dict
        ),  # dict
        n = dict(
            hard = dict(
                nom_sg = 'о',
                gen_sg = 'а',
                dat_sg = 'у',
                ins_sg = 'ым',
                prp_sg = 'е',
            ),  # dict
            soft = dict(
                nom_sg = ['е', 'ё'],
                gen_sg = 'я',
                dat_sg = 'ю',
                ins_sg = 'им',
                prp_sg = ['ем', 'ём'],
            ),  # dict
        ),  # dict
        common = dict(  # common endings
            hard = dict(
                nom_pl = 'ы',
                gen_pl = 'ых',
                dat_pl = 'ым',
                ins_pl = 'ыми',
                prp_pl = 'ых',
            ),  # dict
            soft = dict(
                nom_pl = 'и',
                gen_pl = 'их',
                dat_pl = 'им',
                ins_pl = 'ими',
                prp_pl = 'их',
            ),  # dict
        ),  # dict
    )  # dict
    # todo: сразу преобразовать в дефисы
# end

# Схлопывание: Выбор окончаний в зависимости от рода и типа основы
def get_base_endings(gender, base_stem_type, adj, pronoun):
    # local standard_endings, keys

    # INFO: Получение списка всех стандартных окончаний
    if adj:
        standard_endings = get_standard_adj_endings()
    elif pronoun:
        standard_endings = get_standard_pronoun_noun_endings()
    else:
        standard_endings = get_standard_noun_endings()
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
def fix_noun_endendings(endings, gender, stem_type, stress_schema):

    # INFO: Replace "ы" to "и"
    if _.equals(stem_type, ['velar', 'sibilant']):
        if gender == 'f': endings['gen_sg'] = 'и' # end
        if gender == 'm': endings['nom_pl'] = 'и' # end
        if gender == 'f': endings['nom_pl'] = 'и' # end
    # end

    # INFO: Replace unstressed "о" to "е"
    if _.equals(stem_type, ['sibilant', 'letter-ц']):
        if not stress_schema['ending']['nom_sg']:
            if gender == 'n': endings['nom_sg'] = 'е' # end # ???
        # end
        if not stress_schema['ending']['ins_sg']:
            if gender == 'm': endings['ins_sg'] = 'ем' # end
            if gender == 'n': endings['ins_sg'] = 'ем' # end
            if gender == 'f': endings['ins_sg'] = 'ей' # end
        # end
        if not stress_schema['ending']['gen_pl']:
            if gender == 'm': endings['gen_pl'] = ['ев', 'ев'] # end  # TODO: should we change stressed value here?
        # end
    # end

    if _.equals(stem_type, 'sibilant'):
        # Replace "ов", "ев", "ёв" and null to "ей"
        if gender == 'm': endings['gen_pl'] = ['ей', 'ей']   # end
        if gender == 'n': endings['gen_pl'][stressed] = 'ей' # end
#        if gender == 'n': endings['gen_pl'][unstressed] = '' # end # this is just don't changed
        if gender == 'f': endings['gen_pl'][stressed] = 'ей' # end
#        if gender == 'f': endings['gen_pl'][unstressed] = '' # end # this is just don't changed
    # end

    # INFO: Replace "ь" to "й"
    if _.equals(stem_type, ['vowel', 'letter-и']):
        if gender == 'm': endings['nom_sg'] = 'й'             # end # ???
        if gender == 'n': endings['gen_pl'][unstressed] = 'й' # end
        if gender == 'f': endings['gen_pl'][unstressed] = 'й' # end
    # end

    # INFO: Replace "ей" to "ев/ёв", and "ь,ей" to "й"
    if _.equals(stem_type, ['vowel', 'letter-и']):
        if gender == 'm': endings['gen_pl'] = ['ев', 'ёв'] # end
        if gender == 'n': endings['gen_pl'] = ['й', 'й']   # end
        if gender == 'f': endings['gen_pl'] = ['й', 'й']   # end
    # end

    if _.equals(stem_type, 'letter-и'):
        if gender == 'f': endings['dat_sg'][unstressed] = 'и' # end
        endings['prp_sg'][unstressed] = 'и'
    # end

    if _.equals(stem_type, 'm-3rd'):
        if gender == 'm': endings['gen_sg'] = 'и' # end
        if gender == 'm': endings['dat_sg'] = 'и' # end
        endings['prp_sg'] = ['и', 'и']
    # end

    if _.equals(stem_type, ['f-3rd', 'f-3rd-sibilant']):
        if gender == 'f': endings['nom_sg'] = 'ь' # end
        if gender == 'f': endings['dat_sg'] = ['и', 'и'] # end
        if gender == 'f': endings['acc_sg'] = 'ь' # end
        if gender == 'f': endings['ins_sg'] = ['ью', 'ью'] # end
        endings['prp_sg'] = ['и', 'и']
        if gender == 'f': endings['gen_pl'] = ['ей', 'ей'] # end
    # end

    if _.equals(stem_type, 'f-3rd-sibilant'):
        endings['dat_pl'] = 'ам'
        endings['ins_pl'] = 'ами'
        endings['prp_pl'] = 'ах'
    # end
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
def fix_adj_pronoun_endings(endings, gender, stem_type, stress_schema, adj, pronoun):

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


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
def fix_pronoun_noun_endings(endings, gender, stem_type, stress_schema):

    # INFO: Replace "ы" to "и"
    if _.equals(stem_type, {'sibilant'}):
        if _.In(gender, ['m', 'n']):
            endings['ins_sg'] = 'им'
        # end

        endings['nom_pl'] = 'и'
        endings['gen_pl'] = 'их'
        endings['dat_pl'] = 'им'
        endings['ins_pl'] = 'ими'
        endings['prp_pl'] = 'их'
    # end

    # INFO: Other Replace
    if _.equals(stem_type, {'sibilant'}):
        if gender == 'n':
            endings['nom_sg'] = {'е', 'о' }
        # end
        if _.In(gender, ['m', 'n']):
            endings['gen_sg'] = ['его', 'ого']
            endings['dat_sg'] = ['ему', 'ому']
            endings['prp_sg'] = ['ем', 'ом']
        # end
        if gender == 'f':
            endings['gen_sg'] = ['ей', 'ой']
            endings['dat_sg'] = ['ей', 'ой']
            endings['ins_sg'] = ['ей', 'ой']
            endings['prp_sg'] = ['ей', 'ой']
        # end
    # end

    if _.equals(stem_type, {'vowel'}):
        if _.In(gender, ['m', 'n']):
            endings['gen_sg'] = 'его'
            endings['dat_sg'] = 'ему'
        # end
    # end
# end


# Изменение окончаний для случаев (1), (2), (3)
def apply_specific_1_2(endings, gender, stem_type, base_stem_type, rest_index, adj, pronoun):

    if adj or pronoun:
        pass # TODO

    else:
        if _.contains(rest_index, ['%(1%)', '①']):
            if base_stem_type == 'hard':
                if gender == 'm': endings['nom_pl'] = 'а' # end
                if gender == 'n': endings['nom_pl'] = 'ы' # end
            # end
            if base_stem_type == 'soft':
                if gender == 'm': endings['nom_pl'] = 'я' # end
                if gender == 'n': endings['nom_pl'] = 'и' # end
            # end
            if _.equals(stem_type, ['velar', 'sibilant']):  # Replace "ы" to "и"
                if gender == 'n': endings['nom_pl'] = 'и' # end
            # end
        # end

        if _.contains(rest_index, ['%(2%)', '②']):
            if base_stem_type == 'hard':
                if gender == 'm': endings['gen_pl'] = ['', ''] # end
                if gender == 'n': endings['gen_pl'] = ['ов', 'ов'] # end
                if gender == 'f': endings['gen_pl'] = {'ей', 'ей' } # end
            # end
            if base_stem_type == 'soft':
                if gender == 'm': endings['gen_pl'] = ['ь', 'ь'] # end
                if gender == 'n': endings['gen_pl'] = ['ев', 'ёв']  # end
                if gender == 'f': endings['gen_pl'] = {'ей', 'ей' } # end
            # end
            if _.equals(stem_type, ['sibilant', 'letter-ц']):  # Replace unstressed "о" to "е"
                if gender == 'n': endings['gen_pl'][unstressed] = 'ев' # end
            # end

#        # Possibly we don't need this:
#            # Replace "ов", "ев", "ёв" and null to "ей"
#            if stem_type = {'sibilant'}}
#                if gender == 'n': endings['gen_pl'] = ['ей', 'ей']
#                if gender == 'm': endings['gen_pl'][stressed] = 'ей'
#            # end
#            # Replace "ь" to "й"
#            if stem_type = ['vowel', 'letter-и']}
#                if gender == 'm': endings['gen_pl'][stressed] = ['й', 'й']
#            # end
#            # Replace "ей" to "ев/ёв", and "ь,ей" to "й"
#            if stem_type = ['vowel', 'letter-и']}
#                if gender == 'f': endings['gen_pl'][unstressed] = ['ев', 'ёв']
#                if gender == 'm': endings['gen_pl'][stressed] = ['й', 'й']
#            # end
#        #
        # end
    # end
# end


# Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
def choose_endings_stress(endings, gender, base_stem_type, stress_schema, adj, pronoun):
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
    # INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')
    # local endings

    endings = get_base_endings(data.gender, data.base_stem_type, data.adj, data.pronoun)

    # INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
    if data.adj:  # or data.pronoun
        fix_adj_pronoun_endings(endings, data.gender, data.stem_type, data.stress_schema, data.adj, False)
    elif data.pronoun:
        fix_pronoun_noun_endings(endings, data.gender, data.stem_type, data.stress_schema)
    else:
        fix_noun_endendings(endings, data.gender, data.stem_type, data.stress_schema)
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
