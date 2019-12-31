from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.parts.prepare import endings as endings
from ...run.parts.prepare import stress_apply as stress_apply


module = 'run.parts.prepare'  # local


@a.starts(module)
def prepare(func, i):  # export
    # INFO: Generates `.endings` and `.stems`

    # todo: logging info
    endings.get_endings(i)

    # todo: logging info
    i.parts.stems = dict()  # dict
    stress_apply.apply_stress_type(i)
    _.log_table(i.parts.stems, 'info.parts.stems')
    _.log_table(i.parts.endings, 'info.parts.endings')

    _.ends(module, func)
# end


# return export
