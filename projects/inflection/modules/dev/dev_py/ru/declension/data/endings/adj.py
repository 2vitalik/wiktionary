from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'data.endings.adj'  # local


# Данные: все стандартные окончания для двух типов основ
@a.call(module)
def get_standard_adj_endings():  # export
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
    e.m.hard['nom-sg'] = ['ый', 'ой']
    e.m.hard['gen-sg'] = 'ого'
    e.m.hard['dat-sg'] = 'ому'
    e.m.hard['ins-sg'] = 'ым'
    e.m.hard['prp-sg'] = 'ом'
    e.m.hard['srt-sg'] = ''
    e.m.soft['nom-sg'] = 'ий'
    e.m.soft['gen-sg'] = 'его'
    e.m.soft['dat-sg'] = 'ему'
    e.m.soft['ins-sg'] = 'им'
    e.m.soft['prp-sg'] = 'ем'
    e.m.soft['srt-sg'] = 'ь'
    e.f.hard['nom-sg'] = 'ая'
    e.f.hard['gen-sg'] = 'ой'
    e.f.hard['dat-sg'] = 'ой'
    e.f.hard['acc-sg'] = 'ую'
    e.f.hard['ins-sg'] = 'ой'
    e.f.hard['prp-sg'] = 'ой'
    e.f.hard['srt-sg'] = 'а'
    e.f.soft['nom-sg'] = 'яя'
    e.f.soft['gen-sg'] = 'ей'
    e.f.soft['dat-sg'] = 'ей'
    e.f.soft['acc-sg'] = 'юю'
    e.f.soft['ins-sg'] = 'ей'
    e.f.soft['prp-sg'] = 'ей'
    e.f.soft['srt-sg'] = 'я'
    e.n.hard['nom-sg'] = 'ое'
    e.n.hard['gen-sg'] = 'ого'
    e.n.hard['dat-sg'] = 'ому'
    e.n.hard['ins-sg'] = 'ым'
    e.n.hard['prp-sg'] = 'ом'
    e.n.hard['srt-sg'] = 'о'
    e.n.soft['nom-sg'] = 'ее'
    e.n.soft['gen-sg'] = 'его'
    e.n.soft['dat-sg'] = 'ему'
    e.n.soft['ins-sg'] = 'им'
    e.n.soft['prp-sg'] = 'ем'
    e.n.soft['srt-sg'] = ['е', 'ё']
    e.common.hard['nom-pl'] = 'ые'
    e.common.hard['gen-pl'] = 'ых'
    e.common.hard['dat-pl'] = 'ым'
    e.common.hard['ins-pl'] = 'ыми'
    e.common.hard['prp-pl'] = 'ых'
    e.common.hard['srt-pl'] = 'ы'
    e.common.soft['nom-pl'] = 'ие'
    e.common.soft['gen-pl'] = 'их'
    e.common.soft['dat-pl'] = 'им'
    e.common.soft['ins-pl'] = 'ими'
    e.common.soft['prp-pl'] = 'их'
    e.common.soft['srt-pl'] = 'и'
    return e
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
@a.starts(module)
def fix_adj_pronoun_endings(func, i, pronoun):  # export
    d = i.data  # local

    # INFO: Replace "ы" to "и"
    if _.equals(i.stem.type, ['velar', 'sibilant']):
        if i.gender == 'm':
            if i.adj:
                d.endings['nom-sg'][unstressed] = 'ий'
            # end
            d.endings['ins-sg'] = 'им'
        # end
        if i.gender == 'n':
            d.endings['ins-sg'] = 'им'
        # end

        if i.adj:
            d.endings['nom-pl'] = 'ие'
        elif pronoun:
            d.endings['nom-pl'] = 'и'
        # end
        d.endings['gen-pl'] = 'их'
        d.endings['dat-pl'] = 'им'
        d.endings['ins-pl'] = 'ими'
        d.endings['prp-pl'] = 'их'
        if i.adj:
            d.endings['srt-pl'] = 'и'
        # end
    # end

    # INFO: Replace unstressed "о" to "е"
    if _.equals(i.stem.type, ['sibilant', 'letter-ц']):
        if not i.stress_schema['ending']['sg']:
            if i.gender == 'm':
                if i.adj:
                    d.endings['nom-sg'][stressed] = 'ей'
                # end
                d.endings['gen-sg'] = 'его'
                d.endings['dat-sg'] = 'ему'
                d.endings['prp-sg'] = 'ем'
            # end
            if i.gender == 'n':
                d.endings['nom-sg'] = 'ее'
                d.endings['gen-sg'] = 'его'
                d.endings['dat-sg'] = 'ему'
                d.endings['prp-sg'] = 'ем'
            # end
            if i.gender == 'f':
                d.endings['gen-sg'] = 'ей'
                d.endings['dat-sg'] = 'ей'
                d.endings['ins-sg'] = 'ей'
                d.endings['prp-sg'] = 'ей'
            # end
        # end
        if not i.stress_schema['ending']['srt-sg-n']:
            if i.gender == 'n':
                if i.adj:
                    d.endings['srt-sg'] = 'е'
                # end
            # end
        # end
    # end

    # INFO: Replace "ь" to "й"
    if _.equals(i.stem.type, {'vowel'}):
        if i.gender == 'm':
            if i.adj:
                d.endings['srt-sg'] = 'й'
            # end
        # end
    # end

    _.ends(module, func)
# end


# return export
