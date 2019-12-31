from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.out.forms.adj'


@a.starts(module)
def add_comparative(func, i):  # export
    # todo: move to `modify` (и сделать через основы и окончания)
    o = i.out_args  # local

    if _.contains(i.rest_index, '~'):
        o['comparative'] = '-'
        return _.ends(module, func)
    # end

    if i.stem.type == 'velar':
        new_stem = i.stem.unstressed
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

        o['comparative'] = new_stem + 'е'
    else:
        if _.equals(i.stress_type, ['a', 'a/a']):
            o['comparative'] = i.stem.stressed + 'ее'
            o['comparative2'] = i.stem.stressed + 'ей'
        else:
            o['comparative'] = i.stem.unstressed + 'е́е'
            o['comparative2'] = i.stem.unstressed + 'е́й'
        # end
    # end

    _.ends(module, func)
# end


# return export
