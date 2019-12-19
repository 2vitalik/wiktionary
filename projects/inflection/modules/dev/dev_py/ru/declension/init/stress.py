from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..data.stress import adj as adj_stress
from ..data.stress import pronoun as pronoun_stress
from ..data.stress import noun as noun_stress


module = 'init.stress'  # local


@a.starts(module)
def extract_stress_type(func, rest_index):  # export
    #    OLD: Старая версия кода:
#    # local stress_regexp = "([abcdef][′']?[′']?)"
#    # local stress_regexp2 = '(' + stress_regexp + '.*//.*' + stress_regexp + ')'
#    stress_regexp = '(' + stress_regexp + '(% ?.*))'
#    data.stress_type = _.extract(rest_index, stress_regexp2)
#    if not data.stress_type:
#        data.stress_type = _.extract(rest_index, stress_regexp)
#    # end
    # local stress_type, allowed_stress_types

    # INFO: Извлечение ударения из оставшейся части индекса:
    stress_type = _.extract(rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

    # INFO: Замена особых апострофов в ударении на обычные:
    if stress_type:
        stress_type = _.replaced(stress_type, '′', "'")
    # end

    # INFO: Список допустимых схем ударений:
    allowed_stress_types = {
        'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
        'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
        'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
    }

    # INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
    if stress_type and not _.equals(stress_type, allowed_stress_types):
        _.ends(module, func)
        return stress_type, dict(error='Ошибка: Неправильная схема ударения: ' + stress_type)  # dict
    # end

    _.ends(module, func)
    return stress_type, None  # INFO: `None` здесь -- признак, что нет ошибок
# end


@a.starts(module)
def get_stress_schema(func, stress_type, adj, pronoun):  # export
    result = ''  # local
    if adj:
        result = adj_stress.get_adj_stress_schema(stress_type)
    elif pronoun:
        result = pronoun_stress.get_pronoun_stress_schema(stress_type)
    else:
        result = noun_stress.get_noun_stress_schema(stress_type)
    # end

    _.ends(module, func)
    return result
# end


# return export
