from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from projects.inflection.modules.dev.dev_py.a import syllables


module = 'output.result'  # local


# Использование дефисов вместо подчёркивания
@a.starts(module)
def replace_underscore_with_hyphen(func, out_args):
    # local keys, old_key

    keys = [
        'nom-sg',   'gen-sg',   'dat-sg',   'acc-sg',   'ins-sg',   'prp-sg',
        'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
        'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
        'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
        'nom-pl',   'gen-pl',   'dat-pl',   'acc-pl',   'ins-pl',   'prp-pl',
#        'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
#        'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
        'voc-sg',  'loc-sg',  'prt-sg',
        'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
        'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
        'ins-sg2',  # temp?
        'ins-sg2-f',
    ]  # list
    for i, new_key in enumerate(keys):
        old_key = mw.ustring.gsub(new_key, '-', '_')
        if _.has_key(out_args, old_key):
            out_args[new_key] = out_args[old_key]
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def forward_args(func, out_args, data):
    # local keys, args

    args = data.args
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
        out_args['слоги'] = data.word.unstressed  # fixme: может всё-таки stressed?
    # end

    _.ends(module, func)
# end


@a.starts(module)
def finalize(func, data, out_args):  # export
    replace_underscore_with_hyphen(out_args)  # fixme: this will be redundant soon
    forward_args(out_args, data)  # fixme: move this to the ending of the main function

    _.ends(module, func)
    return out_args
# end


# return export
