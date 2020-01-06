from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .run import _parts as p
from .run import _result as res
from .run.result import forward as forward
from .run.result import variations as v
from .run.result.forms import noun as noun_forms


module = 'run'  # local


@a.starts(module)
def run_gender(func, i):
    r = i.result  # local

    if _.startswith(i.rest_index, '0'):
        # todo: move to special function
        # local keys
        keys = [  # todo: depend on `calc_sg` and `calc_pl`
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
        ]  # list
        for j, key in enumerate(keys):
            r[key] = i.word.stressed
        # end
        return _.ends(module, func)
    # end

    p.generate_parts(i)
    res.generate_result(i)

    _.ends(module, func)
# end


@a.starts(module)
def run_info(func, i):
    if not i.has_index:
        return
    # end

    if i.noun:
        run_gender(i)
    elif i.adj:
        r = i.result  # local
        orig = mw.clone(i)
        genders = ['m', 'n', 'f', 'pl']  # plural (without gender) should be last one?
        for j, gender in enumerate(genders):
            ii = mw.clone(orig)  # local
            ii.gender = gender
            _.log_value(ii.gender, 'i.gender')

            if ii.gender != 'pl':
                ii.calc_sg = True
                _.log_value(ii.calc_sg, 'i.calc_sg')
            else:
                ii.calc_pl = True
                _.log_value(ii.calc_pl, 'i.calc_pl')
            # end

            run_gender(ii)
            r_copy = ii.result  # local

            # local cases
            if ii.gender != 'pl':
                cases = [
                    'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                    'srt-sg',
                ]  # list

                for c, case in enumerate(cases):
                    r[case + '-' + ii.gender] = r_copy[case]
                # end

                if ii.gender == 'f':
                    r['ins-sg2-f'] = r_copy['ins-sg2']
                # end
                if ii.gender == 'm':
                    r['acc-sg-m-a'] = r['gen-sg-m']
                    r['acc-sg-m-n'] = r['nom-sg-m']
                # end
            else:
                cases = [
                    'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
                    'srt-pl',
                    'comparative', 'comparative2'
                ]  # list

                for c, case in enumerate(cases):
                    r[case] = r_copy[case]
                # end

                r['acc-pl-a'] = r_copy['gen-pl']
                r['acc-pl-n'] = r_copy['nom-pl']
            # end
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def run(func, i):  # export
    # todo: move this `if` block inside `run_info` and run it recursively? :)
    if i.variations:
        _.log_info("Случай с вариациями '//'")
        i1 = i.variations[0]  # local
        i2 = i.variations[1]  # local
        run_info(i1)
        run_info(i2)
        i.result = v.join_forms(i1.result, i2.result)
        # todo: form.join_variations()
        # todo: check for errors inside variations
    elif i.plus:
        _.log_info("Случай с '+'")
        plus = []  # list  # local
        for j, sub_info in enumerate(i.plus):
            run_info(sub_info)
            plus.append(sub_info.result)
        # end
        i.result = v.plus_forms(plus)
        # todo: form.plus_out_args()
    else:
        _.log_info('Стандартный случай без вариаций')
        run_info(i)
    # end

    if i.noun:
        noun_forms.special_cases(i)  # todo: move to `run/result/generate_result`
    # end

    forward.forward_args(i)

    _.log_table(i.result, "i.result")
    _.ends(module, func)
# end


# return export
