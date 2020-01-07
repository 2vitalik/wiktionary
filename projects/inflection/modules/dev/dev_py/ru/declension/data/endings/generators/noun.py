from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


import json
import re
from shared_utils.io.io import write


# constants:
unstressed = 0  # local
stressed = 1  # local
genders = ['m', 'n', 'f']  # local

module = 'data.endings.noun'  # local


@a.call(module)
def base_noun_endings():
    # Все стандартные окончания для двух типов основ
    return {
        'm': {  # стандартные окончания мужского рода
            '1-hard': {
                'nom-sg': '',
                'gen-sg': 'а',
                'dat-sg': 'у',
                'acc-sg': '...',
                'ins-sg': ['ом', 'ом'],
                'prp-sg': 'common',
                'nom-pl': 'ы',
                'gen-pl': ['ов', 'ов'],  # TODO: possibly we can join them together again: m-hard-gen-pl stressed and unstressed
            },
            '2-soft': {
                'nom-sg': 'ь',
                'gen-sg': 'я',
                'dat-sg': 'ю',
                'acc-sg': '...',
                'ins-sg': ['ем', 'ём'],
                'prp-sg': 'common',
                'nom-pl': 'и',
                'gen-pl': ['ей', 'ей'],
            },
        },
        'f': {  # стандартные окончания женского рода
            '1-hard': {
                'nom-sg': 'а',
                'gen-sg': 'ы',
                'dat-sg': 'е',
                'acc-sg': 'у',
                'ins-sg': ['ой', 'ой'],
                'prp-sg': 'common',
                'nom-pl': 'ы',
                'gen-pl': ['', ''],
            },
            '2-soft': {
                'nom-sg': 'я',
                'gen-sg': 'и',
                'dat-sg': ['е', 'е'],
                'acc-sg': 'ю',
                'ins-sg': ['ей', 'ёй'],
                'prp-sg': 'common',
                'nom-pl': 'и',
                'gen-pl': ['ь', 'ей'],
            },
        },
        'n': {  # стандартные окончания среднего рода
            '1-hard': {
                'nom-sg': ['о', 'о'],
                'gen-sg': 'а',
                'dat-sg': 'у',
                'acc-sg': '...',
                'ins-sg': ['ом', 'ом'],
                'prp-sg': 'common',
                'nom-pl': 'а',
                'gen-pl': ['', ''],
            },
            '2-soft': {
                'nom-sg': 'е',  # was: ['е', 'ё']
                'gen-sg': 'я',
                'dat-sg': 'ю',
                'acc-sg': '...',
                'ins-sg': ['ем', 'ём'],
                'prp-sg': 'common',
                'nom-pl': 'я',
                'gen-pl': ['ь', 'ей'],
            },
        },
        'common': {  # common endings
            '1-hard': {
                'prp-sg': ['е', 'е'],
                'dat-pl': 'ам',
                'acc-pl': '...',
                'ins-pl': 'ами',
                'prp-pl': 'ах',
            },
            '2-soft': {
                'prp-sg': ['е', 'е'],
                'dat-pl': 'ям',
                'acc-pl': '...',
                'ins-pl': 'ями',
                'prp-pl': 'ях',
            }
        }
    }
# end


def copy_common_endings(endings):
    # INFO: Заполнение из общих данных для всех родов:
    base_types = ['1-hard', '2-soft']  # local
    for j, gender in enumerate(genders):
        for j, base_type in enumerate(base_types):
            for key, value in endings['common'][base_type].items():
                endings[gender][base_type][key] = value
            # end
        # end
    # end
    del endings['common']  # todo: rewrite in LUA
# end


def copy_other_endings(endings, genders):
    hard_types = ['3-velar', '4-sibilant', '5-letter-ц']
    soft_types = ['6-vowel', '7-letter-и']

    # INFO: Generate other types based on hard and soft
    for j, gender in enumerate(genders):
        for j, hard_type in enumerate(hard_types):
            endings[gender][hard_type] = mw.clone(endings[gender]['1-hard'])
        # end
        for j, soft_type in enumerate(soft_types):
            endings[gender][soft_type] = mw.clone(endings[gender]['2-soft'])
        # end
    # end
# end


def copy_8_third_endings(endings):
    # local keys
    keys = [
        'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
        'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
    ]  # list

    stem_type = '8-third'
    for j, gender in enumerate(genders):
        endings[gender][stem_type] = dict()  # dict
        if gender == 'n':
            base_stem_type = '1-hard'
        elif gender == 'm' or gender == 'f':
            base_stem_type = '2-soft'
        else:
            base_stem_type = '?'  # never should happen
        for j, key in enumerate(keys):
            endings[gender][stem_type][key] = endings[gender][base_stem_type][key]
        # end
    # end
# end


@a.starts(module)
def fill_other_noun_endings(func, endings):
    # INFO: Изменение окончаний для нестандартного типов основы ('3-velar', '4-sibilant', '6-vowel' и т.п.)
    # INFO: Изменение окончаний для остальных типов основ (базирующихся на первых двух):

    # INFO: Replace "ы" to "и"
    for j, stem_type in enumerate(['3-velar', '4-sibilant']):
        endings['f'][stem_type]['gen-sg'] = 'и'
        endings['m'][stem_type]['nom-pl'] = 'и'
        endings['n'][stem_type]['nom-pl'] = 'и'
    # end

    # INFO: Replace unstressed "о" to "е"
    for j, stem_type in enumerate(['4-sibilant', '5-letter-ц']):
        endings['n'][stem_type]['nom-sg'][unstressed] = 'е'  # fixme: ???
        endings['m'][stem_type]['ins-sg'][unstressed] = 'ем'
        endings['n'][stem_type]['ins-sg'][unstressed] = 'ем'
        endings['f'][stem_type]['ins-sg'][unstressed] = 'ей'
        endings['m'][stem_type]['gen-pl'] = ['ев', 'ев']  # TODO: should we change stressed value here or only unstressed?
    # end

    # INFO: Replace "ов", "ев", "ёв" and null to "ей"
    stem_type = '4-sibilant'
    endings['m'][stem_type]['gen-pl'] = ['ей', 'ей']
    endings['n'][stem_type]['gen-pl'][stressed] = 'ей'
    # endings['n'][stem_type]['gen-pl'][unstressed] = ''  # this is just don't changed
    endings['f'][stem_type]['gen-pl'][stressed] = 'ей'
    # endings['f'][stem_type]['gen-pl'][unstressed] = ''  # this is just don't changed

    # INFO: Replace "ь" to "й"
    for j, stem_type in enumerate(['6-vowel', '7-letter-и']):
        endings['m'][stem_type]['nom-sg'] = 'й'             # ???
        endings['n'][stem_type]['gen-pl'][unstressed] = 'й'
        endings['f'][stem_type]['gen-pl'][unstressed] = 'й'
    # end

    # INFO: Replace "ей" to "ев/ёв", and "ь,ей" to "й"
    for j, stem_type in enumerate(['6-vowel', '7-letter-и']):
        endings['m'][stem_type]['gen-pl'] = ['ев', 'ёв']
        endings['n'][stem_type]['gen-pl'] = ['й', 'й']
        endings['f'][stem_type]['gen-pl'] = ['й', 'й']
    # end

    stem_type = '7-letter-и'
    endings['f'][stem_type]['dat-sg'][unstressed] = 'и'
    for j, gender in enumerate(genders):
        endings[gender][stem_type]['prp-sg'][unstressed] = 'и'
    # end

    stem_type = '8-third'
    endings['m'][stem_type]['gen-sg'] = 'и'
    endings['m'][stem_type]['dat-sg'] = 'и'
    endings['f'][stem_type]['nom-sg'] = 'ь'
    endings['f'][stem_type]['dat-sg'] = ['и', 'и']
    endings['f'][stem_type]['acc-sg'] = 'ь'
    endings['f'][stem_type]['ins-sg'] = ['ью', 'ью']
    endings['f'][stem_type]['gen-pl'] = ['ей', 'ей']
    for j, gender in enumerate(genders):
        endings[gender][stem_type]['prp-sg'] = ['и', 'и']
    # end

    _.ends(module, func)
# end


def dump_data(filename, endings):
    content = json.dumps(endings, indent=4, ensure_ascii=False)
    content = \
        re.sub(r'\[\s+"([^"]*)",\s*"([^"]*)"\s*\]', r'["\1", "\2"]', content)
    write(f'{filename}.json', content)

    content = re.sub(r'"([^"]+)": ', r'["\1"] = ', content)
    content = re.sub(r' = \[([^]]+)\]', r' = {\1}', content)
    content = 'return ' + content
    write(f'{filename}.lua', content)
# end


@a.starts(module)
def generate_noun_endings(func):
    endings = base_noun_endings()  # local
    copy_common_endings(endings)
    copy_other_endings(endings, genders)
    copy_8_third_endings(endings)
    fill_other_noun_endings(endings)
    dump_data('noun', endings)
    return _.returns(module, func, endings)
# end


if __name__ == '__main__':
    generate_noun_endings()


# todo: convert this also to LUA later? (and all other `generators`)
