from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


# Данные: ударность основы и окончания в зависимости от схемы ударения
def get_adj_stress_schema(stress_type):  # export  # INFO: Вычисление схемы ударения
    _.log_func('stress', 'get_adj_stress_schema')

    # local stress_schema, types, cases, sg_value

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = dict(  # dict
        stem = dict(  # dict
            full = _.startswith(stress_type, ["a", "a/"]),
            srt_sg_f = _.endswith(stress_type, ["/a", "/a'"]),
            srt_sg_n = _.endswith(stress_type, ["/a", "/c", "/a'", "/c'", "/c''"]),
            srt_pl = _.endswith(stress_type, ["/a", "/c", "/a'", "/b'", "/c'", "/c''"]),
        ),  # dict
        ending = dict(  # dict
            full = _.startswith(stress_type, ["b", "b/"]),
            srt_sg_f = _.endswith(stress_type, ["/b", "/c", "/a'", "/b'", "/c'", "/c''"]),
            srt_sg_n = _.endswith(stress_type, ["/b", "/b'", "/c''"]),
            srt_pl = _.endswith(stress_type, ["/b", "/b'", "/c'", "/c''"]),
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

    return stress_schema
# end


# return export
