from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'data.stress.adj'  # local


# Данные: ударность основы и окончания в зависимости от схемы ударения
@a.starts(module)
def get_adj_stress_schema(func, stress_type):  # export  # INFO: Вычисление схемы ударения
    # local stress_schema, types, cases, sg_value

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = dict(  # dict
        stem = dict(  # dict
            full = _.startswith(stress_type, ["a", "a/"]),
            srt_sg_m = True,
            srt_sg_f = _.endswith(stress_type, ["/a", "/a'"]) or _.equals(stress_type, ['a', "a'"]),
            srt_sg_n = _.endswith(stress_type, ["/a", "/c", "/a'", "/c'", "/c''"]) or _.equals(stress_type, ['a', "a'"]),
            srt_pl = _.endswith(stress_type, ["/a", "/c", "/a'", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['a', "a'", "b'"]),
        ),  # dict
        ending = dict(  # dict
            full = _.startswith(stress_type, ["b", "b/"]),
            srt_sg_m = False,
            srt_sg_f = _.endswith(stress_type, ["/b", "/c", "/a'", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['b', "a'", "b'"]),
            srt_sg_n = _.endswith(stress_type, ["/b", "/b'", "/c''"]) or _.equals(stress_type, ['b', "b'"]),
            srt_pl = _.endswith(stress_type, ["/b", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['b', "b'"]),
        ),  # dict
    )  # dict

    types = ['stem', 'ending']
    cases = [
        'sg', 'pl',
        'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
        'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
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
