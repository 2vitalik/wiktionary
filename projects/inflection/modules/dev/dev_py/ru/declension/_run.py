from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .run import _parts as p
from .run.out import result as r
from .run.out.forms import common as form
from .run.out.forms import noun as noun_forms


module = 'run'  # local


@a.starts(module)
def run_gender(func, i):
    o = i.out_args  # local

    if _.startswith(i.rest_index, '0'):
        # todo: move to special function
        # local keys
        keys = [
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
        ]  # list
        for j, key in enumerate(keys):
            o[key] = i.word.stressed
        # end
        return _.ends(module, func)
    # end

    p.generate_parts(i)
    form.generate_out_args(i)

    _.ends(module, func)
# end


@a.starts(module)
def run_info(func, i):  # todo rename to `run_info`
    if not i.has_index:
        return
    # end

    if i.noun:
        run_gender(i)
    elif i.adj:
        o = i.out_args  # local
        genders = ['m', 'n', 'f', '']  # plural (without gender) should be last one?
        for j, gender in enumerate(genders):
            i_copy = mw.clone(i)  # local
            i_copy.gender = gender
            _.log_value(i_copy.gender, 'info.gender')
            run_gender(i_copy)

            o_copy = i_copy.out_args  # local

            # local cases
            if i_copy.gender != '':
                cases = [
                    'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                    'srt-sg',
                ]  # list
            else:
                cases = [
                    'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
                    'srt-pl',
                    'comparative', 'comparative2'
                ]  # list
            # end

            for c, case in enumerate(cases):
                if i_copy.gender != '':
                    key = case + '-' + i_copy.gender
                else:
                    key = case
                # end
                o[key] = o_copy[case]
            # end
            if i_copy.gender == 'f':
                o['ins-sg2-f'] = o_copy['ins-sg2']
            # end

            if i_copy.gender == 'm':
                o['acc-sg-m-a'] = o['gen-sg-m']
                o['acc-sg-m-n'] = o['nom-sg-m']
            elif i_copy.gender == '':
                o['acc-pl-a'] = o_copy['gen-pl']
                o['acc-pl-n'] = o_copy['nom-pl']
            # end

        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def run(func, info):  # export
    # todo: move this `if` block inside `run_info` and run it recursively :)
    if info.variations:
        _.log_info("Случай с вариациями '//'")
        info_1 = info.variations[0]  # local
        info_2 = info.variations[1]  # local
        # todo: ... = o.output(m.modify(info_1))
        run_info(info_1)
        run_info(info_2)
        info.out_args = form.join_forms(info_1.out_args, info_2.out_args)
        # todo: form.join_variations()
        # todo: check for errors inside variations
    elif info.plus:
        _.log_info("Случай с '+'")
        out_args_plus = []  # list  # local
        for i, sub_info in enumerate(info.plus):
            run_info(sub_info)
            out_args_plus.append(sub_info.out_args)
        # end
        info.out_args = form.plus_forms(out_args_plus)
        # todo: form.plus_out_args()
    else:
        _.log_info('Стандартный случай без вариаций')
        run_info(info)
    # end

    if info.noun:
        noun_forms.special_cases(info)
    # end

    r.forward_args(info)

    _.log_table(info.out_args, "info.out_args")
    _.ends(module, func)
# end


# return export
