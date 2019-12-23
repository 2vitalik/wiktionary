from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'data.stress.pronoun'  # local


@a.starts(module)
def get_pronoun_stress_schema(func, stress_type):  # export  # INFO: Вычисление схемы ударения

    # todo: Сгенерировать все `stress_schema` для всех видов `stress_type` заранее и потом просто использовать/загружать их

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = a.AttrDict()  # AttrDict  # local
    stress_schema.stem = dict()  # dict
    stress_schema.ending = dict()  # dict
    stress_schema.stem['sg'] = _.equals(stress_type, "a")
    stress_schema.stem['pl'] = _.equals(stress_type, "a")
    stress_schema.ending['sg'] = _.equals(stress_type, "b")
    stress_schema.ending['pl'] = _.equals(stress_type, "b")

    types = ['stem', 'ending']
    sg_cases = ['nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg']  # list
    pl_cases = ['nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl']  # list
    for i, type in enumerate(types):
        sg_value = stress_schema[type]['sg']
        pl_value = stress_schema[type]['pl']
        for j, case in enumerate(sg_cases):
            stress_schema[type][case] = sg_value
        # end
        for j, case in enumerate(pl_cases):
            stress_schema[type][case] = pl_value
        # end
    # end

    _.ends(module, func)
    return stress_schema
# end


# return export
