from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


def get_cyrl_animacy(index, gender):
    _.log_func('parse_args', 'get_cyrl_animacy')

    if _.extract(index, '^' + gender + 'о//' + gender):
        return 'an//in'
    elif _.extract(index, '^' + gender + '//' + gender + 'о'):
        return 'in//an'
    elif _.extract(index, '^' + gender + 'о'):
        return 'an'
    else:
        return 'in'
    # end
# end


def extract_gender_animacy(data):
    _.log_func('parse_args', 'extract_gender_animacy')

    # local convert_animacy, orig_index, rest_index

    # мо-жо - mf a
    # ж//жо - f ina//a
    # мо - m a
    # с  - n ina
    data.pt = False

    if _.startswith(data.index, 'п'):
        data.adj = True
    elif _.extract(data.index, '^м//ж') or _.extract(data.index, '^m//f'):
        data.gender = 'mf'
        data.animacy = 'in'
    elif _.extract(data.index, '^м//с') or _.extract(data.index, '^m//n'):
        data.gender = 'mn'
        data.animacy = 'in'
    elif _.extract(data.index, '^ж//м') or _.extract(data.index, '^f//m'):
        data.gender = 'fm'
        data.animacy = 'in'
    elif _.extract(data.index, '^ж//с') or _.extract(data.index, '^f//n'):
        data.gender = 'fn'
        data.animacy = 'in'
    elif _.extract(data.index, '^с//м') or _.extract(data.index, '^n//m'):
        data.gender = 'nm'
        data.animacy = 'in'
    elif _.extract(data.index, '^с//ж') or _.extract(data.index, '^n//m'):
        data.gender = 'nm'
        data.animacy = 'in'
    elif _.extract(data.index, '^мо%-жо') or _.extract(data.index, '^mf a'):
        data.gender = 'f'
        data.animacy = 'an'
        data.common_gender = True
    elif _.extract(data.index, '^мн'):
        data.gender = ''
        data.animacy = ''
        data.common_gender = False
        data.pt = True
        if _.extract(data.index, 'одуш'):
            data.animacy = 'an'
        elif _.extract(data.index, 'неод'):
            data.animacy = 'in'
        # end
        # TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
        data.rest_index = data.index
    elif _.extract(data.index, '^мс'):
        data.pronoun = True
    elif _.extract(data.index, '^м'):
        data.gender = 'm'
        data.animacy = get_cyrl_animacy(data.index, 'м')
        data.common_gender = False
    elif _.extract(data.index, '^ж'):
        data.gender = 'f'
        data.animacy = get_cyrl_animacy(data.index, 'ж')
        data.common_gender = False
    elif _.extract(data.index, '^с'):
        data.gender = 'n'
        data.animacy = get_cyrl_animacy(data.index, 'с')
        data.common_gender = False
    else:
        data.gender = _.extract(data.index, '^([mnf])')
        data.animacy = _.extract(data.index, '^[mnf] ([a-z/]+)')
        data.common_gender = False
        if data.animacy:
            convert_animacy = {}
            convert_animacy['in'] = 'in'
            convert_animacy['an'] = 'an'
            convert_animacy['ina'] = 'in'
            convert_animacy['a'] = 'an'
            convert_animacy['a//ina'] = 'an//in'
            convert_animacy['ina//a'] = 'in//an'
            convert_animacy['anin'] = 'an//in'
            convert_animacy['inan'] = 'in//an'
            data.animacy = convert_animacy[data.animacy]
        # end
    # end

    # Удаляем теперь соответствующий кусок индекса
    if (data.gender or data.gender == '') and data.animacy and not data.adj and not data.pronoun:
        _.log_value(data.index, 'data.index')
        orig_index = mw.text.trim(data.index)

#        # local test1 = _.replaced(data.index, '^mf a ?', '')
#        mw.log('test1 = ' + mw.text.trim(test1))
#
#        # local test2 = _.replaced(data.index, '^mf a ', '')
#        mw.log('test2 = ' + mw.text.trim(test2))
#
#        # local test3 = _.replaced(data.index, 'mf a ', '')
#        mw.log('test3 = ' + mw.text.trim(test3))
#
#        # local test4 = _.replaced(data.index, 'mf a', '')
#        mw.log('test4 = ' + mw.text.trim(test4))
#
#        # local test5 = mw.text.trim(_.replaced(data.index, '^mf a ?', ''))
#        mw.log('test5 = ' + test5)
#
#        # local test6 = _.replaced(data.index, '^mf a ?', '')
#        mw.log('test6 = ' + test6)
#        # local test7 = mw.text.trim(test6)
#        mw.log('test7 = ' + test7)

        # TODO: Simplify things a bit here (сделать циклом!):

        rest_index = _.replaced(data.index, '^mf a ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "mf a" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^[mnf]+ [a-z/]+ ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "[mnf] [in/an]" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^мн%.? неод%.? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. неод." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^мн%.? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^[-мжсо/]+%,? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "м/ж/с/мо/жо/со/..." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        return dict(error = 'TODO')  # dict # TODO: process such errors
    elif data.adj:
        _.log_value(data.index, 'data.index (п)')
        orig_index = mw.text.trim(data.index)

        rest_index = _.replaced(data.index, '^п ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "п" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
    elif data.pronoun:
        _.log_value(data.index, 'data.index (мс)')
        orig_index = mw.text.trim(data.index)

        rest_index = _.replaced(data.index, '^мс ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мс" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
    # end
# end


def init(data):
    _.log_func('parse_args', 'init')

    # local several_vovwels, has_stress

    # INFO: Исходное слово без ударения:
    data.word = _.replaced(data.word_stressed, '́ ', '')

    # INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
    data.word_cleared = _.replaced(_.replaced(_.replaced(data.word, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

    if data.adj:
        if _.endswith(data.word_stressed, 'ся'):
            data.postfix = True
            data.stem = _.replaced(data.word, '{vowel}[йяе]ся$', '')
            data.stem_stressed = _.replaced(data.word_stressed, '{vowel}́ ?[йяе]ся$', '')
        else:
            data.stem = _.replaced(data.word, '{vowel}[йяе]$', '')
            data.stem_stressed = _.replaced(data.word_stressed, '{vowel}́ ?[йяе]$', '')
        # end
    else:
        # INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
        data.stem = _.replaced(data.word, '[аеёийоьыя]$', '')
        data.stem_stressed = _.replaced(data.word_stressed, '[аеёийоьыя]́ ?$', '')
    # end

    _.log_value(data.word, 'data.word')
    _.log_value(data.stem, 'data.stem')
    _.log_value(data.stem_stressed, 'data.stem_stressed')

#  INFO: Случай, когда не указано ударение у слова:
    several_vovwels = _.contains_several(data.word_stressed, '{vowel+ё}')
    has_stress = _.contains(data.word_stressed, '[́ ё]')
    if several_vovwels and not has_stress:
        return dict(
            error='Ошибка: Не указано ударение в слове',
            error_category='Ошибка в шаблоне "сущ-ru": не указано ударение в слове',
        )  # dict
    # end
# end


def angle_brackets(data):
    _.log_func('parse_args', 'angle_brackets')

    # local another_index, pt, error

    another_index = _.extract(data.rest_index, '%<([^>]+)%>')
    if another_index:
        pt = data.pt
        if not pt:
            data.output_gender = data.gender
            data.output_animacy = data.animacy
        # end
        data.orig_index = data.index
        data.index = another_index
        error = extract_gender_animacy(data)
        data.pt = pt
        if error: return error # end

        _.log_value(data.adj, 'data.adj')
        if data.adj:  # Для прилагательных надо по-особенному
            error = init(data)
            if error: return data, error # end
        # end
    # end
# end


def parse(base, args):  # export
    _.log_func('parse_args', 'parse')

    # local data, error, parts, n_parts, data1, data2
    # local index_parts, words_parts, n_sub_parts, data_copy

    # INFO: Достаём значения из параметров:
    data = additional.AttrDict()  # AttrDict
    data.base = base
    data.args = args
    data.index = mw.text.trim(args['индекс'])
    data.word_stressed = mw.text.trim(args['слово'])

    _.log_value(data.index, 'data.index')
    _.log_value(data.word_stressed, 'data.word_stressed')

    # mw.log('')
    # mw.log('==================================================')
    # mw.log('args: ' + str(data.index) + ' | ' + str(data.word_stressed))
    # mw.log('--------------------------------------------------')

    # -------------------------------------------------------------------------

    _.log_info('Получение информации о роде и одушевлённости')

    error = extract_gender_animacy(data)

    if error: return data, error # end

    _.log_value(data.gender, 'data.gender')
    _.log_value(data.animacy, 'data.animacy')
    _.log_value(data.common_gender, 'data.common_gender')
    _.log_value(data.adj, 'data.adj')
    _.log_value(data.pronoun, 'data.pronoun')
    _.log_value(data.pt, 'data.pt')
    _.log_value(data.rest_index, 'data.rest_index')

    # INFO: stem, stem_stressed, etc.
    error = init(data)
    if error: return data, error # end

    # INFO: Случай, если род или одушевлённость не указаны:
    if (not data.gender or not data.animacy) and not data.pt:
        return data, dict()  # dict # INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
    # end

    # INFO: Проверяем случай с вариациями:
    parts = mw.text.split(data.rest_index, '//')
    n_parts = additional.table_len(parts)

    if n_parts == 1:  # INFO: Дополнительных вариаций нет
        if _.contains(data.animacy, '//'):  # INFO: Случаи 'in//an' и 'an//in'
            # INFO: Клонируем две вариации на основании текущих данных
            data1 = mw.clone(data)
            data2 = mw.clone(data)

            # INFO: Устанавливаем для них соответствующую вариацию одушевлённости
            data1.animacy = mw.ustring.sub(data.animacy, 1, 2)
            data2.animacy = mw.ustring.sub(data.animacy, 5, 6)

            # INFO: Заполняем атрибут с вариациями
            data.sub_cases = [data1, data2]  # list

            return data, None
            # TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
        # end

        # _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

        index_parts = mw.text.split(data.rest_index, '%+')
        words_parts = mw.text.split(data.word_stressed, '-')
        n_sub_parts = additional.table_len(index_parts)
        if n_sub_parts > 1:
            data.sub_parts = []  # list
            for i in range(1, n_sub_parts + 1):
                data_copy = mw.clone(data)
                data_copy.word_stressed = words_parts[i]

                error = init(data_copy)
                if error: return data, error # end

                data_copy.rest_index = index_parts[i]

                error = angle_brackets(data_copy)
                if error: return data, error # end

                data.sub_parts.append(data_copy)
            # end
            return data, None
        # end

        error = angle_brackets(data)
        if error: return data, error # end

        if _.contains(data.rest_index, '%[%([12]%)%]') or _.contains(data.rest_index, '%[[①②]%]'):
            # INFO: Клонируем две вариации на основании текущих данных
            data1 = mw.clone(data)
            data2 = mw.clone(data)

            # INFO: Устанавливаем факультативность (первый случай):
            data1.rest_index = _.replaced(data1.rest_index, '%[(%([12]%))%]', '')
            data1.rest_index = _.replaced(data1.rest_index, '%[([①②])%]', '')

            # INFO: Устанавливаем факультативность (второй случай):
            data2.rest_index = _.replaced(data2.rest_index, '%[(%([12]%))%]', '%1')
            data2.rest_index = _.replaced(data2.rest_index, '%[([①②])%]', '%1')
            data2.rest_index = _.replaced(data2.rest_index, '%*', '')

            # INFO: Заполняем атрибут с вариациями
            data.sub_cases = [data1, data2]  # list

            return data, None
        # end

    elif n_parts == 2:  # INFO: Вариации "//" для ударения (и прочего индекса)
        _.log_info('> Случай с вариациями //')

        if _.contains(data.animacy, '//'):
            # INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
            return data, dict(error='Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')  # dict
        # end

        # INFO: Клонируем две вариации на основании текущих данных
        data1 = mw.clone(data)
        data2 = mw.clone(data)

        # INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
        data1.rest_index = parts[1]
        data2.rest_index = parts[2]

        # INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
        data2.index = parts[2]  # INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
        extract_gender_animacy(data2)

        # INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
        if not data2.gender and not data2.animacy:
            # INFO: Восстанавливаем прежние общие значения:
            data2.gender = data.gender
            data2.animacy = data.animacy
            data2.common_gender = data.common_gender

        # INFO: Проверка на гипотетическую ошибку в алгоритме:
        elif not data2.gender and data2.animacy or data2.gender and not data2.animacy:
            return data, dict(error='Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей' )  # dict

        # INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
        elif data.gender != data2.gender or data.animacy != data2.animacy or data.common_gender != data2.common_gender:
            data.rest_index = None  # INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
        # end
        data2.index = data.index  # INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

        # INFO: Заполняем атрибут с вариациями
        data.sub_cases = [data1, data2]  # list

    else:  # INFO: Какая-то ошибка, слишком много "//" в индексе
        return data, dict(error='Ошибка: Слишком много частей для "//"')  # dict
    # end

    return data, None  # INFO: `None` здесь -- признак, что нет ошибок
# end


# return export
