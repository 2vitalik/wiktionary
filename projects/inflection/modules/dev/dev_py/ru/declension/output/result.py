from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from projects.inflection.modules.dev.dev_py.a import syllables


module = 'output.result'  # local


@a.starts(module)
def forward_args(func, out_args, info):
    # local keys, args

    args = info.args
    keys = [
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
        'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
        'voc-sg',  'loc-sg',  'prt-sg',
    ]  # list
    for i, key in enumerate(keys):
        if _.has_value(args, key):
            if args[key] == '-':
                out_args[key] = args[key]
            else:
                out_args[key] = args[key] + '<sup>△</sup>'
            # end
        # end
    # end

    keys = [
        'П', 'Пр', 'Сч',
        'hide-text', 'зачин', 'слоги', 'дореф',
        'скл', 'зализняк', 'зализняк1', 'чередование',
        'pt', 'st', 'затрудн', 'клитика',
        'коммент', 'тип', 'степень',
    ]  # list
    for i, key in enumerate(keys):
        if _.has_value(args, key):
            out_args[key] = args[key]
        # end
    # end

    if _.has_key(out_args, 'слоги'):
        if not _.contains(out_args['слоги'], '%<'):
            out_args['слоги'] = syllables.get_syllables(out_args['слоги'])
        # end
    else:
        out_args['слоги'] = info.word.unstressed  # fixme: может всё-таки stressed?
    # end

    _.ends(module, func)
# end


@a.starts(module)
def finalize(func, info, out_args):  # export
    forward_args(out_args, info)  # fixme: move this to the ending of the main function

    _.ends(module, func)
    return out_args
# end


# return export
