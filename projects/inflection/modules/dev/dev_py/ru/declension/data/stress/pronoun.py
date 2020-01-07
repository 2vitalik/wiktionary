from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


import sys, os; sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from data.endings.noun import dump_data
except ImportError:
    from ...data.endings.noun import dump_data


module = 'data.stress.pronoun'  # local


@a.starts(module)
def generate_pronoun_stress_schemas(func):  # INFO: Вычисление схемы ударения
    stress_types = ['a', 'b']  # local
    res = dict()  # dict

    for j, stress_type in enumerate(stress_types):
        stress_schema = dict()  # dict
        stress_schema['stem'] = dict()  # dict
        stress_schema['ending'] = dict()  # dict

        # общий подход следующий:
        # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
        stress_schema['stem']['sg'] = _.equals(stress_type, "a")
        stress_schema['stem']['pl'] = _.equals(stress_type, "a")
        stress_schema['ending']['sg'] = _.equals(stress_type, "b")
        stress_schema['ending']['pl'] = _.equals(stress_type, "b")

        types = ['stem', 'ending']
        sg_cases = ['nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg']  # list
        pl_cases = ['nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl']  # list
        for j, type in enumerate(types):
            sg_value = stress_schema[type]['sg']
            for j, case in enumerate(sg_cases):
                stress_schema[type][case] = sg_value
            # end
            del stress_schema[type]['sg']

            pl_value = stress_schema[type]['pl']
            for j, case in enumerate(pl_cases):
                stress_schema[type][case] = pl_value
            # end
            del stress_schema[type]['pl']
        # end
        res[stress_type] = stress_schema
    # end

    dump_data('pronoun', res)

    return _.returns(module, func, res)
# end


if __name__ == '__main__':
    generate_pronoun_stress_schemas()
