from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.result import index as index
from ...run.result import forward as forward


module = 'run.result.init_out_args'  # local

# todo: move this to root `init` package


# Формирование параметров рода и одушевлённости для подстановки в шаблон
@a.starts(module)
def forward_gender_animacy(func, i):
    r = i.result  # local

    # Род:
    genders = dict(m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж')  # dict  # local

    if i.common_gender:
        r['род'] = 'общ'
    elif i.output_gender:
        r['род'] = genders[i.output_gender]
    elif i.gender:
        r['род'] = genders[i.gender]
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
        r['кат'] = animacies[i.output_animacy]
    else:
        r['кат'] = animacies[i.animacy]
    # end

    _.ends(module, func)
# end


@a.starts(module)
def additional_arguments(func, i):
    r = i.result  # local

    # RU (склонение)
    if _.contains(i.rest_index, '0'):
        r['скл'] = 'не'
    elif i.adj:
        r['скл'] = 'а'
    elif i.pronoun:
        r['скл'] = 'мс'
    elif _.endswith(i.word.unstressed, '[ая]'):
        r['скл'] = '1'
    else:
        if i.gender == 'm' or i.gender == 'n':
            r['скл'] = '2'
        else:
            r['скл'] = '3'
        # end
    # end

    # RU (чередование)
    if _.contains(i.index, '%*'):
        r['чередование'] = '1'
    # end

    if i.pt:
        r['pt'] = '1'
    # end

    # RU ("-" в индексе)
    # TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
    if i.rest_index:
        if _.contains(i.rest_index, ['%-', '—', '−']):
            r['st'] = '1'
            r['затрудн'] = '1'
        # end
    else:
        pass  # TODO
    # end

    _.ends(module, func)
# end


@a.starts(module)
def init_out_args(func, i):  # export
    r = i.result  # local

    r['stem_type'] = i.stem.type  # for testcases
    r['stress_type'] = i.stress_type  # for categories   -- is really used?

    r['dev'] = dev_prefix

    index.get_zaliznyak(i)

    additional_arguments(i)

    if i.noun:
        forward_gender_animacy(i)
    # end

    if _.contains(i.rest_index, ['⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)']):
        r['краткая'] = '⊠'
    elif _.contains(i.rest_index, ['✕', '×', 'x', 'х', 'X', 'Х']):
        r['краткая'] = '✕'
    elif _.contains(i.rest_index, ['%-', '—', '−']):
        r['краткая'] = '−'
    else:
        r['краткая'] = '1'
    # end

    if not _.has_key(r, 'error_category') and i.word.cleared != i.base:
        r['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
    # end

    forward.forward_args(i)

    _.ends(module, func)
# end


# return export
