from projects.inflection.modules.dev.py import additional
from projects.inflection.modules.dev.py import mw
from projects.inflection.modules.dev.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


def remove_stress_if_one_syllable(value):  # export
    # _.log_func('forms', 'remove_stress_if_one_syllable')

    if _.contains_once(value, '{vowel+ё}'):
        return _.replaced(value, '́ ', '')
    # end
    return value
# end


def apply_obelus(forms, rest_index):  # export
    _.log_func('forms', 'apply_obelus')

    if _.contains(rest_index, '÷'):
        forms['obelus'] = '1'
    # end
# end


def apply_specific_3(forms, gender, rest_index):  # export
    _.log_func('forms', 'apply_specific_3')

    # Специфика по (3)
    if _.contains(rest_index, '%(3%)') or _.contains(rest_index, '③'):
        if _.endswith(forms['prp_sg'], 'и'):
            forms['prp_sg'] = forms['prp_sg'] + '&nbsp;//<br />' + _.replaced(forms['prp_sg'], 'и$', 'е')
        # end
        if gender == 'f' and _.endswith(forms['dat_sg'], 'и'):
            forms['dat_sg'] = forms['dat_sg'] + '&nbsp;//<br />' + _.replaced(forms['dat_sg'], 'и$', 'е')
        # end
    # end
# end



#------------------------------------------------------------------------------


def prt_case(forms, args, index):  # Разделительный падеж
    _.log_func('forms', 'prt_case')

    if _.contains(index, 'Р2') or _.contains(index, 'Р₂'):
        forms['prt_sg'] = forms['dat_sg']
    # end
    if _.has_value(args, 'Р'):
        forms['prt_sg'] = args['Р']
    # end
# end


def loc_case(forms, args, index):  # Местный падеж
    _.log_func('forms', 'loc_case')

    # local loc, loc_prep

    if _.contains(index, 'П2') or _.contains(index, 'П₂'):
        loc = forms['dat_sg']
        loc = _.replaced(loc, '́ ', '')
        loc = _.replaced(loc, 'ё', 'е')
        loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
        loc = remove_stress_if_one_syllable(loc)  # = export.
        forms['loc_sg'] = loc
        loc_prep = '?'
        loc_prep = _.extract(index, 'П2%((.+)%)')
        if not loc_prep:
            loc_prep = _.extract(index, 'П₂%((.+)%)')
        # end
        if not loc_prep:
            loc_prep = 'в, на'
        # end
        forms['loc_sg'] = '(' + loc_prep + ') ' + forms['loc_sg']
        if _.contains(index, '%[П'):
            forms['loc_sg'] = forms['loc_sg'] + '&nbsp;//<br />' + forms['prp_sg']
        # end
    # end
    if _.has_value(args, 'М'):
        forms['loc_sg'] = args['М']
    # end
# end


def voc_case(forms, args, index, word):  # Звательный падеж
    _.log_func('forms', 'voc_case')

    if _.has_value(args, 'З'):
        forms['voc_sg'] = args['З']
    elif _.contains(index, 'З'):
        if _.endswith(word, ['а', 'я']):
            forms['voc_sg'] = forms['gen_pl']
        else:
            forms['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
        # end
    # end
# end


def special_cases(forms, args, index, word):  # export
    _.log_func('forms', 'special_cases')

    prt_case(forms, args, index)
    loc_case(forms, args, index)
    voc_case(forms, args, index, word)
# end


# return export
