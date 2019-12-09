from projects.inflection.modules.dev.py import additional
from projects.inflection.modules.dev.py import mw
from projects.inflection.modules.dev.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...noun import parse_args as noun_parse_args


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
        _.log_info('Ошибка: Не указано ударение в слове')
        return dict(
            error='Ошибка: Не указано ударение в слове',
            error_category='Ошибка в шаблоне "сущ-ru": не указано ударение в слове',
        )  # dict
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
    data.lang = mw.text.trim(args['lang'])
    data.unit = mw.text.trim(args['unit'])
    data.index = mw.text.trim(args['индекс'])
    data.word_stressed = mw.text.trim(args['слово'])

    data.noun = (data.unit == 'noun')

    _.log_value(data.index, 'data.index')
    _.log_value(data.word_stressed, 'data.word_stressed')

    # mw.log('')
    # mw.log('==================================================')
    # mw.log('args: ' + str(data.index) + ' | ' + str(data.word_stressed))
    # mw.log('--------------------------------------------------')

    # -------------------------------------------------------------------------

    _.log_info('Получение информации о роде и одушевлённости')

    if data.noun:  # fxime
        error = noun_parse_args.extract_gender_animacy(data)
        if error: return data, error # end

        _.log_value(data.gender, 'data.gender')
        _.log_value(data.animacy, 'data.animacy')
        _.log_value(data.common_gender, 'data.common_gender')
        _.log_value(data.adj, 'data.adj')
        _.log_value(data.pronoun, 'data.pronoun')
    else:
        data.gender = ''  # fixme
        data.animacy = ''  # fixme
        data.adj = True  # fixme
        data.rest_index = data.index  # fixme
    # end

    _.log_value(data.pt, 'data.pt')
    _.log_value(data.rest_index, 'data.rest_index')

    # INFO: stem, stem_stressed, etc.
    error = init(data)
    if error: return data, error # end

    if data.noun:
        # INFO: Случай, если род или одушевлённость не указаны:
        if (not data.gender or not data.animacy) and not data.pt:
            return data, dict()  # dict # INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
        # end
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

                if data.noun:
                    error = noun_parse_args.angle_brackets(data_copy)
                    if error: return data, error # end
                # end

                data.sub_parts.append(data_copy)
            # end
            return data, None
        # end

        if data.noun:
            error = noun_parse_args.angle_brackets(data)
            if error: return data, error # end
        # end

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
        data1.rest_index = parts[0]
        data2.rest_index = parts[1]

        if data.noun:
            # INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
            data2.index = parts[1]  # INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
            noun_parse_args.extract_gender_animacy(data2)
        # end

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
