from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


import sys, os; sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from data.endings.noun import dump_data
except ImportError:
    from ...data.endings.noun import dump_data


module = 'data.stress.noun'  # local  # todo: rename to `stress_schemas`


# Данные: ударность основы и окончания в зависимости от схемы ударения
@a.starts(module)
def generate_noun_stress_schemas(func):  # INFO: Вычисление схемы ударения
    # todo: special variable for this?
    stress_types = ['a', 'b', 'c', 'd', 'e', 'f', "d'", "f'", "f''"]  # local
    res = dict()  # dict

    for j, stress_type in enumerate(stress_types):
        stress_schema = dict()  # dict
        stress_schema['stem'] = dict()  # dict
        stress_schema['ending'] = dict()  # dict

        # общий подход следующий:
        # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
        stress_schema['stem']['sg']     = _.equals(stress_type, ["a", "c", "e"])
        stress_schema['stem']['nom-sg'] = '...'
        stress_schema['stem']['gen-sg'] = '...'
        stress_schema['stem']['dat-sg'] = '...'
        stress_schema['stem']['acc-sg'] = _.equals(stress_type, ["a", "c", "e", "d'", "f'"])
        stress_schema['stem']['ins-sg'] = _.equals(stress_type, ["a", "c", "e", "b'", "f''"])
        stress_schema['stem']['prp-sg'] = '...'
        stress_schema['stem']['pl']     = _.equals(stress_type, ["a", "d", "d'"])
        stress_schema['stem']['nom-pl'] = _.equals(stress_type, ["a", "d", "d'", "e", "f", "f'", "f''"])
        stress_schema['stem']['gen-pl'] = '...'
        stress_schema['stem']['dat-pl'] = '...'
        stress_schema['stem']['ins-pl'] = '...'
        stress_schema['stem']['prp-pl'] = '...'
        stress_schema['ending']['sg']     = _.equals(stress_type, ["b", "b'", "d", "d'", "f", "f'", "f''"])
        stress_schema['ending']['nom-sg'] = '...'
        stress_schema['ending']['gen-sg'] = '...'
        stress_schema['ending']['dat-sg'] = '...'
        stress_schema['ending']['acc-sg'] = _.equals(stress_type, ["b", "b'", "d", "f", "f''"])
        stress_schema['ending']['ins-sg'] = _.equals(stress_type, ["b", "d", "d'", "f", "f'"])
        stress_schema['ending']['prp-sg'] = '...'
        stress_schema['ending']['pl']     = _.equals(stress_type, ["b", "b'", "c", "e", "f", "f'", "f''"])
        stress_schema['ending']['nom-pl'] = _.equals(stress_type, ["b", "b'", "c"])
        stress_schema['ending']['gen-pl'] = '...'
        stress_schema['ending']['dat-pl'] = '...'
        stress_schema['ending']['ins-pl'] = '...'
        stress_schema['ending']['prp-pl'] = '...'

        types = ['stem', 'ending']  # local
        for j, type in enumerate(types):
            sg_value = stress_schema[type]['sg']  # local
            stress_schema[type]['nom-sg'] = sg_value
            stress_schema[type]['gen-sg'] = sg_value
            stress_schema[type]['dat-sg'] = sg_value
            stress_schema[type]['prp-sg'] = sg_value
            del stress_schema[type]['sg']

            pl_value = stress_schema[type]['pl']  # local
            stress_schema[type]['gen-pl'] = pl_value
            stress_schema[type]['dat-pl'] = pl_value
            stress_schema[type]['ins-pl'] = pl_value
            stress_schema[type]['prp-pl'] = pl_value
            del stress_schema[type]['pl']
        # end

        res[stress_type] = stress_schema
    # end

    dump_data('noun', res)

    return _.returns(module, func, res)
# end


if __name__ == '__main__':
    generate_noun_stress_schemas()
