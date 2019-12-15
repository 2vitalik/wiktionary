from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..modify import reducable


module = 'modify.degree'  # local


@a.starts(module)
def apply_specific_degree(func, stems, endings, word, stem, stem_type, gender, stress_type, rest_index, data):  # export
    # If degree sign °

    if _.contains(rest_index, '°') and _.endswith(word, '[ая]нин'):
        _.replace(stems, 'all_pl', '([ая])ни́ н$', '%1́ н')
        _.replace(stems, 'all_pl', '([ая]́ ?н)ин$', '%1')
        endings['nom_pl'] = 'е'
        endings['gen_pl'] = ''
        _.ends(module, func)
        return rest_index
    # end

    if _.contains(rest_index, '°') and _.endswith(word, 'ин'):
        _.replace(stems, 'all_pl', 'и́ ?н$', '')
        if not _.contains(rest_index, ['%(1%)', '①']):
            endings['nom_pl'] = 'е'
        # end
        endings['gen_pl'] = ''
    # end

    if _.contains(rest_index, '°') and _.endswith(word, ['ёнок', 'онок']):
        _.replace(stems, 'all_pl', 'ёнок$', 'я́т')
        _.replace(stems, 'all_pl', 'о́нок$', 'а́т')

        # INFO: Эмуляция среднего рода `1a` для форм мн. числа
        endings['nom_pl'] = 'а'
        endings['gen_pl'] = ''

        reducable.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index + '*', data, True)  # export.
        _.ends(module, func)
        return rest_index
    # end

    if _.contains(rest_index, '°') and _.endswith(word, ['ёночек', 'оночек']):

        _.replace(stems, 'all_pl', 'ёночек$', 'я́тк')
        _.replace(stems, 'all_pl', 'о́ночек$', 'а́тк')

        # INFO: Черездование для единичной формы (возможно применится также и для множественной, но это не страшно, потом заменится по идее)
        reducable.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index + '*', data, False)  # export.

        # INFO: По сути должно примениться только к мн. формам (случай `B`)
        reducable.apply_specific_reducable(stems, endings, word, stem, stem_type, 'f', stress_type, rest_index + '*', data, False)  # export.

        endings['gen_pl'] = ''  # INFO: Странный фикс, но он нужен.. <_<

        _.ends(module, func)
        return rest_index
    # end

    if _.contains(rest_index, '°') and gender == 'n' and _.endswith(word, 'мя'):
        _.replace(stems, 'all_sg', 'м$', 'мен')
        _.replace(stems, 'ins_sg', 'м$', 'мен')
        _.replace(stems, 'all_pl', 'м$', 'мен')

        endings['nom_sg'] = 'я'
        endings['gen_sg'] = 'и'
        endings['dat_sg'] = 'и'
        endings['ins_sg'] = 'ем'
        endings['prp_sg'] = 'и'
    # end

    _.ends(module, func)
    return rest_index
# end
