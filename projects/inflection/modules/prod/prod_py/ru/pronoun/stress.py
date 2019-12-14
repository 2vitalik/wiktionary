from projects.inflection.modules.prod.prod_py import a
from projects.inflection.modules.prod.prod_py import mw
from projects.inflection.modules.prod.prod_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'pronoun.stress'  # local


@a.starts(module)
def get_pronoun_stress_schema(func, stress_type):  # export  # INFO: Вычисление схемы ударения
    # TODO: Пока не используется

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = dict(  # dict
        stem = dict(  # dict
            sg = _.equals(stress_type, "a"),
            pl = _.equals(stress_type, "a"),
        ),  # dict
        ending = dict(  # dict
            sg = _.equals(stress_type, "b"),
            pl = _.equals(stress_type, "b"),
        ),  # dict
    )  # dict

    types = ['stem', 'ending']
    sg_cases = ['nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg']  # list
    pl_cases = ['nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl']  # list
    for i, type in enumerate(types):
        sg_value = stress_schema[type]['sg']
        pl_value = stress_schema[type]['pl']
        for i, case in enumerate(sg_cases):
            stress_schema[type][case] = sg_value
        # end
        for i, case in enumerate(pl_cases):
            stress_schema[type][case] = pl_value
        # end
    # end

    _.ends(module, func)
    return stress_schema
# end


# return export
