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
