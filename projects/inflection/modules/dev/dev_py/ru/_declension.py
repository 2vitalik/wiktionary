from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .declension import _init as init
from .declension.run.result import error as e
from .declension import _run as run


module = 'declension'  # local


@a.starts(module)
def forms(func, base, args, frame):  # export  # todo: rename to `out_args`
    i = init.init_info(base, args, frame)  # local
    if e.has_error(i):
        return _.returns(module, func, i.result)
    # end

    # INFO: Запуск основного алгоритма и получение результирующих словоформ:
    run.run(i)

    return _.returns(module, func, i.result)
# end


# return export
