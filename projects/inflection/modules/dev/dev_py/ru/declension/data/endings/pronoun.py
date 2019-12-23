from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'data.endings.pronoun'  # local


@a.call(module)
def get_standard_pronoun_endings():  # export
    e = a.AttrDict()  # AttrDict  # local
    e.m = a.AttrDict()  # AttrDict
    e.f = a.AttrDict()  # AttrDict
    e.n = a.AttrDict()  # AttrDict
    e.common = a.AttrDict()  # AttrDict
    e.m.hard = dict()  # dict
    e.m.soft = dict()  # dict
    e.f.hard = dict()  # dict
    e.f.soft = dict()  # dict
    e.n.hard = dict()  # dict
    e.n.soft = dict()  # dict
    e.common.hard = dict()  # dict
    e.common.soft = dict()  # dict
    e.m.hard['nom-sg'] = ''
    e.m.hard['gen-sg'] = 'ого'
    e.m.hard['dat-sg'] = 'ому'
    e.m.hard['ins-sg'] = 'ым'
    e.m.hard['prp-sg'] = 'ом'
    e.m.soft['nom-sg'] = 'ь'
    e.m.soft['gen-sg'] = 'его'
    e.m.soft['dat-sg'] = 'ему'
    e.m.soft['ins-sg'] = 'им'
    e.m.soft['prp-sg'] = ['ем', 'ём']
    e.f.hard['nom-sg'] = 'а'
    e.f.hard['gen-sg'] = 'ой'
    e.f.hard['dat-sg'] = 'ой'
    e.f.hard['acc-sg'] = 'у'
    e.f.hard['ins-sg'] = 'ой'
    e.f.hard['prp-sg'] = 'ой'
    e.f.soft['nom-sg'] = 'я'
    e.f.soft['gen-sg'] = 'ей'
    e.f.soft['dat-sg'] = 'ей'
    e.f.soft['acc-sg'] = 'ю'
    e.f.soft['ins-sg'] = 'ей'
    e.f.soft['prp-sg'] = 'ей'
    e.n.hard['nom-sg'] = 'о'
    e.n.hard['gen-sg'] = 'ого'
    e.n.hard['dat-sg'] = 'ому'
    e.n.hard['ins-sg'] = 'ым'
    e.n.hard['prp-sg'] = 'ом'
    e.n.soft['nom-sg'] = ['е', 'ё']
    e.n.soft['gen-sg'] = 'его'
    e.n.soft['dat-sg'] = 'ему'
    e.n.soft['ins-sg'] = 'им'
    e.n.soft['prp-sg'] = 'ем'
    e.common.hard['nom-pl'] = 'ы'
    e.common.hard['gen-pl'] = 'ых'
    e.common.hard['dat-pl'] = 'ым'
    e.common.hard['ins-pl'] = 'ыми'
    e.common.hard['prp-pl'] = 'ых'
    e.common.soft['nom-pl'] = 'и'
    e.common.soft['gen-pl'] = 'их'
    e.common.soft['dat-pl'] = 'им'
    e.common.soft['ins-pl'] = 'ими'
    e.common.soft['prp-pl'] = 'их'
    return e
# end


@a.call(module)
def get_standard_pronoun_noun_endings():  # export
    e = a.AttrDict()  # AttrDict  # local
    e.m = a.AttrDict()  # AttrDict
    e.f = a.AttrDict()  # AttrDict
    e.n = a.AttrDict()  # AttrDict
    e.common = a.AttrDict()  # AttrDict
    e.m.hard = dict()  # dict
    e.m.soft = dict()  # dict
    e.f.hard = dict()  # dict
    e.f.soft = dict()  # dict
    e.n.hard = dict()  # dict
    e.n.soft = dict()  # dict
    e.common.hard = dict()  # dict
    e.common.soft = dict()  # dict
    e.m.hard['nom-sg'] = ''
    e.m.hard['gen-sg'] = 'а'
    e.m.hard['dat-sg'] = 'у'
    e.m.hard['ins-sg'] = 'ым'
    e.m.hard['prp-sg'] = 'е'
    e.m.soft['nom-sg'] = 'ь'
    e.m.soft['gen-sg'] = 'я'
    e.m.soft['dat-sg'] = 'ю'
    e.m.soft['ins-sg'] = 'им'
    e.m.soft['prp-sg'] = ['ем', 'ём']
    e.f.hard['nom-sg'] = 'а'
    e.f.hard['gen-sg'] = 'а'
    e.f.hard['dat-sg'] = 'ой'
    e.f.hard['acc-sg'] = 'у'
    e.f.hard['ins-sg'] = 'ой'
    e.f.hard['prp-sg'] = 'ой'
    e.f.soft['nom-sg'] = 'я'
    e.f.soft['gen-sg'] = 'ей'
    e.f.soft['dat-sg'] = 'ей'
    e.f.soft['acc-sg'] = 'ю'
    e.f.soft['ins-sg'] = 'ей'
    e.f.soft['prp-sg'] = 'ей'
    e.n.hard['nom-sg'] = 'о'
    e.n.hard['gen-sg'] = 'а'
    e.n.hard['dat-sg'] = 'у'
    e.n.hard['ins-sg'] = 'ым'
    e.n.hard['prp-sg'] = 'е'
    e.n.soft['nom-sg'] = ['е', 'ё']
    e.n.soft['gen-sg'] = 'я'
    e.n.soft['dat-sg'] = 'ю'
    e.n.soft['ins-sg'] = 'им'
    e.n.soft['prp-sg'] = ['ем', 'ём']
    e.common.hard['nom-pl'] = 'ы'
    e.common.hard['gen-pl'] = 'ых'
    e.common.hard['dat-pl'] = 'ым'
    e.common.hard['ins-pl'] = 'ыми'
    e.common.hard['prp-pl'] = 'ых'
    e.common.soft['nom-pl'] = 'и'
    e.common.soft['gen-pl'] = 'их'
    e.common.soft['dat-pl'] = 'им'
    e.common.soft['ins-pl'] = 'ими'
    e.common.soft['prp-pl'] = 'их'
    return e
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
@a.starts(module)
def fix_pronoun_noun_endings(func, endings, gender, stem_type, stress_schema):  # export
    # INFO: Replace "ы" to "и"
    if _.equals(stem_type, {'sibilant'}):
        if _.In(gender, ['m', 'n']):
            endings['ins-sg'] = 'им'
        # end

        endings['nom-pl'] = 'и'
        endings['gen-pl'] = 'их'
        endings['dat-pl'] = 'им'
        endings['ins-pl'] = 'ими'
        endings['prp-pl'] = 'их'
    # end

    # INFO: Other Replace
    if _.equals(stem_type, {'sibilant'}):
        if gender == 'n':
            endings['nom-sg'] = {'е', 'о' }
        # end
        if _.In(gender, ['m', 'n']):
            endings['gen-sg'] = ['его', 'ого']
            endings['dat-sg'] = ['ему', 'ому']
            endings['prp-sg'] = ['ем', 'ом']
        # end
        if gender == 'f':
            endings['gen-sg'] = ['ей', 'ой']
            endings['dat-sg'] = ['ей', 'ой']
            endings['ins-sg'] = ['ей', 'ой']
            endings['prp-sg'] = ['ей', 'ой']
        # end
    # end

    if _.equals(stem_type, {'vowel'}):
        if _.In(gender, ['m', 'n']):
            endings['gen-sg'] = 'его'
            endings['dat-sg'] = 'ему'
        # end
    # end

    _.ends(module, func)
# end


# return export
