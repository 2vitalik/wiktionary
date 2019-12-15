from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'modify.circles.adj'


@a.starts(module)
def apply_adj_specific_1_2(func, stems, gender, rest_index):  # export
    if not _.endswith(stems['srt_sg'], 'нн'):
        # todo: log some error?
        _.ends(module, func)
        return
    # end
    if _.contains(rest_index, ['%(1%)', '①']):
        if gender == 'm':
            _.replace(stems, 'srt_sg', 'нн$', 'н')
        # end
    # end
    if _.contains(rest_index, ['%(2%)', '②']):
        _.replace(stems, 'srt_sg', 'нн$', 'н')
        _.replace(stems, 'srt_pl', 'нн$', 'н')
    # end

    _.ends(module, func)
# end


# return export
