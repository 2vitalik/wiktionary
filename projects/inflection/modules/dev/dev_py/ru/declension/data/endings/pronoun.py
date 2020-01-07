from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


import sys, os; sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from data.endings.noun import copy_common_endings, copy_other_endings, dump_data
except ImportError:
    from ...data.endings.noun import copy_common_endings, copy_other_endings, dump_data


genders = ['m', 'n', 'f']  # local

module = 'data.endings.pronoun'  # local


@a.call(module)
def base_pronoun_endings():
    # todo: not used yet
    return {
        'm': {
            '1-hard': {
                'nom-sg': '',
                'gen-sg': 'ого',
                'dat-sg': 'ому',
                'ins-sg': 'ым',
                'prp-sg': 'ом',
            },
            '2-soft': {
                'nom-sg': 'ь',
                'gen-sg': 'его',
                'dat-sg': 'ему',
                'ins-sg': 'им',
                'prp-sg': ['ем', 'ём'],
            },
        },
        'f': {
            '1-hard': {
                'nom-sg': 'а',
                'gen-sg': 'ой',
                'dat-sg': 'ой',
                'acc-sg': 'у',
                'ins-sg': 'ой',
                'prp-sg': 'ой',
            },
            '2-soft': {
                'nom-sg': 'я',
                'gen-sg': 'ей',
                'dat-sg': 'ей',
                'acc-sg': 'ю',
                'ins-sg': 'ей',
                'prp-sg': 'ей',
            },
        },
        'n': {
            '1-hard': {
                'nom-sg': 'о',
                'gen-sg': 'ого',
                'dat-sg': 'ому',
                'ins-sg': 'ым',
                'prp-sg': 'ом',
            },
            '2-soft': {
                'nom-sg': ['е', 'ё'],
                'gen-sg': 'его',
                'dat-sg': 'ему',
                'ins-sg': 'им',
                'prp-sg': 'ем',
            },
        },
        'common': {
            '1-hard': {
                'nom-pl': 'ы',
                'gen-pl': 'ых',
                'dat-pl': 'ым',
                'ins-pl': 'ыми',
                'prp-pl': 'ых',
            },
            '2-soft': {
                'nom-pl': 'и',
                'gen-pl': 'их',
                'dat-pl': 'им',
                'ins-pl': 'ими',
                'prp-pl': 'их',
            },
        },
    }
# end


@a.call(module)
def base_pronoun_noun_endings():
    return {
        'm': {
            '1-hard': {
                'nom-sg': '',
                'gen-sg': 'а',
                'dat-sg': 'у',
                'ins-sg': 'ым',
                'prp-sg': 'е',
            },
            '2-soft': {
                'nom-sg': 'ь',
                'gen-sg': 'я',
                'dat-sg': 'ю',
                'ins-sg': 'им',
                'prp-sg': ['ем', 'ём'],
            },
        },
        'f': {
            '1-hard': {
                'nom-sg': 'а',
                'gen-sg': 'а',
                'dat-sg': 'ой',
                'acc-sg': 'у',
                'ins-sg': 'ой',
                'prp-sg': 'ой',
            },
            '2-soft': {
                'nom-sg': 'я',
                'gen-sg': 'ей',
                'dat-sg': 'ей',
                'acc-sg': 'ю',
                'ins-sg': 'ей',
                'prp-sg': 'ей',
            },
        },
        'n': {
            '1-hard': {
                'nom-sg': 'о',
                'gen-sg': 'а',
                'dat-sg': 'у',
                'ins-sg': 'ым',
                'prp-sg': 'е',
            },
            '2-soft': {
                'nom-sg': ['е', 'ё'],
                'gen-sg': 'я',
                'dat-sg': 'ю',
                'ins-sg': 'им',
                'prp-sg': ['ем', 'ём'],
            },
        },
        'common': {
            '1-hard': {
                'nom-pl': 'ы',
                'gen-pl': 'ых',
                'dat-pl': 'ым',
                'ins-pl': 'ыми',
                'prp-pl': 'ых',
            },
            '2-soft': {
                'nom-pl': 'и',
                'gen-pl': 'их',
                'dat-pl': 'им',
                'ins-pl': 'ими',
                'prp-pl': 'их',
            },
        },
    }
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
@a.starts(module)
def fill_other_pronoun_noun_endings(func, endings):
    mn_genders = ['m', 'n']  # local

    # INFO: Replace "ы" to "и"
    stem_type = '4-sibilant'  # local
    for j, gender in enumerate(mn_genders):
        endings[gender][stem_type]['ins-sg'] = 'им'
    # end
    for j, gender in enumerate(genders):
        endings[gender][stem_type]['nom-pl'] = 'и'
        endings[gender][stem_type]['gen-pl'] = 'их'
        endings[gender][stem_type]['dat-pl'] = 'им'
        endings[gender][stem_type]['ins-pl'] = 'ими'
        endings[gender][stem_type]['prp-pl'] = 'их'
    # end

    # INFO: Other Replace
    endings['n'][stem_type]['nom-sg'] = ['е', 'о']
    for j, gender in enumerate(mn_genders):
        endings[gender][stem_type]['gen-sg'] = ['его', 'ого']
        endings[gender][stem_type]['dat-sg'] = ['ему', 'ому']
        endings[gender][stem_type]['prp-sg'] = ['ем', 'ом']
    # end
    endings['f'][stem_type]['gen-sg'] = ['ей', 'ой']
    endings['f'][stem_type]['dat-sg'] = ['ей', 'ой']
    endings['f'][stem_type]['ins-sg'] = ['ей', 'ой']
    endings['f'][stem_type]['prp-sg'] = ['ей', 'ой']

    stem_type = '6-vowel'
    for j, gender in enumerate(mn_genders):
        endings[gender][stem_type]['gen-sg'] = 'его'
        endings[gender][stem_type]['dat-sg'] = 'ему'
    # end

    _.ends(module, func)
# end


@a.starts(module)
def generate_pronoun_noun_endings(func):
    endings = base_pronoun_noun_endings()  # local
    copy_common_endings(endings)
    copy_other_endings(endings, genders)
    fill_other_pronoun_noun_endings(endings)
    dump_data('pronoun', endings)
    return _.returns(module, func, endings)
# end


if __name__ == '__main__':
    generate_pronoun_noun_endings()
