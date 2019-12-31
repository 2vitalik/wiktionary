from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from projects.inflection.modules.dev.dev_py.a import syllables


module = 'run.result.forward'  # local


@a.starts(module)
def forward_args(func, i):  # export
    # INFO: Используется дважды -- при инициализации, и потом в самом конце

    # local keys, args
    r = i.result  # local

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
                r[key] = args[key]
            else:
                r[key] = args[key] + '<sup>△</sup>'
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
            r[key] = args[key]
        # end
    # end

    if _.has_key(r, 'слоги'):
        if not _.contains(r['слоги'], '%<'):
            r['слоги'] = syllables.get_syllables(r['слоги'])
        # end
    else:
        r['слоги'] = i.word.unstressed  # fixme: может всё-таки stressed?
    # end

    _.ends(module, func)
# end


# return export
