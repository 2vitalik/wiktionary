from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'data.stress.noun'  # local


# Данные: ударность основы и окончания в зависимости от схемы ударения
@a.starts(module)
def get_noun_stress_schema(func, stress_type):  # export  # INFO: Вычисление схемы ударения
    # local stress_schema, types, sg_value, pl_value

    # todo: Сгенерировать все `stress_schema` для всех видов `stress_type` заранее и потом просто использовать/загружать их

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    stress_schema = a.AttrDict()  # AttrDict  # local
    stress_schema.stem = dict()  # dict
    stress_schema.ending = dict()  # dict
    stress_schema.stem['sg']     = _.equals(stress_type, ["a", "c", "e"])
    stress_schema.stem['acc-sg'] = _.equals(stress_type, ["a", "c", "e", "d'", "f'"])
    stress_schema.stem['ins-sg'] = _.equals(stress_type, ["a", "c", "e", "b'", "f''"])
    stress_schema.stem['pl']     = _.equals(stress_type, ["a", "d", "d'"])
    stress_schema.stem['nom-pl'] = _.equals(stress_type, ["a", "d", "d'", "e", "f", "f'", "f''"])
    stress_schema.ending['sg']     = _.equals(stress_type, ["b", "b'", "d", "d'", "f", "f'", "f''"])
    stress_schema.ending['acc-sg'] = _.equals(stress_type, ["b", "b'", "d", "f", "f''"])
    stress_schema.ending['ins-sg'] = _.equals(stress_type, ["b", "d", "d'", "f", "f'"])
    stress_schema.ending['pl']     = _.equals(stress_type, ["b", "b'", "c", "e", "f", "f'", "f''"])
    stress_schema.ending['nom-pl'] = _.equals(stress_type, ["b", "b'", "c"])

    types = ['stem', 'ending']
    for j, type in enumerate(types):
        sg_value = stress_schema[type]['sg']
        stress_schema[type]['nom-sg'] = sg_value
        stress_schema[type]['gen-sg'] = sg_value
        stress_schema[type]['dat-sg'] = sg_value
        stress_schema[type]['prp-sg'] = sg_value

        pl_value = stress_schema[type]['pl']
        stress_schema[type]['gen-pl'] = pl_value
        stress_schema[type]['dat-pl'] = pl_value
        stress_schema[type]['ins-pl'] = pl_value
        stress_schema[type]['prp-pl'] = pl_value
    # end

    return _.returns(module, func, stress_schema)
# end


# return export
