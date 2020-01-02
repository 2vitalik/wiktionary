from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...init import _process as p
from ...init.parse import angle_brackets as angle
from ...init.parse import init_stem as init_stem
from ...init.parse import noun as noun_parse
from ...run.result import error as e


module = 'init.parse.variations'  # local


@a.starts(module)
def process_animacy_variations(func, i):  # export
    # INFO: Клонируем две вариации на основании текущих данных
    i_1 = mw.clone(i)  # local
    i_2 = mw.clone(i)  # local

    # INFO: Устанавливаем для них соответствующую вариацию одушевлённости
    i_1.animacy = mw.ustring.sub(i.animacy, 1, 2)
    i_2.animacy = mw.ustring.sub(i.animacy, 5, 6)

    # INFO: Заполняем атрибут с вариациями
    i.variations = [p.process(i_1), p.process(i_2)]  # list

    _.ends(module, func)
# end


@a.starts(module)
def process_plus(func, i, plus_words, plus_index):  # export
    i.plus = []  # list
    n_plus = a.table_len(plus_index)  # local
    for j in range(n_plus):
        i_copy = mw.clone(i)  # local
        i_copy.word.stressed = plus_words[i]

        init_stem.init_stem(i_copy)
        if e.has_error(i_copy):
            e.add_error(i, i_copy.result.error)
            return _.ends(module, func)
        # end

        i_copy.rest_index = plus_index[j]

        if i.noun:
            angle.angle_brackets(i_copy)
            if e.has_error(i_copy):
                e.add_error(i, i_copy.result.error)
                return _.ends(module, func)
            # end
        # end

        i.plus.append(p.process(i_copy))
    # end

    _.ends(module, func)
# end


@a.starts(module)
def process_brackets_variations(func, i):  # export
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
# end


@a.starts(module)
def process_full_variations(func, i, parts):  # export
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
        return _.ends(module, func)

    # INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
    elif i.gender != i_2.gender or i.animacy != i_2.animacy or i.common_gender != i_2.common_gender:
        i.rest_index = None  # INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
    # end
    i_2.index = i.index  # INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

    # INFO: Заполняем атрибут с вариациями
    i.variations = [p.process(i_1), p.process(i_2)]  # list

    _.ends(module, func)
# end


# return export
