from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


import sys, os; sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
try:
    # чтобы запускать скрипт и импорт работал:
    from data.endings.generators.noun import dump_data
except ImportError:
    # для IDE, чтобы она находила методы:
    from ....data.endings.generators.noun import dump_data


module = 'data.stress.adj'  # local


# Данные: ударность основы и окончания в зависимости от схемы ударения
@a.starts(module)
def generate_adj_stress_schemas(func):  # INFO: Вычисление схемы ударения
    stress_types = [  # todo: special variables for that?
        'a', "a'", 'b', "b'", 'c',
        'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
        'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
    ]
    res = dict()  # dict

    for j, stress_type in enumerate(stress_types):
        stress_schema = dict()  # dict
        stress_schema['stem'] = dict()  # dict
        stress_schema['ending'] = dict()  # dict

        # local cases
        cases = [
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
        ]  # list

        # пустышки в падежи, чтобы они шли раньше кратких форм в результате
        types = ['stem', 'ending']  # local
        for j, type in enumerate(types):
            for j, case in enumerate(cases):
                stress_schema[type][case] = '...'
            # end
        # end

        # общий подход следующий:
        # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
        stress_schema['stem']['full'] = _.startswith(stress_type, ["a", "a/"])
        stress_schema['stem']['srt-sg-m'] = True
        stress_schema['stem']['srt-sg-f'] = _.endswith(stress_type, ["/a", "/a'"]) or _.equals(stress_type, ['a', "a'"])
        stress_schema['stem']['srt-sg-n'] = _.endswith(stress_type, ["/a", "/c", "/a'", "/c'", "/c''"]) or _.equals(stress_type, ['a', "a'"])
        stress_schema['stem']['srt-pl'] = _.endswith(stress_type, ["/a", "/c", "/a'", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['a', "a'", "b'"])
        stress_schema['ending']['full'] = _.startswith(stress_type, ["b", "b/"])
        stress_schema['ending']['srt-sg-m'] = False
        stress_schema['ending']['srt-sg-f'] = _.endswith(stress_type, ["/b", "/c", "/a'", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['b', "a'", "b'"])
        stress_schema['ending']['srt-sg-n'] = _.endswith(stress_type, ["/b", "/b'", "/c''"]) or _.equals(stress_type, ['b', "b'"])
        stress_schema['ending']['srt-pl'] = _.endswith(stress_type, ["/b", "/b'", "/c'", "/c''"]) or _.equals(stress_type, ['b', "b'"])

        types = ['stem', 'ending']  # local
        for j, type in enumerate(types):
            value = stress_schema[type]['full']  # local
            for j, case in enumerate(cases):
                stress_schema[type][case] = value
            # end
            del stress_schema[type]['full']
        # end
        res[stress_type] = stress_schema
    # end

    dump_data('adj', res)

    return _.returns(module, func, res)
# end


if __name__ == '__main__':
    generate_adj_stress_schemas()
