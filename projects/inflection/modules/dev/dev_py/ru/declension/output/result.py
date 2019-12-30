from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from projects.inflection.modules.dev.dev_py.a import syllables


module = 'output.result'  # local


@a.starts(module)
def forward_args(func, i):  # export
    # info: Используется дважды -- при инициализации, и потом в самом конце

    # local keys, args
    o = i.out_args  # local

    args = i.args
    keys = [
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
        'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
        'voc-sg',  'loc-sg',  'prt-sg',
    ]  # list
    for j, key in enumerate(keys):
        if _.has_value(args, key):
            if args[key] == '-':
                o[key] = args[key]
            else:
                o[key] = args[key] + '<sup>△</sup>'
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
    for j, key in enumerate(keys):
        if _.has_value(args, key):
            o[key] = args[key]
        # end
    # end

    if _.has_key(o, 'слоги'):
        if not _.contains(o['слоги'], '%<'):
            o['слоги'] = syllables.get_syllables(o['слоги'])
        # end
    else:
        o['слоги'] = i.word.unstressed  # fixme: может всё-таки stressed?
    # end

    _.ends(module, func)
# end


def has_error(i):  # export
    return i.out_args.error != ''
# end


@a.call(module)
def add_error(i, error):  # export
    o = i.out_args  # local

    if o.error:
        o.error = o.error + '<br/>'
    # end
    o.error = o.error + error
# end


# return export
