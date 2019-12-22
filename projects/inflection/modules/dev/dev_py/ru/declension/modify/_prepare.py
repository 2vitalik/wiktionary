from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..modify.prepare import endings as endings
from ..modify.prepare import stress_apply as stress_apply


module = 'modify.prepare'  # local


@a.starts(module)
def prepare(func, info):  # export
    # INFO: Generates `.endings` and `.stems`

    # todo: create info.data.* !!!

    # todo: logging info
    info.data.endings = endings.get_endings(info)

    # todo: logging info
    info.data.stems = dict()  # dict
    stress_apply.apply_stress_type(info)
    _.log_table(info.data.stems, 'info.data.stems')
    _.log_table(info.data.endings, 'info.data.endings')

    _.ends(module, func)
# end


# return export
