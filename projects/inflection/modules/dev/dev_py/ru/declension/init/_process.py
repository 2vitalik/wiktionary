from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .process import stem_type, stress


module = 'init.process'  # local


@a.starts(module)
def process(func, info):  # export
    _.log_info('Извлечение информации об ударении (stress_type)')
    info.stress_type, error = stress.extract_stress_type(info.rest_index)
    _.log_value(info.stress_type, 'info.stress_type')

    if error:
        # out_args = result.finalize(data, error)
        # todo: save error somewhere in `info`
        _.ends(module, func)
        return info
        # return out_args
    # end

    _.log_info('Вычисление схемы ударения')
    info.stress_schema = stress.get_stress_schema(info.stress_type, info.adj,
                                                  info.pronoun)
    _.log_table(info.stress_schema['stem'], "info.stress_schema['stem']")
    _.log_table(info.stress_schema['ending'], "info.stress_schema['ending']")

    _.log_info('Определение типа основы (stem_type)')
    info.stem.type, info.stem.base_type = stem_type.get_stem_type(info.stem.unstressed, info.word.unstressed, info.gender, info.adj, info.rest_index)
    _.log_value(info.stem.type, 'info.stem.type')
    _.log_value(info.stem.base_type, 'info.stem.base_type')

    _.ends(module, func)
    return info
# end


# return export
