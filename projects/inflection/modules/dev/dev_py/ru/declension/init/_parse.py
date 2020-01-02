from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..init import _process as p
from ..init.parse import angle_brackets as angle
from ..init.parse import init_stem as init_stem
from ..init.parse import noun as noun_parse
from ..init.parse import variations as v
from ..run.result import error as e


module = 'init.parse'  # local


@a.starts(module)
def parse(func, base, args, frame):  # export
    i = a.AttrDict()  # AttrDict  # local
    i.word = a.AttrDict()  # AttrDict
    i.stem = a.AttrDict()  # AttrDict
    i.parts = a.AttrDict()  # AttrDict
    i.result = a.AttrDict()  # AttrDict
    i.result.error = ''
    i.has_index = True  # изначально предполагаем, что индекс есть

    # INFO: Достаём значения из параметров:
    i.base = base
    i.args = args
    i.frame = frame
    i.lang = mw.text.trim(args['lang'])
    i.unit = mw.text.trim(args['unit'])
    i.index = mw.text.trim(args['индекс'])
    i.word.stressed = mw.text.trim(args['слово'])
    i.noun = (i.unit == 'noun')

    _.log_value(i.index, 'i.index')
    _.log_value(i.word.stressed, 'i.word.stressed')

    # mw.log('')
    # mw.log('==================================================')
    # mw.log('args: ' + str(i.index) + ' | ' + str(i.word.stressed))
    # mw.log('--------------------------------------------------')

    _.log_info('Получение информации о роде и одушевлённости')

    if i.noun:  # fixme
        noun_parse.extract_gender_animacy(i)
        if e.has_error(i):
            return _.returns(module, func, i)
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
    init_stem.init_stem(i)
    if e.has_error(i):
        return _.returns(module, func, i)
    # end

    if i.noun:
        # INFO: Случай, если род или одушевлённость не указаны:
        if (not i.gender or not i.animacy) and not i.pt:
            # INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
            return _.returns(module, func, i)
        # end
    # end

    # INFO: Проверяем случай с вариациями:
    variations = mw.text.split(i.rest_index, '//')  # local  # todo: rename
    n_variations = a.table_len(variations)  # local

    if n_variations == 1:  # INFO: Дополнительных вариаций нет
        if _.contains(i.animacy, '//'):  # INFO: Случаи 'in//an' и 'an//in'
            v.process_animacy_variations(i)
            return _.returns(module, func, i)
            # TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
        # end

        # _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

        plus_index = mw.text.split(i.rest_index, '%+')  # local
        plus_words = mw.text.split(i.word.stressed, '-')  # local
        n_plus = a.table_len(plus_index)  # local
        if n_plus > 1:
            v.process_plus(i, plus_words, plus_index)
            return _.returns(module, func, i)
        # end

        if i.noun:
            angle.angle_brackets(i)
            if e.has_error(i):
                return _.returns(module, func, i)
            # end
        # end

        if _.contains(i.rest_index, '%[%([12]%)%]') or _.contains(i.rest_index, '%[[①②]%]'):
            v.process_brackets_variations(i)
            return _.returns(module, func, i)
        # end

    elif n_variations == 2:  # INFO: Вариации "//" для ударения (и прочего индекса)
        _.log_info('> Случай с вариациями //')

        if _.contains(i.animacy, '//'):
            # INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
            e.add_error(i, 'Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')
            return _.returns(module, func, i)
        # end

        v.process_full_variations(i, variations)

        return _.returns(module, func, i)

    else:  # INFO: Какая-то ошибка, слишком много "//" в индексе
        e.add_error(i, 'Ошибка: Слишком много частей для "//"')
        return _.returns(module, func, i)
    # end

    _.ends(module, func)
    return p.process(i)
# end


# return export
