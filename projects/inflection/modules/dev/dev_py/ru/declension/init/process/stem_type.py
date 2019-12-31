from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'init.process.stem_type'  # local


@a.starts(module)
def get_stem_base_type(func, stem_type):
    # local stem_base_types

    # INFO: Выбор подходящего из двух типов

#    TODO: make one big dict?

    stem_base_types = dict()  # dict
    # hard
    stem_base_types['hard']  = 'hard'
    stem_base_types['velar'] = 'hard'
    stem_base_types['sibilant'] = 'hard'
    stem_base_types['letter-ц'] = 'hard'
    # soft
    stem_base_types['soft']  = 'soft'
    stem_base_types['vowel'] = 'soft'
    stem_base_types['letter-и'] = 'soft'
    stem_base_types['m-3rd'] = 'soft'
    stem_base_types['f-3rd'] = 'soft'
    stem_base_types['f-3rd-sibilant'] = 'soft'
    stem_base_types['n-3rd'] = 'hard'

    _.ends(module, func)
    return stem_base_types[stem_type]
# end


@a.starts(module)
def get_stem_type(func, i):  # export  # INFO: Определение типа основы
    word = i.word.unstressed  # local
    stem = i.stem.unstressed  # local

    i.stem.type = ''

    if _.endswith(stem, '[гкх]'):
        i.stem.type = 'velar'  # todo: '3-velar'
    elif _.endswith(stem, '[жчшщ]'):
        i.stem.type = 'sibilant'
    elif _.endswith(stem, 'ц'):
        i.stem.type = 'letter-ц'
    elif _.endswith(stem, ['[йь]', '[аоеёуыэюя]']):
        i.stem.type = 'vowel'
    elif _.endswith(stem, 'и'):
        i.stem.type = 'letter-и'
    else:
        if i.adj:
            if _.endswith(word, ['ый', 'ой', 'ая', 'ое', 'ые']):
                i.stem.type = 'hard'
            elif _.endswith(word, ['ий', 'яя', 'ее', 'ие']):
                i.stem.type = 'soft'
            # end
        elif i.gender == 'm':
            if stem == word or _.endswith(word, 'ы'):
                i.stem.type = 'hard'
            elif _.endswith(word, 'путь'):
                i.stem.type = 'm-3rd'
            elif _.endswith(word, 'ь') or _.endswith(word, 'и'):
                i.stem.type = 'soft'
            elif _.endswith(word, 'а'):
#                i.gender = 'f'
                i.stem.type = 'hard'
            elif _.endswith(word, 'я'):
#                i.gender = 'f'
                i.stem.type = 'soft'
            # end
        elif i.gender == 'f':
            if _.endswith(word, 'а') or _.endswith(word, 'ы'):
                i.stem.type = 'hard'
            elif _.endswith(word, 'я'):
                i.stem.type = 'soft'
            elif _.endswith(word, 'и') and _.contains(i.rest_index, '2'):  # todo: а что если нет индекса??
                i.stem.type = 'soft'
            elif _.endswith(word, 'и') and _.contains(i.rest_index, '8'):
                i.stem.type = 'f-3rd'
            elif _.endswith(word, 'ь'):  # conflict in pl
                i.stem.type = 'f-3rd'
            # end
        elif i.gender == 'n':
            if _.endswith(word, 'о') or _.endswith(word, 'а'):
                i.stem.type = 'hard'
            elif _.endswith(word, 'мя')  or _.endswith(word, 'мена'):
                i.stem.type = 'n-3rd'
            elif _.endswith(word, 'е') or _.endswith(word, 'я'):
                i.stem.type = 'soft'
            # end
        # end
    # end

#    if gender == 'm':
#        if _.endswith(word, ['а', 'я']):
#            i.gender = 'f'
#        # end
#    # end

    if i.gender == 'f' and i.stem.type == 'sibilant' and _.endswith(word, 'ь'):
        i.stem.type = 'f-3rd-sibilant'
    # end
    if i.stem.type == '':
        i.stem.type = 'hard'
        # e.add_error(i, 'Неизвестный тип основы')
        # return _.ends(module, func)
    # end

    # INFO: Выбор подходящего `stem_type` из двух базовых типов: 'hard' и 'soft'
    i.stem.base_type = get_stem_base_type(i.stem.type)

    _.ends(module, func)
# end

# return export
