from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..init.process import stem_type as stem_type
from ..init.process import stress as stress
from ..output import init_out_args as o
from ..output import result as r


module = 'init.process'  # local


@a.starts(module)
def process(func, i):  # export
    _.log_info('Извлечение информации об ударении (stress_type)')
    stress.extract_stress_type(i)  # todo: move to `parse`
    _.log_value(i.stress_type, 'info.stress_type')

    if r.has_error(i):
        _.ends(module, func)
        return i
    # end

    _.log_info('Вычисление схемы ударения')
    stress.get_stress_schema(i)
    _.log_table(i.stress_schema['stem'], "info.stress_schema['stem']")
    _.log_table(i.stress_schema['ending'], "info.stress_schema['ending']")

    _.log_info('Определение типа основы (stem_type)')
    stem_type.get_stem_type(i)
    _.log_value(i.stem.type, 'info.stem.type')
    _.log_value(i.stem.base_type, 'info.stem.base_type')

    _.log_info('Инициализируем `info.out_args`')
    o.init_out_args(i)

    _.ends(module, func)
    return i
# end


# return export
