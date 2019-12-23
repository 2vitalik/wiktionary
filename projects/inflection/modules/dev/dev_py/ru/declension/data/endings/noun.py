from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'data.endings.noun'  # local


# Данные: все стандартные окончания для двух типов основ
@a.call(module)
def get_standard_noun_endings():  # export
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
    e.m.hard['ins-sg'] = 'ом'
    e.m.hard['nom-pl'] = 'ы'
    e.m.hard['gen-pl'] = ['ов', 'ов']  # TODO: possibly we can join them together again: m_hard_gen_pl stressed and unstressed
    e.m.soft['nom-sg'] = 'ь'
    e.m.soft['gen-sg'] = 'я'
    e.m.soft['dat-sg'] = 'ю'
    e.m.soft['ins-sg'] = ['ем', 'ём']
    e.m.soft['nom-pl'] = 'и'
    e.m.soft['gen-pl'] = ['ей', 'ей']
    e.f.hard['nom-sg'] = 'а'
    e.f.hard['gen-sg'] = 'ы'
    e.f.hard['dat-sg'] = 'е'
    e.f.hard['acc-sg'] = 'у'
    e.f.hard['ins-sg'] = 'ой'
    e.f.hard['nom-pl'] = 'ы'
    e.f.hard['gen-pl'] = ['', '']
    e.f.soft['nom-sg'] = 'я'
    e.f.soft['gen-sg'] = 'и'
    e.f.soft['dat-sg'] = ['е', 'е']
    e.f.soft['acc-sg'] = 'ю'
    e.f.soft['ins-sg'] = ['ей', 'ёй']
    e.f.soft['nom-pl'] = 'и'
    e.f.soft['gen-pl'] = ['ь', 'ей']
    e.n.hard['nom-sg'] = 'о'
    e.n.hard['gen-sg'] = 'а'
    e.n.hard['dat-sg'] = 'у'
    e.n.hard['ins-sg'] = 'ом'
    e.n.hard['nom-pl'] = 'а'
    e.n.hard['gen-pl'] = ['', '']
    e.n.soft['nom-sg'] = 'е',  # was: ['е', 'ё']
    e.n.soft['gen-sg'] = 'я'
    e.n.soft['dat-sg'] = 'ю'
    e.n.soft['ins-sg'] = ['ем', 'ём']
    e.n.soft['nom-pl'] = 'я'
    e.n.soft['gen-pl'] = ['ь', 'ей']
    e.common.hard['prp-sg'] = ['е', 'е']
    e.common.hard['dat-pl'] = 'ам'
    e.common.hard['ins-pl'] = 'ами'
    e.common.hard['prp-pl'] = 'ах'
    e.common.soft['prp-sg'] = ['е', 'е']
    e.common.soft['dat-pl'] = 'ям'
    e.common.soft['ins-pl'] = 'ями'
    e.common.soft['prp-pl'] = 'ях'
    return e
# end


# Изменение окончаний для остальных типов основ (базирующихся на первых двух)
@a.starts(module)
def fix_noun_endings(func, i):  # export
    d = i.data  # local

    # INFO: Replace "ы" to "и"
    if _.equals(i.stem.type, ['velar', 'sibilant']):
        if i.gender == 'f': d.endings['gen-sg'] = 'и' # end
        if i.gender == 'm': d.endings['nom-pl'] = 'и' # end
        if i.gender == 'f': d.endings['nom-pl'] = 'и' # end
    # end

    # INFO: Replace unstressed "о" to "е"
    if _.equals(i.stem.type, ['sibilant', 'letter-ц']):
        if not i.stress_schema['ending']['nom-sg']:
            if i.gender == 'n': d.endings['nom-sg'] = 'е' # end # ???
        # end
        if not i.stress_schema['ending']['ins-sg']:
            if i.gender == 'm': d.endings['ins-sg'] = 'ем' # end
            if i.gender == 'n': d.endings['ins-sg'] = 'ем' # end
            if i.gender == 'f': d.endings['ins-sg'] = 'ей' # end
        # end
        if not i.stress_schema['ending']['gen-pl']:
            if i.gender == 'm': d.endings['gen-pl'] = ['ев', 'ев'] # end  # TODO: should we change stressed value here?
        # end
    # end

    if _.equals(i.stem.type, 'sibilant'):
        # Replace "ов", "ев", "ёв" and null to "ей"
        if i.gender == 'm': d.endings['gen-pl'] = ['ей', 'ей']   # end
        if i.gender == 'n': d.endings['gen-pl'][stressed] = 'ей' # end
#        if i.gender == 'n': d.endings['gen-pl'][unstressed] = '' # end # this is just don't changed
        if i.gender == 'f': d.endings['gen-pl'][stressed] = 'ей' # end
#        if i.gender == 'f': d.endings['gen-pl'][unstressed] = '' # end # this is just don't changed
    # end

    # INFO: Replace "ь" to "й"
    if _.equals(i.stem.type, ['vowel', 'letter-и']):
        if i.gender == 'm': d.endings['nom-sg'] = 'й'             # end # ???
        if i.gender == 'n': d.endings['gen-pl'][unstressed] = 'й' # end
        if i.gender == 'f': d.endings['gen-pl'][unstressed] = 'й' # end
    # end

    # INFO: Replace "ей" to "ев/ёв", and "ь,ей" to "й"
    if _.equals(i.stem.type, ['vowel', 'letter-и']):
        if i.gender == 'm': d.endings['gen-pl'] = ['ев', 'ёв'] # end
        if i.gender == 'n': d.endings['gen-pl'] = ['й', 'й']   # end
        if i.gender == 'f': d.endings['gen-pl'] = ['й', 'й']   # end
    # end

    if _.equals(i.stem.type, 'letter-и'):
        if i.gender == 'f': d.endings['dat-sg'][unstressed] = 'и' # end
        d.endings['prp-sg'][unstressed] = 'и'
    # end

    if _.equals(i.stem.type, 'm-3rd'):
        if i.gender == 'm': d.endings['gen-sg'] = 'и' # end
        if i.gender == 'm': d.endings['dat-sg'] = 'и' # end
        d.endings['prp-sg'] = ['и', 'и']
    # end

    if _.equals(i.stem.type, ['f-3rd', 'f-3rd-sibilant']):
        if i.gender == 'f': d.endings['nom-sg'] = 'ь' # end
        if i.gender == 'f': d.endings['dat-sg'] = ['и', 'и'] # end
        if i.gender == 'f': d.endings['acc-sg'] = 'ь' # end
        if i.gender == 'f': d.endings['ins-sg'] = ['ью', 'ью'] # end
        d.endings['prp-sg'] = ['и', 'и']
        if i.gender == 'f': d.endings['gen-pl'] = ['ей', 'ей'] # end
    # end

    if _.equals(i.stem.type, 'f-3rd-sibilant'):
        d.endings['dat-pl'] = 'ам'
        d.endings['ins-pl'] = 'ами'
        d.endings['prp-pl'] = 'ах'
    # end

    _.ends(module, func)
# end


# return export
