from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..run.result.forms import init as init_forms
from ..run.result.forms import common as common_forms
from ..run.result.forms import noun as noun_forms
from ..run.result.forms import adj as adj_forms


module = 'run.result'  # local


@a.starts(module)
def generate_result(func, i):  # export
    r = i.result  # local

    init_forms.init_forms(i)
    if i.adj:
        init_forms.init_srt_forms(i)
    # end

    common_forms.fix_stress(r)

    if i.adj:
        adj_forms.add_comparative(i)
    # end

    for key, value in r.items():
        # replace 'ё' with 'е' when unstressed
        # if _.contains_once(i.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё'):  -- trying to bug-fix
        if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё'):
            if i.adj and _.contains(i.stress_type, "a'") and i.gender == 'f' and key == 'srt-sg':
                r[key] = _.replaced(value, 'ё', 'е') + ' // ' + _.replaced(value, '́', '')
            else:
                r[key] = _.replaced(value, 'ё', 'е')  # обычный случай
            # end
        # end
    # end

    if i.noun:
        noun_forms.apply_obelus(i)
    # end

    common_forms.choose_accusative_forms(i)

    common_forms.second_ins_case(i)

    if i.noun:
        noun_forms.apply_specific_3(i)
    # end

    for key, value in r.items():
#        INFO Удаляем ударение, если только один слог:
        r[key] = noun_forms.remove_stress_if_one_syllable(value)
    # end

    if i.adj:
        if i.postfix:
            # local keys
            keys = [
                'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
            ]  # list
            for j, key in enumerate(keys):
                r[key] = r[key] + 'ся'
            # end
        # end
    # end

    _.ends(module, func)
# end


# return export
