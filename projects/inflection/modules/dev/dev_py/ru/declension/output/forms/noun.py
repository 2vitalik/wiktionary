from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'output.forms.noun'  # local


def remove_stress_if_one_syllable(value):  # export
    # _.call('noun.forms', 'remove_stress_if_one_syllable')

    if _.contains_once(value, '{vowel+ё}'):
        return _.replaced(value, '́ ', '')
    # end
    return value
# end


@a.starts(module)
def apply_obelus(func, out_args, rest_index):  # export
    if _.contains(rest_index, '÷'):
        out_args['obelus'] = '1'
    # end

    _.ends(module, func)
# end


@a.starts(module)
def apply_specific_3(func, out_args, gender, rest_index):  # export
    # Специфика по (3)
    if _.contains(rest_index, '%(3%)') or _.contains(rest_index, '③'):
        if _.endswith(out_args['prp_sg'], 'и'):
            out_args['prp_sg'] = out_args['prp_sg'] + '&nbsp;//<br />' + _.replaced(out_args['prp_sg'], 'и$', 'е')
        # end
        if gender == 'f' and _.endswith(out_args['dat_sg'], 'и'):
            out_args['dat_sg'] = out_args['dat_sg'] + '&nbsp;//<br />' + _.replaced(out_args['dat_sg'], 'и$', 'е')
        # end
    # end

    _.ends(module, func)
# end



#------------------------------------------------------------------------------


@a.starts(module)
def prt_case(func, out_args, args, index):  # Разделительный падеж
    if _.contains(index, 'Р2') or _.contains(index, 'Р₂'):
        out_args['prt_sg'] = out_args['dat_sg']
    # end
    if _.has_value(args, 'Р'):
        out_args['prt_sg'] = args['Р']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def loc_case(func, out_args, args, index):  # Местный падеж
    # local loc, loc_prep

    if _.contains(index, 'П2') or _.contains(index, 'П₂'):
        loc = out_args['dat_sg']
        loc = _.replaced(loc, '́ ', '')
        loc = _.replaced(loc, 'ё', 'е')
        loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
        loc = remove_stress_if_one_syllable(loc)  # = export.
        out_args['loc_sg'] = loc
        loc_prep = '?'
        loc_prep = _.extract(index, 'П2%((.+)%)')
        if not loc_prep:
            loc_prep = _.extract(index, 'П₂%((.+)%)')
        # end
        if not loc_prep:
            loc_prep = 'в, на'
        # end
        out_args['loc_sg'] = '(' + loc_prep + ') ' + out_args['loc_sg']
        if _.contains(index, '%[П'):
            out_args['loc_sg'] = out_args['loc_sg'] + '&nbsp;//<br />' + out_args['prp_sg']
        # end
    # end
    if _.has_value(args, 'М'):
        out_args['loc_sg'] = args['М']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def voc_case(func, out_args, args, index, word):  # Звательный падеж
    if _.has_value(args, 'З'):
        out_args['voc_sg'] = args['З']
    elif _.contains(index, 'З'):
        if _.endswith(word, ['а', 'я']):
            out_args['voc_sg'] = out_args['gen_pl']
        else:
            out_args['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def special_cases(func, out_args, args, index, word):  # export
    prt_case(out_args, args, index)
    loc_case(out_args, args, index)
    voc_case(out_args, args, index, word)

    _.ends(module, func)
# end


# return export
