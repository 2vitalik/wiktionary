from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...modify.transform import reducable as reducable


module = 'modify.transform.degree'  # local


@a.starts(module)
def apply_specific_degree(func, stems, endings, word, stem, stem_type, gender, stress_type, rest_index, data):  # export
    # If degree sign °

    if _.contains(rest_index, '°') and _.endswith(word, '[ая]нин'):
        _.replace(stems, 'all-pl', '([ая])ни́ н$', '%1́ н')
        _.replace(stems, 'all-pl', '([ая]́ ?н)ин$', '%1')
        endings['nom-pl'] = 'е'
        endings['gen-pl'] = ''
        _.ends(module, func)
        return rest_index
    # end

    if _.contains(rest_index, '°') and _.endswith(word, 'ин'):
        _.replace(stems, 'all-pl', 'и́ ?н$', '')
        if not _.contains(rest_index, ['%(1%)', '①']):
            endings['nom-pl'] = 'е'
        # end
        endings['gen-pl'] = ''
    # end

    if _.contains(rest_index, '°') and _.endswith(word, ['ёнок', 'онок']):
        _.replace(stems, 'all-pl', 'ёнок$', 'я́т')
        _.replace(stems, 'all-pl', 'о́нок$', 'а́т')

        # INFO: Эмуляция среднего рода `1a` для форм мн. числа
        endings['nom-pl'] = 'а'
        endings['gen-pl'] = ''

        reducable.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index + '*', data, True)
        _.ends(module, func)
        return rest_index
    # end

    if _.contains(rest_index, '°') and _.endswith(word, ['ёночек', 'оночек']):

        _.replace(stems, 'all-pl', 'ёночек$', 'я́тк')
        _.replace(stems, 'all-pl', 'о́ночек$', 'а́тк')

        # INFO: Черездование для единичной формы (возможно применится также и для множественной, но это не страшно, потом заменится по идее)
        reducable.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index + '*', data, False)

        # INFO: По сути должно примениться только к мн. формам (случай `B`)
        reducable.apply_specific_reducable(stems, endings, word, stem, stem_type, 'f', stress_type, rest_index + '*', data, False)

        endings['gen-pl'] = ''  # INFO: Странный фикс, но он нужен.. <_<

        _.ends(module, func)
        return rest_index
    # end

    if _.contains(rest_index, '°') and gender == 'n' and _.endswith(word, 'мя'):
        _.replace(stems, 'all-sg', 'м$', 'мен')
        _.replace(stems, 'ins-sg', 'м$', 'мен')
        _.replace(stems, 'all-pl', 'м$', 'мен')

        endings['nom-sg'] = 'я'
        endings['gen-sg'] = 'и'
        endings['dat-sg'] = 'и'
        endings['ins-sg'] = 'ем'
        endings['prp-sg'] = 'и'
    # end

    _.ends(module, func)
    return rest_index
# end


# return export
