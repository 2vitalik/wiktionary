from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.parts.transform.circles.adj'


@a.starts(module)
def apply_adj_specific_1_2(func, i):  # export
    p = i.parts  # local

    if i.calc_sg:
        if not _.endswith(p.stems['srt-sg'], 'нн'):
            # todo: log some error?
            return _.ends(module, func)
        # end
        if _.contains(i.rest_index, ['%(1%)', '①']):
            if i.gender == 'm':
                _.replace(p.stems, 'srt-sg', 'нн$', 'н')
            # end
        # end
    # end

    if _.contains(i.rest_index, ['%(2%)', '②']):
        if i.calc_sg:
            _.replace(p.stems, 'srt-sg', 'нн$', 'н')
        # end
        if i.calc_pl:
            _.replace(p.stems, 'srt-pl', 'нн$', 'н')
        # end
    # end

    _.ends(module, func)
# end


# return export
