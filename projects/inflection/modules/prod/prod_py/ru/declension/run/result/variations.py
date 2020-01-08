from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.variations'  # local


@a.starts(module)
def join_forms(func, out_args_1, out_args_2):  # export  # todo: rename to `variations`
    # local keys, out_args, delim

    keys = [
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
        'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
        'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
        'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
        'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
        'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
        'ins-sg2',
        'ins-sg2-f',
        'зализняк1', 'зализняк',
        'error',
    ]  # list

    out_args = out_args_1
    out_args['зализняк-1'] = out_args_1['зализняк']
    out_args['зализняк-2'] = out_args_2['зализняк']
    for j, key in enumerate(keys):
        if not _.has_key(out_args, key) and not _.has_key(out_args_2, key):
            pass
        elif not _.has_key(out_args, key) and _.has_key(out_args_2, key):  # INFO: Если out_args[key] == None
            out_args[key] = out_args_2[key]
        elif out_args[key] != out_args_2[key] and out_args_2[key]:
            delim = '<br/>'
            if _.equals(key, ['зализняк1', 'зализняк']):
                delim = '&nbsp;'
            # end
            # TODO: <br/> только для падежей
            out_args[key] = out_args[key] + '&nbsp;//' + delim + out_args_2[key]
        # end
        if not _.has_key(out_args, key) or not out_args[key]:  # INFO: Если out_args[key] == None
            out_args[key] = ''
        # end
    # end

    return _.returns(module, func, out_args)
# end


@a.starts(module)
def plus_forms(func, sub_forms):  # export  # todo: rename to `out_args`
    # local keys, out_args, delim

    keys = [
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
        'ins-sg2',
        'зализняк1', 'зализняк',
        'error',
    ]  # list
    out_args = sub_forms[0]  # todo: rename to `out_args`
    for j, forms2 in enumerate(sub_forms):  # todo: rename to `out_args`
        if j != 0:
            for j, key in enumerate(keys):
                if not out_args[key] and forms2[key]:  # INFO: Если out_args[key] == None
                    out_args[key] = forms2[key]
                elif out_args[key] != forms2[key] and forms2[key]:
                    delim = '-'
                    if _.equals(key, ['зализняк1', 'зализняк']):
                        delim = ' + '
                    # end
                    out_args[key] = out_args[key] + delim + forms2[key]
                # end
                if not out_args[key]:  # INFO: Если out_args[key] == None
                    out_args[key] = ''
                # end
            # end
        # end
    # end

    return _.returns(module, func, out_args)
# end


# return export
