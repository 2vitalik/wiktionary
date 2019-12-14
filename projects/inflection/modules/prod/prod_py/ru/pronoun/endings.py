from projects.inflection.modules.prod.prod_py import a
from projects.inflection.modules.prod.prod_py import mw
from projects.inflection.modules.prod.prod_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'pronoun.endings'  # local


@a.call(module)
def get_standard_pronoun_endings():  # export
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


@a.call(module)
def get_standard_pronoun_noun_endings():  # export
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


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
@a.starts(module)
def fix_pronoun_noun_endings(func, endings, gender, stem_type, stress_schema):  # export
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

    _.ends(module, func)
# end


# return export
