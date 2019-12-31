from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...init.parse import noun as noun_parse
from ...init import _process as p
from ...run.result import error as e


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

    _.log_value(i.word.unstressed, 'i.word.unstressed')
    _.log_value(i.stem.unstressed, 'i.stem.unstressed')
    _.log_value(i.stem.stressed, 'i.stem.stressed')

#  INFO: Случай, когда не указано ударение у слова:
    several_vowels = _.contains_several(i.word.stressed, '{vowel+ё}')
    has_stress = _.contains(i.word.stressed, '[́ ё]')
    if several_vowels and not has_stress:
        _.log_info('Ошибка: Не указано ударение в слове')
        e.add_error(i, 'Ошибка: Не указано ударение в слове')
        i.result.error_category = 'Ошибка в шаблоне "сущ-ru" (не указано ударение в слове)'
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
        if e.has_error(i):
            return _.ends(module, func)
        # end

        _.log_value(i.adj, 'i.adj')
        if i.adj:  # fixme: Для прилагательных надо по-особенному?
            init_info(i)
            if e.has_error(i):
                return _.ends(module, func)
            # end
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def parse(func, base, args):  # export
    i = a.AttrDict()  # AttrDict  # local
    i.word = a.AttrDict()  # AttrDict                                      #
    i.stem = a.AttrDict()  # AttrDict                                      #

    # INFO: Достаём значения из параметров:
    i.base = base
    i.args = args
    i.lang = mw.text.trim(args['lang'])
    i.unit = mw.text.trim(args['unit'])
    i.index = mw.text.trim(args['индекс'])
    i.word.stressed = mw.text.trim(args['слово'])
    i.noun = (i.unit == 'noun')

    i.parts = a.AttrDict()  # AttrDict
    i.result = a.AttrDict()  # AttrDict
    i.result.error = ''

    i.has_index = True  # изначально предполагаем, что индекс есть

    _.log_value(i.index, 'i.index')
    _.log_value(i.word.stressed, 'i.word.stressed')

    # mw.log('')
    # mw.log('==================================================')
    # mw.log('args: ' + str(i.index) + ' | ' + str(i.word.stressed))
    # mw.log('--------------------------------------------------')

    _.log_info('Получение информации о роде и одушевлённости')

    if i.noun:  # fxime
        noun_parse.extract_gender_animacy(i)
        if e.has_error(i):
            _.ends(module, func)
            return i
        # end

        _.log_value(i.gender, 'i.gender')
        _.log_value(i.animacy, 'i.animacy')
        _.log_value(i.common_gender, 'i.common_gender')
        _.log_value(i.adj, 'i.adj')
        _.log_value(i.pronoun, 'i.pronoun')
    else:
        i.gender = ''  # fixme
        i.animacy = ''  # fixme
        i.adj = True  # fixme
        i.rest_index = i.index  # fixme
    # end

    _.log_value(i.pt, 'i.pt')
    _.log_value(i.rest_index, 'i.rest_index')

    # INFO: stem, stem.stressed, etc.
    init_info(i)  # todo: rename to `init_stem`
    if e.has_error(i):
        _.ends(module, func)
        return i
    # end

    if i.noun:
        # INFO: Случай, если род или одушевлённость не указаны:
        if (not i.gender or not i.animacy) and not i.pt:
            # INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
            _.ends(module, func)
            return i
        # end
    # end

    # INFO: Проверяем случай с вариациями:
    parts = mw.text.split(i.rest_index, '//')  # local
    n_parts = a.table_len(parts)  # local

    if n_parts == 1:  # INFO: Дополнительных вариаций нет
        if _.contains(i.animacy, '//'):  # INFO: Случаи 'in//an' и 'an//in'
            # INFO: Клонируем две вариации на основании текущих данных
            i_1 = mw.clone(i)  # local
            i_2 = mw.clone(i)  # local

            # INFO: Устанавливаем для них соответствующую вариацию одушевлённости
            i_1.animacy = mw.ustring.sub(i.animacy, 1, 2)
            i_2.animacy = mw.ustring.sub(i.animacy, 5, 6)

            # INFO: Заполняем атрибут с вариациями
            i.variations = [p.process(i_1), p.process(i_2)]  # list

            _.ends(module, func)
            return i
            # TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
        # end

        # _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

        index_parts = mw.text.split(i.rest_index, '%+')  # local
        words_parts = mw.text.split(i.word.stressed, '-')  # local
        n_sub_parts = a.table_len(index_parts)  # local
        if n_sub_parts > 1:
            i.plus = []  # list
            for j in range(n_sub_parts):
                i_copy = mw.clone(i)  # local
                i_copy.word.stressed = words_parts[i]

                init_info(i_copy)
                if e.has_error(i_copy):
                    e.add_error(i, i_copy.result.error)
                    _.ends(module, func)
                    return i
                # end

                i_copy.rest_index = index_parts[i]

                if i.noun:
                    angle_brackets(i_copy)
                    if e.has_error(i_copy):
                        e.add_error(i, i_copy.result.error)
                        _.ends(module, func)
                        return i
                    # end
                # end

                i.plus.append(p.process(i_copy))
            # end
            _.ends(module, func)
            return i
        # end

        if i.noun:
            angle_brackets(i)
            if e.has_error(i):
                _.ends(module, func)
                return i
            # end
        # end

        if _.contains(i.rest_index, '%[%([12]%)%]') or _.contains(i.rest_index, '%[[①②]%]'):
            # INFO: Клонируем две вариации на основании текущих данных
            i_1 = mw.clone(i)  # local
            i_2 = mw.clone(i)  # local

            # INFO: Устанавливаем факультативность (первый случай):
            i_1.rest_index = _.replaced(i_1.rest_index, '%[(%([12]%))%]', '')
            i_1.rest_index = _.replaced(i_1.rest_index, '%[([①②])%]', '')

            # INFO: Устанавливаем факультативность (второй случай):
            i_2.rest_index = _.replaced(i_2.rest_index, '%[(%([12]%))%]', '%1')
            i_2.rest_index = _.replaced(i_2.rest_index, '%[([①②])%]', '%1')
            i_2.rest_index = _.replaced(i_2.rest_index, '%*', '')

            # INFO: Заполняем атрибут с вариациями
            i.variations = [p.process(i_1), p.process(i_2)]  # list

            _.ends(module, func)
            return i
        # end

    elif n_parts == 2:  # INFO: Вариации "//" для ударения (и прочего индекса)
        _.log_info('> Случай с вариациями //')

        if _.contains(i.animacy, '//'):
            # INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
            e.add_error(i, 'Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')
            _.ends(module, func)
            return i
        # end

        # INFO: Клонируем две вариации на основании текущих данных
        i_1 = mw.clone(i)  # local
        i_2 = mw.clone(i)  # local

        # INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
        i_1.rest_index = parts[0]
        i_2.rest_index = parts[1]

        if i.noun:
            # INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
            i_2.index = parts[1]  # INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
            noun_parse.extract_gender_animacy(i_2)
        # end

        # INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
        if not i_2.gender and not i_2.animacy:
            # INFO: Восстанавливаем прежние общие значения:
            i_2.gender = i.gender
            i_2.animacy = i.animacy
            i_2.common_gender = i.common_gender

        # INFO: Проверка на гипотетическую ошибку в алгоритме:
        elif not i_2.gender and i_2.animacy or i_2.gender and not i_2.animacy:
            e.add_error(i, 'Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей')
            _.ends(module, func)
            return i

        # INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
        elif i.gender != i_2.gender or i.animacy != i_2.animacy or i.common_gender != i_2.common_gender:
            i.rest_index = None  # INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
        # end
        i_2.index = i.index  # INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

        # INFO: Заполняем атрибут с вариациями
        i.variations = [p.process(i_1), p.process(i_2)]  # list

        _.ends(module, func)
        return i

    else:  # INFO: Какая-то ошибка, слишком много "//" в индексе
        e.add_error(i, 'Ошибка: Слишком много частей для "//"')
        _.ends(module, func)
        return i
    # end

    _.ends(module, func)
    return p.process(i)
# end


# return export
