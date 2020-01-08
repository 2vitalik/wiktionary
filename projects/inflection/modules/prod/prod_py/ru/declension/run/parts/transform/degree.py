from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ....run.parts.transform import reducable as reducable


module = 'run.parts.transform.degree'  # local


@a.starts(module)
def apply_specific_degree(func, i):  # export
    # If degree sign °
    p = i.parts  # local
    word = i.word.unstressed  # local

    if _.contains(i.rest_index, '°') and _.endswith(word, '[ая]нин'):
        _.replace(p.stems, 'all-pl', '([ая])ни́ н$', '%1́ н')
        _.replace(p.stems, 'all-pl', '([ая]́ ?н)ин$', '%1')
        p.endings['nom-pl'] = 'е'
        p.endings['gen-pl'] = ''
        return _.returns(module, func, i.rest_index)
    # end

    if _.contains(i.rest_index, '°') and _.endswith(word, 'ин'):
        _.replace(p.stems, 'all-pl', 'и́ ?н$', '')
        if not _.contains(i.rest_index, ['%(1%)', '①']):
            p.endings['nom-pl'] = 'е'
        # end
        p.endings['gen-pl'] = ''
    # end

    if _.contains(i.rest_index, '°') and _.endswith(word, ['ёнок', 'онок']):
        _.replace(p.stems, 'all-pl', 'ёнок$', 'я́т')
        _.replace(p.stems, 'all-pl', 'о́нок$', 'а́т')

        # INFO: Эмуляция среднего рода `1a` для форм мн. числа
        p.endings['nom-pl'] = 'а'
        p.endings['gen-pl'] = ''

        reducable.apply_specific_reducable(i, i.gender, i.rest_index + '*', True)
        return _.returns(module, func, i.rest_index)
    # end

    if _.contains(i.rest_index, '°') and _.endswith(word, ['ёночек', 'оночек']):

        _.replace(p.stems, 'all-pl', 'ёночек$', 'я́тк')
        _.replace(p.stems, 'all-pl', 'о́ночек$', 'а́тк')

        # INFO: Черездование для единичной формы (возможно применится также и для множественной, но это не страшно, потом заменится по идее)
        reducable.apply_specific_reducable(i, i.gender, i.rest_index + '*', False)

        # INFO: По сути должно примениться только к мн. формам (случай `B`)
        reducable.apply_specific_reducable(i, 'f', i.rest_index + '*', False)

        p.endings['gen-pl'] = ''  # INFO: Странный фикс, но он нужен.. <_<

        return _.returns(module, func, i.rest_index)
    # end

    if _.contains(i.rest_index, '°') and i.gender == 'n' and _.endswith(word, 'мя'):
        _.replace(p.stems, 'all-sg', 'м$', 'мен')
        _.replace(p.stems, 'ins-sg', 'м$', 'мен')
        _.replace(p.stems, 'all-pl', 'м$', 'мен')

        p.endings['nom-sg'] = 'я'
        p.endings['gen-sg'] = 'и'
        p.endings['dat-sg'] = 'и'
        p.endings['ins-sg'] = 'ем'
        p.endings['prp-sg'] = 'и'
    # end

    return _.returns(module, func, i.rest_index)
# end


# return export
