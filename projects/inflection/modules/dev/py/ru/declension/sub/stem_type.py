from projects.inflection.modules.dev.py import a
from projects.inflection.modules.dev.py import mw
from projects.inflection.modules.dev.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'declension.stem_type'  # local


@a.starts(module)
def get_base_stem_type(func, stem_type):
    # local change_stem_type

    # INFO: Выбор подходящего из двух типов

#    TODO: make one big dict?

    change_stem_type = dict()  # dict
    # hard
    change_stem_type['hard']  = 'hard'
    change_stem_type['velar'] = 'hard'
    change_stem_type['sibilant'] = 'hard'
    change_stem_type['letter-ц'] = 'hard'
    # soft
    change_stem_type['soft']  = 'soft'
    change_stem_type['vowel'] = 'soft'
    change_stem_type['letter-и'] = 'soft'
    change_stem_type['m-3rd'] = 'soft'
    change_stem_type['f-3rd'] = 'soft'
    change_stem_type['f-3rd-sibilant'] = 'soft'
    change_stem_type['n-3rd'] = 'hard'

    _.ends(module, func)
    return change_stem_type[stem_type]
# end


@a.starts(module)
def get_stem_type(func, stem, word, gender, adj, rest_index):  # export  # INFO: Определение типа основы
    # local stem_type

    if _.endswith(stem, '[гкх]'):
        stem_type = 'velar'  # todo: '3-velar'
    elif _.endswith(stem, '[жчшщ]'):
        stem_type = 'sibilant'
    elif _.endswith(stem, 'ц'):
        stem_type = 'letter-ц'
    elif _.endswith(stem, ['[йь]', '[аоеёуыэюя]']):
        stem_type = 'vowel'
    elif _.endswith(stem, 'и'):
        stem_type = 'letter-и'
    else:
        if adj:
            if _.endswith(word, ['ый', 'ой', 'ая', 'ое', 'ые']):
                stem_type = 'hard'
            elif _.endswith(word, ['ий', 'яя', 'ее', 'ие']):
                stem_type = 'soft'
            # end
        elif gender == 'm':
            if stem == word or _.endswith(word, 'ы'):
                stem_type = 'hard'
            elif _.endswith(word, 'путь'):
                stem_type = 'm-3rd'
            elif _.endswith(word, 'ь') or _.endswith(word, 'и'):
                stem_type = 'soft'
            elif _.endswith(word, 'а'):
#                data.gender = 'f'
                stem_type = 'hard'
            elif _.endswith(word, 'я'):
#                data.gender = 'f'
                stem_type = 'soft'
            # end
        elif gender == 'f':
            if _.endswith(word, 'а') or _.endswith(word, 'ы'):
                stem_type = 'hard'
            elif _.endswith(word, 'я'):
                stem_type = 'soft'
            elif _.endswith(word, 'и') and _.contains(rest_index, '2'):  # todo: а что если нет индекса??
                stem_type = 'soft'
            elif _.endswith(word, 'и') and _.contains(rest_index, '8'):
                stem_type = 'f-3rd'
            elif _.endswith(word, 'ь'):  # conflict in pl
                stem_type = 'f-3rd'
            # end
        elif gender == 'n':
            if _.endswith(word, 'о') or _.endswith(word, 'а'):
                stem_type = 'hard'
            elif _.endswith(word, 'мя')  or _.endswith(word, 'мена'):
                stem_type = 'n-3rd'
            elif _.endswith(word, 'е') or _.endswith(word, 'я'):
                stem_type = 'soft'
            # end
        # end
    # end

#    if gender == 'm':
#        if _.endswith(word, ['а', 'я']):
#            data.gender = 'f'
#        # end
#    # end

    if gender == 'f' and stem_type == 'sibilant' and _.endswith(word, 'ь'):
        stem_type = 'f-3rd-sibilant'
    # end
    if stem_type == '':
        stem_type = 'hard'
    # end

    # INFO: Выбор подходящего `stem_type` из двух базовых типов: 'hard' и 'soft'
    # local base_stem_type
    base_stem_type = get_base_stem_type(stem_type)

    _.ends(module, func)
    return stem_type, base_stem_type
# end

# return export
