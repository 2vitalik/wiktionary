from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'output.init_out_args'  # local


# Формирование параметров рода и одушевлённости для подстановки в шаблон
@a.starts(module)
def forward_gender_animacy(func, info):
    # local genders, animacies

    # Род:
    genders = dict(m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж' )  # dict
    if info.common_gender:
        info.out_args['род'] = 'общ'
    elif info.output_gender:
        info.out_args['род'] = genders[info.output_gender]
    elif info.gender:
        info.out_args['род'] = genders[info.gender]
    else:
        pass
    # end

    # Одушевлённость:
    animacies = dict()  # dict
    animacies['in'] = 'неодуш'
    animacies['an'] = 'одуш'
    animacies['in//an'] = 'неодуш-одуш'
    animacies['an//in'] = 'одуш-неодуш'
    if info.output_animacy:
        info.out_args['кат'] = animacies[info.output_animacy]
    else:
        info.out_args['кат'] = animacies[info.animacy]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def additional_arguments(func, info):
    # RU (склонение)
    if _.contains(info.rest_index, '0'):
        info.out_args['скл'] = 'не'
    elif info.adj:
        info.out_args['скл'] = 'а'
    elif info.pronoun:
        info.out_args['скл'] = 'мс'
    elif _.endswith(info.word.unstressed, '[ая]'):
        info.out_args['скл'] = '1'
    else:
        if info.gender == 'm' or info.gender == 'n':
            info.out_args['скл'] = '2'
        else:
            info.out_args['скл'] = '3'
        # end
    # end

    # RU (чередование)
    if _.contains(info.index, '%*'):
        info.out_args['чередование'] = '1'
    # end

    if info.pt:
        info.out_args['pt'] = '1'
    # end

    # RU ("-" в индексе)
    # TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
    if info.rest_index:
        if _.contains(info.rest_index, ['%-', '—', '−']):
            info.out_args['st'] = '1'
            info.out_args['затрудн'] = '1'
        # end
    else:
        pass  # TODO
    # end

    _.ends(module, func)
# end


@a.starts(module)
def init_out_args(func, info):
    info.out_args['stem_type'] = info.stem.type  # for testcases
    info.out_args['stress_type'] = info.stress_type  # for categories   -- is really used?

    info.out_args['dev'] = dev_prefix
    info.out_args['зализняк'] = '??'  # значение по умолчанию

    additional_arguments(info)

    if info.noun:
        forward_gender_animacy(info)
    # end

    if not _.has_key(info.out_args, 'error_category') and info.word.cleared != info.base:
        info.out_args['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
    # end

    _.ends(module, func)
# end


# return export
