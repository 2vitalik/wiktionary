from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...init.parse import noun as noun_parse
from ...init import _process as p
from ...run.out import result as r


module = 'init.parse.common'  # local


@a.starts(module)
def init_info(func, i):  # todo rename to `init_stem`
    # local several_vowels, has_stress

    # INFO: Исходное слово без ударения:
    i.word.unstressed = _.replaced(i.word.stressed, '́ ', '')  # todo: move outside this function

    # INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
    i.word.cleared = _.replaced(_.replaced(_.replaced(i.word.unstressed, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

    if i.adj:
        if _.endswith(i.word.stressed, 'ся'):
            i.postfix = True
            i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]ся$', '')
            i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]ся$', '')
        else:
            i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]$', '')
            i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]$', '')
        # end
    else:
        # INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
        i.stem.unstressed = _.replaced(i.word.unstressed, '[аеёийоьыя]$', '')
        i.stem.stressed = _.replaced(i.word.stressed, '[аеёийоьыя]́ ?$', '')
    # end

    _.log_value(i.word.unstressed, 'info.word.unstressed')
    _.log_value(i.stem.unstressed, 'info.stem.unstressed')
    _.log_value(i.stem.stressed, 'info.stem.stressed')

#  INFO: Случай, когда не указано ударение у слова:
    several_vowels = _.contains_several(i.word.stressed, '{vowel+ё}')
    has_stress = _.contains(i.word.stressed, '[́ ё]')
    if several_vowels and not has_stress:
        _.log_info('Ошибка: Не указано ударение в слове')
        r.add_error(i, 'Ошибка: Не указано ударение в слове')
        i.out_args.error_category = 'Ошибка в шаблоне "сущ-ru" (не указано ударение в слове)'
    # end

    _.ends(module, func)
# end


@a.starts(module)
def angle_brackets(func, i):
    another_index = _.extract(i.rest_index, '%<([^>]+)%>')  # local
    if another_index:
        pt = i.pt  # local
        if not pt:
            i.output_gender = i.gender
            i.output_animacy = i.animacy
        # end
        i.orig_index = i.index
        i.index = another_index
        noun_parse.extract_gender_animacy(i)
        i.pt = pt
        if r.has_error(i):
            return _.ends(module, func)
        # end

        _.log_value(i.adj, 'info.adj')
        if i.adj:  # fixme: Для прилагательных надо по-особенному?
            init_info(i)
            if r.has_error(i):
                return _.ends(module, func)
            # end
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def parse(func, base, args):  # export
    info = a.AttrDict()  # AttrDict  # local
    info.word = a.AttrDict()  # AttrDict                                      #
    info.stem = a.AttrDict()  # AttrDict                                      #

    # INFO: Достаём значения из параметров:
    info.base = base
    info.args = args
    info.lang = mw.text.trim(args['lang'])
    info.unit = mw.text.trim(args['unit'])
    info.index = mw.text.trim(args['индекс'])
    info.word.stressed = mw.text.trim(args['слово'])
    info.noun = (info.unit == 'noun')

    info.data = a.AttrDict()  # AttrDict
    info.out_args = a.AttrDict()  # AttrDict
    info.out_args.error = ''

    info.has_index = True  # изначально предполагаем, что индекс есть

    _.log_value(info.index, 'info.index')
    _.log_value(info.word.stressed, 'info.word.stressed')

    # mw.log('')
    # mw.log('==================================================')
    # mw.log('args: ' + str(info.index) + ' | ' + str(info.word.stressed))
    # mw.log('--------------------------------------------------')

    _.log_info('Получение информации о роде и одушевлённости')

    if info.noun:  # fxime
        noun_parse.extract_gender_animacy(info)
        if r.has_error(info):
            _.ends(module, func)
            return info
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

    # INFO: stem, stem.stressed, etc.
    init_info(info)  # todo: rename to `init_stem`
    if r.has_error(info):
        _.ends(module, func)
        return info
    # end

    if info.noun:
        # INFO: Случай, если род или одушевлённость не указаны:
        if (not info.gender or not info.animacy) and not info.pt:
            # INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
            _.ends(module, func)
            return info
        # end
    # end

    # INFO: Проверяем случай с вариациями:
    parts = mw.text.split(info.rest_index, '//')  # local
    n_parts = a.table_len(parts)  # local

    if n_parts == 1:  # INFO: Дополнительных вариаций нет
        if _.contains(info.animacy, '//'):  # INFO: Случаи 'in//an' и 'an//in'
            # INFO: Клонируем две вариации на основании текущих данных
            info_1 = mw.clone(info)  # local
            info_2 = mw.clone(info)  # local

            # INFO: Устанавливаем для них соответствующую вариацию одушевлённости
            info_1.animacy = mw.ustring.sub(info.animacy, 1, 2)
            info_2.animacy = mw.ustring.sub(info.animacy, 5, 6)

            # INFO: Заполняем атрибут с вариациями
            info.variations = [p.process(info_1), p.process(info_2)]  # list

            _.ends(module, func)
            return info
            # TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
        # end

        # _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

        index_parts = mw.text.split(info.rest_index, '%+')  # local
        words_parts = mw.text.split(info.word.stressed, '-')  # local
        n_sub_parts = a.table_len(index_parts)  # local
        if n_sub_parts > 1:
            info.plus = []  # list
            for i in range(n_sub_parts):
                info_copy = mw.clone(info)  # local
                info_copy.word.stressed = words_parts[i]

                init_info(info_copy)
                if r.has_error(info_copy):
                    r.add_error(info, info_copy.out_args.error)
                    _.ends(module, func)
                    return info
                # end

                info_copy.rest_index = index_parts[i]

                if info.noun:
                    angle_brackets(info_copy)
                    if r.has_error(info_copy):
                        r.add_error(info, info_copy.out_args.error)
                        _.ends(module, func)
                        return info
                    # end
                # end

                info.plus.append(p.process(info_copy))
            # end
            _.ends(module, func)
            return info
        # end

        if info.noun:
            angle_brackets(info)
            if r.has_error(info):
                _.ends(module, func)
                return info
            # end
        # end

        if _.contains(info.rest_index, '%[%([12]%)%]') or _.contains(info.rest_index, '%[[①②]%]'):
            # INFO: Клонируем две вариации на основании текущих данных
            info_1 = mw.clone(info)  # local
            info_2 = mw.clone(info)  # local

            # INFO: Устанавливаем факультативность (первый случай):
            info_1.rest_index = _.replaced(info_1.rest_index, '%[(%([12]%))%]', '')
            info_1.rest_index = _.replaced(info_1.rest_index, '%[([①②])%]', '')

            # INFO: Устанавливаем факультативность (второй случай):
            info_2.rest_index = _.replaced(info_2.rest_index, '%[(%([12]%))%]', '%1')
            info_2.rest_index = _.replaced(info_2.rest_index, '%[([①②])%]', '%1')
            info_2.rest_index = _.replaced(info_2.rest_index, '%*', '')

            # INFO: Заполняем атрибут с вариациями
            info.variations = [p.process(info_1), p.process(info_2)]  # list

            _.ends(module, func)
            return info
        # end

    elif n_parts == 2:  # INFO: Вариации "//" для ударения (и прочего индекса)
        _.log_info('> Случай с вариациями //')

        if _.contains(info.animacy, '//'):
            # INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
            r.add_error(info, 'Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')
            _.ends(module, func)
            return info
        # end

        # INFO: Клонируем две вариации на основании текущих данных
        info_1 = mw.clone(info)  # local
        info_2 = mw.clone(info)  # local

        # INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
        info_1.rest_index = parts[0]
        info_2.rest_index = parts[1]

        if info.noun:
            # INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
            info_2.index = parts[1]  # INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
            noun_parse.extract_gender_animacy(info_2)
        # end

        # INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
        if not info_2.gender and not info_2.animacy:
            # INFO: Восстанавливаем прежние общие значения:
            info_2.gender = info.gender
            info_2.animacy = info.animacy
            info_2.common_gender = info.common_gender

        # INFO: Проверка на гипотетическую ошибку в алгоритме:
        elif not info_2.gender and info_2.animacy or info_2.gender and not info_2.animacy:
            r.add_error(info, 'Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей')
            _.ends(module, func)
            return info

        # INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
        elif info.gender != info_2.gender or info.animacy != info_2.animacy or info.common_gender != info_2.common_gender:
            info.rest_index = None  # INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
        # end
        info_2.index = info.index  # INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

        # INFO: Заполняем атрибут с вариациями
        info.variations = [p.process(info_1), p.process(info_2)]  # list

        _.ends(module, func)
        return info

    else:  # INFO: Какая-то ошибка, слишком много "//" в индексе
        r.add_error(info, 'Ошибка: Слишком много частей для "//"')
        _.ends(module, func)
        return info
    # end

    _.ends(module, func)
    return p.process(info)
# end


# return export
