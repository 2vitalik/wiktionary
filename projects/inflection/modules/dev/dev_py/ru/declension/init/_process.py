from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..init.process import stem_type as stem_type
from ..init.process import stress as stress
from ..run.result import init_out_args as o
from ..run.result import error as e


module = 'init.process'  # local


@a.starts(module)
def process(func, i):  # export
    _.log_info('Извлечение информации об ударении (stress_type)')
    stress.extract_stress_type(i)  # todo: move to `parse`
    _.log_value(i.stress_type, 'i.stress_type')

    if e.has_error(i):
        _.ends(module, func)
        return i
    # end

    if not i.stress_type:  # если ударение не указано
        if _.contains(i.rest_index, '0'):  # если несклоняемая схема
            i.stress_type = ''
        else:
            # INFO: Если при этом есть какой-то индекс, это явно ОШИБКА
            if _.has_value(i.rest_index):
                e.add_error(i, 'Нераспознанная часть индекса: ' + i.rest_index)
                _.ends(module, func)
                return i
            # end

            # INFO: Если же индекса вообще нет, то и формы просто не известны:
            i.has_index = False
            _.ends(module, func)
            return i
        # end
    # end

    _.log_info('Вычисление схемы ударения')
    stress.get_stress_schema(i)
    _.log_table(i.stress_schema['stem'], "i.stress_schema['stem']")
    _.log_table(i.stress_schema['ending'], "i.stress_schema['ending']")

    _.log_info('Определение типа основы (stem_type)')
    stem_type.get_stem_type(i)
    _.log_value(i.stem.type, 'i.stem.type')
    _.log_value(i.stem.base_type, 'i.stem.base_type')

    # INFO: Итак, ударение мы получили.

    # INFO: Добавление ударения для `stem.stressed` (если его не было)
    # INFO: Например, в слове только один слог, или ударение было на окончание
    if not _.contains(i.stem.stressed, '[́ ё]'):  # and not i.absent_stress ??
        if _.equals(i.stress_type, ["f", "f'"]):
            i.stem.stressed = _.replaced(i.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
        elif _.contains(i.rest_index, '%*'):
            pass  # *** поставим ударение позже, после чередования
        else:
            i.stem.stressed = _.replaced(i.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
        # end
    # end

    _.log_value(i.stem.stressed, 'i.stem.stressed')

    _.log_info('Инициализируем `i.result`')
    o.init_out_args(i)

    _.ends(module, func)
    return i
# end


# return export
