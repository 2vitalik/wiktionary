from projects.inflection.modules.dev.py import additional
from projects.inflection.modules.dev.py import mw
from projects.inflection.modules.dev.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


def get_pronoun_stress_schema(stress_type):  # export  # INFO: Вычисление схемы ударения
    _.log_func('stress', 'get_pronoun_stress_schema')

    # TODO: Пока не используется

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = dict(  # dict
        stem = dict(  # dict
            sg = _.equals(stress_type, "a"),
            pl = _.equals(stress_type, "b"),
        ),  # dict
        ending = dict(  # dict
            sg = _.equals(stress_type, "b"),
            pl = _.equals(stress_type, "a"),
        ),  # dict
    )  # dict
    return stress_schema
# end


# return export
