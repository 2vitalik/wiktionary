from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .modify import _prepare
from .modify import _transform


module = 'modify'  # local


@a.starts(module)
def modify(func, i):  # export                                                #
    _prepare.prepare(i)                                                       #
    _transform.transform(i)                                                   #
                                                                              #
    _.ends(module, func)                                                      #
# end                                                                         #


# return export
