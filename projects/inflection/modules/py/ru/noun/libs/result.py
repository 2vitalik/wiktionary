from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


# Использование дефисов вместо подчёркивания
def replace_underscore_with_hyphen(forms):
    # local keys, old_key

    keys = [
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
#        'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
#        'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
        'voc-sg',  'loc-sg',  'prt-sg',
        'ins-sg2',  # temp?
    ]  # list
    for i, new_key in enumerate(keys):
        old_key = mw.ustring.gsub(new_key, '-', '_')
        if _.has_key(forms, old_key):
            forms[new_key] = forms[old_key]
        # end
    # end
# end


# Фформирование параметров рода и одушевлённости для подстановки в шаблон
def forward_gender_animacy(forms, data):
    # local genders, animacies

    # Род:
    genders = dict(m='муж', f='жен', n='ср' )  # dict
    if data.common_gender:
        forms['род'] = 'общ'
    elif data.output_gender:
        forms['род'] = genders[data.output_gender]
    else:
        forms['род'] = genders[data.gender]
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
# end


def forward_args(forms, args):
    # local keys

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
    ]  # list
    for i, key in enumerate(keys):
        if _.has_value(args, key):
            forms[key] = args[key]
        # end
    # end

    if _.has_key(args, 'коммент'):
        if not forms['коммент']:
            forms['коммент'] = ''
        # end
        forms['коммент'] = forms['коммент'] + args['коммент']
    # end
# end


def additional_arguments(forms, data):
    # RU (склонение)
    if data.adj:
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
# end


#------------------------------------------------------------------------------


def forward_things(forms, args, data):  # export
    forms['stem_type'] = data.stem_type  # for testcases
    forms['stress_type'] = data.stress_type  # for categories   -- is really used?
    forms['dev'] = dev_prefix

    additional_arguments(forms, data)

    # TODO: Убедиться, что кастомные формы идут как дополнение, а не замена? Или таки замена7 Хм..

    replace_underscore_with_hyphen(forms)
    forward_gender_animacy(forms, data)
    forward_args(forms, args)
# end


def default(data, additional):  # export
    # local forms

    forms = additional
    forms['stem_type'] = data.stem_type  # for testcases
    forward_gender_animacy(forms, data)
    forward_args(forms, data.args)
    if not _.has_key(forms, 'зализняк'):
        forms['зализняк'] = '??'
    # end
    return forms
# end


# return export
