from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'output.init_out_args'  # local


# Формирование параметров рода и одушевлённости для подстановки в шаблон
@a.starts(module)
def forward_gender_animacy(func, i):
    o = i.out_args  # local

    # Род:
    genders = dict(m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж')  # dict  # local

    if i.common_gender:
        o['род'] = 'общ'
    elif i.output_gender:
        o['род'] = genders[i.output_gender]
    elif i.gender:
        o['род'] = genders[i.gender]
    else:
        pass
    # end

    # Одушевлённость:
    animacies = dict()  # dict  # local
    animacies['in'] = 'неодуш'
    animacies['an'] = 'одуш'
    animacies['in//an'] = 'неодуш-одуш'
    animacies['an//in'] = 'одуш-неодуш'

    if i.output_animacy:
        o['кат'] = animacies[i.output_animacy]
    else:
        o['кат'] = animacies[i.animacy]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def additional_arguments(func, i):
    o = i.out_args  # local

    # RU (склонение)
    if _.contains(i.rest_index, '0'):
        o['скл'] = 'не'
    elif i.adj:
        o['скл'] = 'а'
    elif i.pronoun:
        o['скл'] = 'мс'
    elif _.endswith(i.word.unstressed, '[ая]'):
        o['скл'] = '1'
    else:
        if i.gender == 'm' or i.gender == 'n':
            o['скл'] = '2'
        else:
            o['скл'] = '3'
        # end
    # end

    # RU (чередование)
    if _.contains(i.index, '%*'):
        o['чередование'] = '1'
    # end

    if i.pt:
        o['pt'] = '1'
    # end

    # RU ("-" в индексе)
    # TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
    if i.rest_index:
        if _.contains(i.rest_index, ['%-', '—', '−']):
            o['st'] = '1'
            o['затрудн'] = '1'
        # end
    else:
        pass  # TODO
    # end

    _.ends(module, func)
# end


@a.starts(module)
def init_out_args(func, i):
    o = i.out_args  # local

    o['stem_type'] = i.stem.type  # for testcases
    o['stress_type'] = i.stress_type  # for categories   -- is really used?

    o['dev'] = dev_prefix
    o['зализняк'] = '??'  # значение по умолчанию

    additional_arguments(i)

    if i.noun:
        forward_gender_animacy(i)
    # end

    if not _.has_key(o, 'error_category') and i.word.cleared != i.base:
        o['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
    # end

    _.ends(module, func)
# end


# return export
