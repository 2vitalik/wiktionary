from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'init.process.stem_type'  # local


@a.starts(module)
def get_stem_base_type(func, i):
    # INFO: Выбор подходящего из двух типов

    if _.equals(i.stem.type, ['1-hard', '3-velar', '4-sibilant', '5-letter-ц']):
        return _.returns(module, func, '1-hard')
    # end

    if _.equals(i.stem.type, ['2-soft', '6-vowel', '7-letter-и']):
        return _.returns(module, func, '2-soft')
    # end

    if _.equals(i.stem.type, ['8-third']):
        if i.gender == 'n':
            return _.returns(module, func, '1-hard')
        # end
        if i.gender == 'm' or i.gender == 'f':
            return _.returns(module, func, '2-soft')
        # end
    # end

    return _.returns(module, func, '?')
# end


@a.starts(module)
def get_stem_type(func, i):  # export  # INFO: Определение типа основы
    word = i.word.unstressed  # local
    stem = i.stem.unstressed  # local

    i.stem.type = ''

    if _.endswith(stem, '[гкх]'):
        i.stem.type = '3-velar'
    elif _.endswith(stem, '[жчшщ]'):
        i.stem.type = '4-sibilant'
    elif _.endswith(stem, 'ц'):
        i.stem.type = '5-letter-ц'
    elif _.endswith(stem, ['[йь]', '[аоеёуыэюя]']):
        i.stem.type = '6-vowel'
    elif _.endswith(stem, 'и'):
        i.stem.type = '7-letter-и'
    else:
        if i.adj:
            if _.endswith(word, ['ый', 'ой', 'ая', 'ое', 'ые']):
                i.stem.type = '1-hard'
            elif _.endswith(word, ['ий', 'яя', 'ее', 'ие']):
                i.stem.type = '2-soft'
            # end
        elif i.gender == 'm':
            if stem == word or _.endswith(word, 'ы'):
                i.stem.type = '1-hard'
            elif _.endswith(word, 'путь'):
                i.stem.type = '8-third'
            elif _.endswith(word, 'ь') or _.endswith(word, 'и'):
                i.stem.type = '2-soft'
            elif _.endswith(word, 'а'):
                i.stem.type = '1-hard'
                # i.gender = 'f' ??
            elif _.endswith(word, 'я'):
                i.stem.type = '2-soft'
                # i.gender = 'f' ??
            # end
        elif i.gender == 'f':
            if _.endswith(word, 'а') or _.endswith(word, 'ы'):
                i.stem.type = '1-hard'
            elif _.endswith(word, 'я'):
                i.stem.type = '2-soft'
            elif _.endswith(word, 'и') and _.contains(i.rest_index, '2'):  # todo: а что если нет индекса??
                i.stem.type = '2-soft'
            elif _.endswith(word, 'и') and _.contains(i.rest_index, '8'):
                i.stem.type = '8-third'
            elif _.endswith(word, 'ь'):  # conflict in pl
                i.stem.type = '8-third'
            # end
        elif i.gender == 'n':
            if _.endswith(word, 'о') or _.endswith(word, 'а'):
                i.stem.type = '1-hard'
            elif _.endswith(word, 'мя') or _.endswith(word, 'мена'):
                i.stem.type = '8-third'
            elif _.endswith(word, 'е') or _.endswith(word, 'я'):
                i.stem.type = '2-soft'
            # end
        # end
    # end

#    if gender == 'm':
#        if _.endswith(word, ['а', 'я']):
#            i.gender = 'f'
#        # end
#    # end

    if i.gender == 'f' and i.stem.type == '4-sibilant' and _.endswith(word, 'ь'):
        i.stem.type = '8-third'
    # end
    if i.stem.type == '':
        i.stem.type = '1-hard'
        # e.add_error(i, 'Неизвестный тип основы')  -- fixme ?
        # return _.ends(module, func)
    # end

    # INFO: Выбор подходящего `stem_type` из двух базовых типов: '1-hard' и '2-soft'
    i.stem.base_type = get_stem_base_type(i)

    _.ends(module, func)
# end

# return export
