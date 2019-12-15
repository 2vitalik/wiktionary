from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from projects.inflection.modules.dev.dev_py.a import syllables


module = 'output.result'  # local


# Использование дефисов вместо подчёркивания
@a.starts(module)
def replace_underscore_with_hyphen(func, forms):
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
        if _.has_key(forms, old_key):
            forms[new_key] = forms[old_key]
        # end
    # end

    _.ends(module, func)
# end


# Формирование параметров рода и одушевлённости для подстановки в шаблон
@a.starts(module)
def forward_gender_animacy(func, forms, data):
    # local genders, animacies

    # Род:
    genders = dict(m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж' )  # dict
    if data.common_gender:
        forms['род'] = 'общ'
    elif data.output_gender:
        forms['род'] = genders[data.output_gender]
    elif data.gender:
        forms['род'] = genders[data.gender]
    else:
        pass
    # end

    # Одушевлённость:
    animacies = dict()  # dict
    animacies['in'] = 'неодуш'
    animacies['an'] = 'одуш'
    animacies['in//an'] = 'неодуш-одуш'
    animacies['an//in'] = 'одуш-неодуш'
    if data.output_animacy:
        forms['кат'] = animacies[data.output_animacy]
    else:
        forms['кат'] = animacies[data.animacy]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def forward_args(func, forms, data):
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
                forms[key] = args[key]
            else:
                forms[key] = args[key] + '<sup>△</sup>'
            # end
        # end
    # end

    keys = [
        'П', 'Пр', 'Сч',
        'hide-text', 'зачин', 'слоги', 'дореф',
        'скл', 'зализняк', 'зализняк1', 'чередование',
        'pt', 'st', 'затрудн', 'клитика',
        'коммент',
    ]  # list
    for i, key in enumerate(keys):
        if _.has_value(args, key):
            forms[key] = args[key]
        # end
    # end

    if _.has_key(forms, 'слоги'):
        if not _.contains(forms['слоги'], '%<'):
            forms['слоги'] = syllables.get_syllables(forms['слоги'])
        # end
    else:
        forms['слоги'] = data.word
    # end

    _.ends(module, func)
# end


@a.starts(module)
def additional_arguments(func, forms, data):
    # RU (склонение)
    if _.contains(data.rest_index, '0'):
        forms['скл'] = 'не'
    elif data.adj:
        forms['скл'] = 'а'
    elif data.pronoun:
        forms['скл'] = 'мс'
    elif _.endswith(data.word, '[ая]'):
        forms['скл'] = '1'
    else:
        if data.gender == 'm' or data.gender == 'n':
            forms['скл'] = '2'
        else:
            forms['скл'] = '3'
        # end
    # end

    # RU (чередование)
    if _.contains(data.index, '%*'):
        forms['чередование'] = '1'
    # end

    if data.pt:
        forms['pt'] = '1'
    # end

    # RU ("-" в индексе)
    # TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
    if data.rest_index:
        if _.contains(data.rest_index, ['%-', '—', '−']):
            forms['st'] = '1'
            forms['затрудн'] = '1'
        # end
    else:
        pass  # TODO
    # end

    _.ends(module, func)
# end


#------------------------------------------------------------------------------


@a.starts(module)
def finalize(func, data, forms):  # export
    forms['stem_type'] = data.stem_type  # for testcases
    forms['stress_type'] = data.stress_type  # for categories   -- is really used?
    forms['dev'] = dev_prefix

    additional_arguments(forms, data)
    replace_underscore_with_hyphen(forms)

    if data.noun:
        forward_gender_animacy(forms, data)
    # end

    forward_args(forms, data)

    if not _.has_key(forms, 'зализняк'):
        forms['зализняк'] = '??'
    # end

    if not _.has_key(forms, 'error_category') and data.word_cleared != data.base:
        forms['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
    # end

    _.ends(module, func)
    return forms
# end


# return export
