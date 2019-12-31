from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.forms.noun'  # local


def remove_stress_if_one_syllable(value):  # export
    if _.contains_once(value, '{vowel+ё}'):
        return _.replaced(value, '́ ', '')
    # end
    return value
# end


@a.starts(module)
def apply_obelus(func, i):  # export
    if _.contains(i.rest_index, '÷'):
        i.result['obelus'] = '1'
    # end
    _.ends(module, func)
# end


@a.starts(module)
def apply_specific_3(func, i):  # export
    r = i.result  # local

    # Специфика по (3)
    if _.contains(i.rest_index, '%(3%)') or _.contains(i.rest_index, '③'):
        if _.endswith(r['prp-sg'], 'и'):
            r['prp-sg'] = r['prp-sg'] + '&nbsp;//<br />' + _.replaced(r['prp-sg'], 'и$', 'е')
        # end
        if i.gender == 'f' and _.endswith(r['dat-sg'], 'и'):
            r['dat-sg'] = r['dat-sg'] + '&nbsp;//<br />' + _.replaced(r['dat-sg'], 'и$', 'е')
        # end
    # end

    _.ends(module, func)
# end


#------------------------------------------------------------------------------


@a.starts(module)
def prt_case(func, i):  # Разделительный падеж
    r = i.result  # local

    if _.contains(i.index, 'Р2') or _.contains(i.index, 'Р₂'):
        r['prt-sg'] = r['dat-sg']
    # end
    if _.has_value(i.args, 'Р'):
        r['prt-sg'] = i.args['Р']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def loc_case(func, i):  # Местный падеж
    r = i.result  # local

    if _.contains(i.index, 'П2') or _.contains(i.index, 'П₂'):
        loc = r['dat-sg']  # local
        loc = _.replaced(loc, '́ ', '')
        loc = _.replaced(loc, 'ё', 'е')
        loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
        loc = remove_stress_if_one_syllable(loc)  # = export.
        r['loc-sg'] = loc
        loc_prep = _.extract(i.index, 'П2%((.+)%)')  # local
        if not loc_prep:
            loc_prep = _.extract(i.index, 'П₂%((.+)%)')
        # end
        if not loc_prep:
            loc_prep = 'в, на'
        # end
        r['loc-sg'] = '(' + loc_prep + ') ' + r['loc-sg']
        if _.contains(i.index, '%[П'):
            r['loc-sg'] = r['loc-sg'] + '&nbsp;//<br />' + r['prp-sg']
        # end
    # end
    if _.has_value(i.args, 'М'):
        r['loc-sg'] = i.args['М']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def voc_case(func, i):  # Звательный падеж
    r = i.result  # local

    if _.has_value(i.args, 'З'):
        r['voc-sg'] = i.args['З']
    elif _.contains(i.index, 'З'):
        if _.endswith(i.word.unstressed, ['а', 'я']):
            r['voc-sg'] = r['gen-pl']
        else:
            r['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
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
