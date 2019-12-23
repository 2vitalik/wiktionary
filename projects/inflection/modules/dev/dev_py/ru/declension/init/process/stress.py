from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...data.stress import adj as adj_stress
from ...data.stress import pronoun as pronoun_stress
from ...data.stress import noun as noun_stress
from ...output import result as r


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
    allowed_stress_types = {
        'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
        'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
        'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
    }

    # INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
    if i.stress_type and not _.equals(i.stress_type, allowed_stress_types):
        r.add_error(i, 'Ошибка: Неправильная схема ударения: ' + i.stress_type)
    # end

    _.ends(module, func)
# end


@a.starts(module)
def get_stress_schema(func, i):  # export
    if i.adj:
        i.stress_schema = adj_stress.get_adj_stress_schema(i.stress_type)
    elif i.pronoun:
        i.stress_schema = pronoun_stress.get_pronoun_stress_schema(i.stress_type)
    else:
        i.stress_schema = noun_stress.get_noun_stress_schema(i.stress_type)
    # end

    _.ends(module, func)
# end


# return export
