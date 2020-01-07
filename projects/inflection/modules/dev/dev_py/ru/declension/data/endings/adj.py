from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version

import sys, os; sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from data.endings.noun import copy_other_endings, dump_data
except ImportError:
    from ...data.endings.noun import copy_other_endings, dump_data


# constants:
unstressed = 0  # local
stressed = 1  # local
genders = ['m', 'n', 'f', 'pl']  # local

module = 'data.endings.adj'  # local


# Данные: все стандартные окончания для двух типов основ
@a.call(module)
def base_adj_endings():
    return {
        'm': {
            '1-hard': {
                'nom-sg': ['ый', 'ой'],
                'gen-sg': ['ого', 'ого'],
                'dat-sg': ['ому', 'ому'],
                'acc-sg': '...',
                'ins-sg': 'ым',
                'prp-sg': ['ом', 'ом'],
                'srt-sg': '',
            },
            '2-soft': {
                'nom-sg': 'ий',
                'gen-sg': 'его',
                'dat-sg': 'ему',
                'acc-sg': '...',
                'ins-sg': 'им',
                'prp-sg': 'ем',
                'srt-sg': 'ь',
            },
        },
        'f': {
            '1-hard': {
                'nom-sg': 'ая',
                'gen-sg': ['ой', 'ой'],
                'dat-sg': ['ой', 'ой'],
                'acc-sg': 'ую',
                'ins-sg': ['ой', 'ой'],
                'prp-sg': ['ой', 'ой'],
                'srt-sg': 'а',
            },
            '2-soft': {
                'nom-sg': 'яя',
                'gen-sg': 'ей',
                'dat-sg': 'ей',
                'acc-sg': 'юю',
                'ins-sg': 'ей',
                'prp-sg': 'ей',
                'srt-sg': 'я',
            },
        },
        'n': {
            '1-hard': {
                'nom-sg': ['ое', 'ое'],
                'gen-sg': ['ого', 'ого'],
                'dat-sg': ['ому', 'ому'],
                'acc-sg': '...',
                'ins-sg': 'ым',
                'prp-sg': ['ом', 'ом'],
                'srt-sg': ['о', 'о'],
            },
            '2-soft': {
                'nom-sg': 'ее',
                'gen-sg': 'его',
                'dat-sg': 'ему',
                'acc-sg': '...',
                'ins-sg': 'им',
                'prp-sg': 'ем',
                'srt-sg': ['е', 'ё'],
            },
        },
        'pl': {  # plural endings
            '1-hard': {
                'nom-pl': 'ые',
                'gen-pl': 'ых',
                'dat-pl': 'ым',
                'acc-pl': '...',
                'ins-pl': 'ыми',
                'prp-pl': 'ых',
                'srt-pl': 'ы',
            },
            '2-soft': {
                'nom-pl': 'ие',
                'gen-pl': 'их',
                'dat-pl': 'им',
                'acc-pl': '...',
                'ins-pl': 'ими',
                'prp-pl': 'их',
                'srt-pl': 'и',
            },
        },
    }
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
@a.starts(module)
def fill_other_adj_endings(func, endings):
    # INFO: Replace "ы" to "и"
    for j, stem_type in enumerate(['3-velar', '4-sibilant']):
        endings['m'][stem_type]['nom-sg'][unstressed] = 'ий'  # adj only
        endings['m'][stem_type]['ins-sg'] = 'им'
        endings['n'][stem_type]['ins-sg'] = 'им'

        endings['pl'][stem_type]['nom-pl'] = 'ие'  # adj only
        # endings['pl'][stem_type]['nom-pl'] = 'и'  # pronoun only
        endings['pl'][stem_type]['gen-pl'] = 'их'
        endings['pl'][stem_type]['dat-pl'] = 'им'
        endings['pl'][stem_type]['ins-pl'] = 'ими'
        endings['pl'][stem_type]['prp-pl'] = 'их'
        endings['pl'][stem_type]['srt-pl'] = 'и'  # adj only
    # end

    # INFO: Replace unstressed "о" to "е"
    for j, stem_type in enumerate(['4-sibilant', '5-letter-ц']):
        # if not i.stress_schema['ending']['sg']:  # fixme
        endings['m'][stem_type]['nom-sg'][stressed] = 'ей'  # adj only  # fixme ???
        endings['m'][stem_type]['gen-sg'][unstressed] = 'его'
        endings['m'][stem_type]['dat-sg'][unstressed] = 'ему'
        endings['m'][stem_type]['prp-sg'][unstressed] = 'ем'

        endings['n'][stem_type]['nom-sg'][unstressed] = 'ее'
        endings['n'][stem_type]['gen-sg'][unstressed] = 'его'
        endings['n'][stem_type]['dat-sg'][unstressed] = 'ему'
        endings['n'][stem_type]['prp-sg'][unstressed] = 'ем'

        endings['f'][stem_type]['gen-sg'][unstressed] = 'ей'
        endings['f'][stem_type]['dat-sg'][unstressed] = 'ей'
        endings['f'][stem_type]['ins-sg'][unstressed] = 'ей'
        endings['f'][stem_type]['prp-sg'][unstressed] = 'ей'

        endings['n'][stem_type]['srt-sg'][unstressed] = 'е'  # adj only
    # end

    # INFO: Replace "ь" to "й"
    stem_type = '6-vowel'  # local
    endings['m'][stem_type]['srt-sg'] = 'й'  # adj only

    _.ends(module, func)
# end


@a.starts(module)
def generate_adj_endings(func):
    endings = base_adj_endings()  # local
    copy_other_endings(endings, genders)
    fill_other_adj_endings(endings)
    dump_data('adj', endings)
    return _.returns(module, func, endings)
# end


if __name__ == '__main__':
    generate_adj_endings()
