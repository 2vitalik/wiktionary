from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .run import _parts as p
from .run.result import forward as forward
from .run.result.forms import common as form
from .run.result.forms import noun as noun_forms


module = 'run'  # local


@a.starts(module)
def run_gender(func, i):
    r = i.result  # local

    if _.startswith(i.rest_index, '0'):
        # todo: move to special function
        # local keys
        keys = [
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
        ]  # list
        for j, key in enumerate(keys):
            r[key] = i.word.stressed
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
        r = i.result  # local
        genders = ['m', 'n', 'f', '']  # plural (without gender) should be last one?
        for j, gender in enumerate(genders):
            i_copy = mw.clone(i)  # local
            i_copy.gender = gender
            _.log_value(i_copy.gender, 'i.gender')
            run_gender(i_copy)

            r_copy = i_copy.result  # local

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
                r[key] = r_copy[case]
            # end
            if i_copy.gender == 'f':
                r['ins-sg2-f'] = r_copy['ins-sg2']
            # end

            if i_copy.gender == 'm':
                r['acc-sg-m-a'] = r['gen-sg-m']
                r['acc-sg-m-n'] = r['nom-sg-m']
            elif i_copy.gender == '':
                r['acc-pl-a'] = r_copy['gen-pl']
                r['acc-pl-n'] = r_copy['nom-pl']
            # end

        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def run(func, i):  # export
    # todo: move this `if` block inside `run_info` and run it recursively :)
    if i.variations:
        _.log_info("Случай с вариациями '//'")
        i1 = i.variations[0]  # local
        i2 = i.variations[1]  # local
        # todo: ... = o.output(m.modify(info_1))
        run_info(i1)
        run_info(i2)
        i.result = form.join_forms(i1.result, i2.result)
        # todo: form.join_variations()
        # todo: check for errors inside variations
    elif i.plus:
        _.log_info("Случай с '+'")
        out_args_plus = []  # list  # local
        for j, sub_info in enumerate(i.plus):
            run_info(sub_info)
            out_args_plus.append(sub_info.result)
        # end
        i.result = form.plus_forms(out_args_plus)
        # todo: form.plus_out_args()
    else:
        _.log_info('Стандартный случай без вариаций')
        run_info(i)
    # end

    if i.noun:
        noun_forms.special_cases(i)
    # end

    forward.forward_args(i)

    _.log_table(i.result, "i.result")
    _.ends(module, func)
# end


# return export
