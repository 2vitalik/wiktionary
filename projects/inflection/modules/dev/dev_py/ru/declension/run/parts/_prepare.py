from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.parts.prepare import endings as endings
from ...run.parts.prepare import stress_apply as stress_apply


module = 'modify.prepare'  # local


@a.starts(module)
def prepare(func, i):  # export
    # INFO: Generates `.endings` and `.stems`

    # todo: logging info
    endings.get_endings(i)

    # todo: logging info
    i.data.stems = dict()  # dict
    stress_apply.apply_stress_type(i)
    _.log_table(i.data.stems, 'info.data.stems')
    _.log_table(i.data.endings, 'info.data.endings')

    _.ends(module, func)
# end


# return export
