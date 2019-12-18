from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...init.parse import noun as noun_parse


module = 'init.parse.common'  # local


@a.starts(module)
def init(func, info):
    # local several_vovwels, has_stress

    # INFO: Исходное слово без ударения:
    info.word = _.replaced(info.word_stressed, '́ ', '')

    # INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
    info.word_cleared = _.replaced(_.replaced(_.replaced(info.word, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

    if info.adj:
        if _.endswith(info.word_stressed, 'ся'):
            info.postfix = True
            info.stem = _.replaced(info.word, '{vowel}[йяе]ся$', '')
            info.stem_stressed = _.replaced(info.word_stressed, '{vowel}́ ?[йяе]ся$', '')
        else:
            info.stem = _.replaced(info.word, '{vowel}[йяе]$', '')
            info.stem_stressed = _.replaced(info.word_stressed, '{vowel}́ ?[йяе]$', '')
        # end
    else:
        # INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
        info.stem = _.replaced(info.word, '[аеёийоьыя]$', '')
        info.stem_stressed = _.replaced(info.word_stressed, '[аеёийоьыя]́ ?$', '')
    # end

    _.log_value(info.word, 'info.word')
    _.log_value(info.stem, 'info.stem')
    _.log_value(info.stem_stressed, 'info.stem_stressed')

#  INFO: Случай, когда не указано ударение у слова:
    several_vovwels = _.contains_several(info.word_stressed, '{vowel+ё}')
    has_stress = _.contains(info.word_stressed, '[́ ё]')
    if several_vovwels and not has_stress:
        _.log_info('Ошибка: Не указано ударение в слове')
        _.ends(module, func)
        return dict(
            error='Ошибка: Не указано ударение в слове',
            error_category='Ошибка в шаблоне "сущ-ru": не указано ударение в слове',
        )  # dict
    # end

    _.ends(module, func)
# end


@a.starts(module)
def angle_brackets(func, info):
    # local another_index, pt, error

    another_index = _.extract(info.rest_index, '%<([^>]+)%>')
    if another_index:
        pt = info.pt
        if not pt:
            info.output_gender = info.gender
            info.output_animacy = info.animacy
        # end
        info.orig_index = info.index
        info.index = another_index
        error = noun_parse.extract_gender_animacy(info)
        info.pt = pt
        if error:
            _.ends(module, func)
            return error
        # end

        _.log_value(info.adj, 'info.adj')
        if info.adj:  # Для прилагательных надо по-особенному?
            error = init(info)
            if error:
                _.ends(module, func)
                return error
            # end
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def parse(func, base, args):  # export
    # local info, error, parts, n_parts, data1, data2
    # local index_parts, words_parts, n_sub_parts, data_copy

    # INFO: Достаём значения из параметров:
    info = a.AttrDict()  # AttrDict
    info.base = base
    info.args = args
    info.lang = mw.text.trim(args['lang'])
    info.unit = mw.text.trim(args['unit'])
    info.index = mw.text.trim(args['индекс'])
    info.word_stressed = mw.text.trim(args['слово'])

    info.noun = (info.unit == 'noun')

    _.log_value(info.index, 'info.index')
    _.log_value(info.word_stressed, 'info.word_stressed')

    # mw.log('')
    # mw.log('==================================================')
    # mw.log('args: ' + str(info.index) + ' | ' + str(info.word_stressed))
    # mw.log('--------------------------------------------------')

    # -------------------------------------------------------------------------

    _.log_info('Получение информации о роде и одушевлённости')

    if info.noun:  # fxime
        error = noun_parse.extract_gender_animacy(info)
        if error:
            _.ends(module, func)
            return info, error
        # end

        _.log_value(info.gender, 'info.gender')
        _.log_value(info.animacy, 'info.animacy')
        _.log_value(info.common_gender, 'info.common_gender')
        _.log_value(info.adj, 'info.adj')
        _.log_value(info.pronoun, 'info.pronoun')
    else:
        info.gender = ''  # fixme
        info.animacy = ''  # fixme
        info.adj = True  # fixme
        info.rest_index = info.index  # fixme
    # end

    _.log_value(info.pt, 'info.pt')
    _.log_value(info.rest_index, 'info.rest_index')

    # INFO: stem, stem_stressed, etc.
    error = init(info)
    if error:
        _.ends(module, func)
        return info, error
    # end

    if info.noun:
        # INFO: Случай, если род или одушевлённость не указаны:
        if (not info.gender or not info.animacy) and not info.pt:
            _.ends(module, func)
            return info, dict()  # dict # INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
        # end
    # end

    # INFO: Проверяем случай с вариациями:
    parts = mw.text.split(info.rest_index, '//')
    n_parts = a.table_len(parts)

    if n_parts == 1:  # INFO: Дополнительных вариаций нет
        if _.contains(info.animacy, '//'):  # INFO: Случаи 'in//an' и 'an//in'
            # INFO: Клонируем две вариации на основании текущих данных
            data1 = mw.clone(info)
            data2 = mw.clone(info)

            # INFO: Устанавливаем для них соответствующую вариацию одушевлённости
            data1.animacy = mw.ustring.sub(info.animacy, 1, 2)
            data2.animacy = mw.ustring.sub(info.animacy, 5, 6)

            # INFO: Заполняем атрибут с вариациями
            info.sub_cases = [data1, data2]  # list

            _.ends(module, func)
            return info, None
            # TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
        # end

        # _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

        index_parts = mw.text.split(info.rest_index, '%+')
        words_parts = mw.text.split(info.word_stressed, '-')
        n_sub_parts = a.table_len(index_parts)
        if n_sub_parts > 1:
            info.sub_parts = []  # list
            for i in range(1, n_sub_parts + 1):
                data_copy = mw.clone(info)
                data_copy.word_stressed = words_parts[i]

                error = init(data_copy)
                if error:
                    _.ends(module, func)
                    return info, error
                # end

                data_copy.rest_index = index_parts[i]

                if info.noun:
                    error = angle_brackets(data_copy)
                    if error:
                        _.ends(module, func)
                        return info, error
                    # end
                # end

                info.sub_parts.append(data_copy)
            # end
            _.ends(module, func)
            return info, None
        # end

        if info.noun:
            error = angle_brackets(info)
            if error:
                _.ends(module, func)
                return info, error
            # end
        # end

        if _.contains(info.rest_index, '%[%([12]%)%]') or _.contains(info.rest_index, '%[[①②]%]'):
            # INFO: Клонируем две вариации на основании текущих данных
            data1 = mw.clone(info)
            data2 = mw.clone(info)

            # INFO: Устанавливаем факультативность (первый случай):
            data1.rest_index = _.replaced(data1.rest_index, '%[(%([12]%))%]', '')
            data1.rest_index = _.replaced(data1.rest_index, '%[([①②])%]', '')

            # INFO: Устанавливаем факультативность (второй случай):
            data2.rest_index = _.replaced(data2.rest_index, '%[(%([12]%))%]', '%1')
            data2.rest_index = _.replaced(data2.rest_index, '%[([①②])%]', '%1')
            data2.rest_index = _.replaced(data2.rest_index, '%*', '')

            # INFO: Заполняем атрибут с вариациями
            info.sub_cases = [data1, data2]  # list

            _.ends(module, func)
            return info, None
        # end

    elif n_parts == 2:  # INFO: Вариации "//" для ударения (и прочего индекса)
        _.log_info('> Случай с вариациями //')

        if _.contains(info.animacy, '//'):
            # INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
            _.ends(module, func)
            return info, dict(error='Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')  # dict
        # end

        # INFO: Клонируем две вариации на основании текущих данных
        data1 = mw.clone(info)
        data2 = mw.clone(info)

        # INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
        data1.rest_index = parts[0]
        data2.rest_index = parts[1]

        if info.noun:
            # INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
            data2.index = parts[1]  # INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
            noun_parse.extract_gender_animacy(data2)
        # end

        # INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
        if not data2.gender and not data2.animacy:
            # INFO: Восстанавливаем прежние общие значения:
            data2.gender = info.gender
            data2.animacy = info.animacy
            data2.common_gender = info.common_gender

        # INFO: Проверка на гипотетическую ошибку в алгоритме:
        elif not data2.gender and data2.animacy or data2.gender and not data2.animacy:
            _.ends(module, func)
            return info, dict(error='Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей' )  # dict

        # INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
        elif info.gender != data2.gender or info.animacy != data2.animacy or info.common_gender != data2.common_gender:
            info.rest_index = None  # INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
        # end
        data2.index = info.index  # INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

        # INFO: Заполняем атрибут с вариациями
        info.sub_cases = [data1, data2]  # list

    else:  # INFO: Какая-то ошибка, слишком много "//" в индексе
        _.ends(module, func)
        return info, dict(error='Ошибка: Слишком много частей для "//"')  # dict
    # end

    _.ends(module, func)
    return info, None  # INFO: `None` здесь -- признак, что нет ошибок
# end


# return export
