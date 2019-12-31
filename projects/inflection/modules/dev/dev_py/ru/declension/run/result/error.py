from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.error'  # local


def has_error(i):  # export
    return i.result.error != ''
# end


@a.call(module)
def add_error(i, error):  # export
    r = i.result  # local

    if r.error:
        r.error = r.error + '<br/>'
    # end
    r.error = r.error + error
# end


# return export
