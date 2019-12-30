from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'output.forms.noun'  # local


def remove_stress_if_one_syllable(value):  # export
    if _.contains_once(value, '{vowel+ё}'):
        return _.replaced(value, '́ ', '')
    # end
    return value
# end


@a.starts(module)
def apply_obelus(func, i):  # export
    if _.contains(i.rest_index, '÷'):
        i.out_args['obelus'] = '1'
    # end
    _.ends(module, func)
# end


@a.starts(module)
def apply_specific_3(func, i):  # export
    o = i.out_args  # local

    # Специфика по (3)
    if _.contains(i.rest_index, '%(3%)') or _.contains(i.rest_index, '③'):
        if _.endswith(o['prp-sg'], 'и'):
            o['prp-sg'] = o['prp-sg'] + '&nbsp;//<br />' + _.replaced(o['prp-sg'], 'и$', 'е')
        # end
        if i.gender == 'f' and _.endswith(o['dat-sg'], 'и'):
            o['dat-sg'] = o['dat-sg'] + '&nbsp;//<br />' + _.replaced(o['dat-sg'], 'и$', 'е')
        # end
    # end

    _.ends(module, func)
# end


#------------------------------------------------------------------------------


@a.starts(module)
def prt_case(func, i):  # Разделительный падеж
    o = i.out_args  # local

    if _.contains(i.index, 'Р2') or _.contains(i.index, 'Р₂'):
        o['prt-sg'] = o['dat-sg']
    # end
    if _.has_value(i.args, 'Р'):
        o['prt-sg'] = i.args['Р']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def loc_case(func, i):  # Местный падеж
    o = i.out_args  # local

    if _.contains(i.index, 'П2') or _.contains(i.index, 'П₂'):
        loc = o['dat-sg']  # local
        loc = _.replaced(loc, '́ ', '')
        loc = _.replaced(loc, 'ё', 'е')
        loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
        loc = remove_stress_if_one_syllable(loc)  # = export.
        o['loc-sg'] = loc
        loc_prep = _.extract(i.index, 'П2%((.+)%)')  # local
        if not loc_prep:
            loc_prep = _.extract(i.index, 'П₂%((.+)%)')
        # end
        if not loc_prep:
            loc_prep = 'в, на'
        # end
        o['loc-sg'] = '(' + loc_prep + ') ' + o['loc-sg']
        if _.contains(i.index, '%[П'):
            o['loc-sg'] = o['loc-sg'] + '&nbsp;//<br />' + o['prp-sg']
        # end
    # end
    if _.has_value(i.args, 'М'):
        o['loc-sg'] = i.args['М']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def voc_case(func, i):  # Звательный падеж
    o = i.out_args  # local

    if _.has_value(i.args, 'З'):
        o['voc-sg'] = i.args['З']
    elif _.contains(i.index, 'З'):
        if _.endswith(i.word.unstressed, ['а', 'я']):
            o['voc-sg'] = o['gen-pl']
        else:
            o['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def special_cases(func, i):  # export
    prt_case(i)
    loc_case(i)
    voc_case(i)
    _.ends(module, func)
# end


# return export
