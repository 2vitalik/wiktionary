from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'output.forms.adj'


@a.starts(module)
def add_comparative(func, out_args, rest_index, stress_type, stem_type, stem):  # export
    # todo: move to `modify` (и сделать через основы и окончания)

    if _.contains(rest_index, '~'):
        out_args['comparative'] = '-'
        return _.ends(module, func)
    # end

    if stem_type == 'velar':
        new_stem = stem.unstressed
        if _.endswith(new_stem, 'к'):
            new_stem = _.replaced(new_stem, 'к$', 'ч')
        elif _.endswith(new_stem, 'г'):
            new_stem = _.replaced(new_stem, 'г$', 'ж')
        elif _.endswith(new_stem, 'х'):
            new_stem = _.replaced(new_stem, 'х$', 'ш')
        else:
            pass  # todo: some error here
        # end

        # ударение на предпоследний слог:
        new_stem = _.replaced(new_stem, '({vowel})({consonant}*)$', '%1́ %2')

        out_args['comparative'] = new_stem + 'е'
    else:
        if stress_type == 'a' or _.startswith(stress_type, 'a/'):
            out_args['comparative'] = stem.stressed + 'ее'
            out_args['comparative2'] = stem.stressed + 'ей'
        else:
            out_args['comparative'] = stem.unstressed + 'е́е'
            out_args['comparative2'] = stem.unstressed + 'е́й'
        # end
    # end
# end


# return export
