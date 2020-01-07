from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from shared_utils.io.json import json_load
from ...run.result import error as e


module = 'init.process.stress'  # local


@a.starts(module)
def extract_stress_type(func, i):  # export
    #    OLD: Старая версия кода:
#    # local stress_regexp = "([abcdef][′']?[′']?)"
#    # local stress_regexp2 = '(' + stress_regexp + '.*//.*' + stress_regexp + ')'
#    stress_regexp = '(' + stress_regexp + '(% ?.*))'
#    i.stress_type = _.extract(i.rest_index, stress_regexp2)
#    if not i.stress_type:
#        i.stress_type = _.extract(i.rest_index, stress_regexp)
#    # end
    # local stress_type, allowed_stress_types

    # INFO: Извлечение ударения из оставшейся части индекса:
    i.stress_type = _.extract(i.rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

    # INFO: Замена особых апострофов в ударении на обычные:
    if i.stress_type:
        i.stress_type = _.replaced(i.stress_type, '′', "'")
    # end

    # INFO: Список допустимых схем ударений:
    allowed_stress_types = {  # todo: special variables for that?
        'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
        'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
        'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
    }

    # INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
    if i.stress_type and not _.equals(i.stress_type, allowed_stress_types):
        e.add_error(i, 'Ошибка: Неправильная схема ударения: ' + i.stress_type)
    # end

    _.ends(module, func)
# end


@a.starts(module)
def get_stress_schema(func, i):  # export
    if _.contains(i.rest_index, '0'):
        _.log_info('Игнорируем схему ударения для случая "0"')
        i.stress_schema = dict()  # dict
        return _.ends(module, func)
    # end

    unit = ''  # todo: get from i.unit ?
    if i.adj:
        unit = 'adj'
    elif i.pronoun:
        unit = 'pronoun'
    else:
        unit = 'noun'
    # end
    _.log_value(unit, 'unit')
    _.log_value(i.unit, 'i.unit')

    stress_schemas = json_load('../modules/dev/dev_py/ru/declension/data/stress/' + unit + '.json')
    i.stress_schema = stress_schemas[i.stress_type]

    _.log_table(i.stress_schema['stem'], "i.stress_schema['stem']")
    _.log_table(i.stress_schema['ending'], "i.stress_schema['ending']")

    _.ends(module, func)
# end


# return export
