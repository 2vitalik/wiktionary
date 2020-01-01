from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...init.parse import init_stem as init_stem
from ...init.parse import noun as noun_parse
from ...run.result import error as e


module = 'init.parse.angle_brackets'  # local


@a.starts(module)
def angle_brackets(func, i):
    angle_index = _.extract(i.rest_index, '%<([^>]+)%>')  # local
    if angle_index:
        if not i.pt:
            i.output_gender = i.gender
            i.output_animacy = i.animacy
        # end

        i.orig_index = i.index
        i.index = angle_index

        pt_backup = i.pt  # local
        noun_parse.extract_gender_animacy(i)
        i.pt = pt_backup

        if e.has_error(i):
            return _.ends(module, func)
        # end

        _.log_value(i.adj, 'i.adj')
        if i.adj:  # fixme: Для прилагательных надо по-особенному?
            init_stem.init_stem(i)
            if e.has_error(i):
                return _.ends(module, func)
            # end
        # end
    # end

    _.ends(module, func)
# end


# return export
