from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'data.stress.adj'  # local


# Данные: ударность основы и окончания в зависимости от схемы ударения
@a.starts(module)
def get_adj_stress_schema(func, stress_type):  # export  # INFO: Вычисление схемы ударения
    # local stress_schema, types, cases, sg_value

    # todo: Сгенерировать все `stress_schema` для всех видов `stress_type` заранее и потом просто использовать/загружать их

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    stress_schema = a.AttrDict()  # AttrDict  # local
    stress_schema.stem = dict()  # dict
    stress_schema.ending = dict()  # dict
    stress_schema.stem['full'] = _.startswith(stress_type, ["a", "a/"])
    stress_schema.stem['srt-sg-m'] = True
    stress_schema.stem['srt-sg-f'] = _.endswith(stress_type, ["/a", "/a'"]) or _.equals(stress_type, ['a', "a'"])
    stress_schema.stem['srt-sg-n'] = _.endswith(stress_type, ["/a", "/c", "/a'", "/c'", "/c''"]) or _.equals(stress_type, ['a', "a'"])
    stress_schema.stem['srt-pl'] = _.endswith(stress_type, ["/a", "/c", "/a'", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['a', "a'", "b'"])
    stress_schema.ending['full'] = _.startswith(stress_type, ["b", "b/"])
    stress_schema.ending['srt-sg-m'] = False
    stress_schema.ending['srt-sg-f'] = _.endswith(stress_type, ["/b", "/c", "/a'", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['b', "a'", "b'"])
    stress_schema.ending['srt-sg-n'] = _.endswith(stress_type, ["/b", "/b'", "/c''"]) or _.equals(stress_type, ['b', "b'"])
    stress_schema.ending['srt-pl'] = _.endswith(stress_type, ["/b", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['b', "b'"])

    types = ['stem', 'ending']
    cases = [
        'sg', 'pl',
        'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
        'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
    ]  # list
    for i, type in enumerate(types):
        sg_value = stress_schema[type]['full']
        for i, case in enumerate(cases):
            stress_schema[type][case] = sg_value
        # end
    # end

    _.ends(module, func)
    return stress_schema
# end


# return export
