from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'run.parts.transform.circles.noun'  # local


@a.starts(module)
def apply_noun_specific_1_2(func, i):  # export
    p = i.parts  # local

    if _.contains(i.rest_index, ['%(1%)', '①']):
        if i.stem.base_type == 'hard':
            if i.gender == 'm': p.endings['nom-pl'] = 'а' # end
            if i.gender == 'n': p.endings['nom-pl'] = 'ы' # end
        # end
        if i.stem.base_type == 'soft':
            if i.gender == 'm': p.endings['nom-pl'] = 'я' # end
            if i.gender == 'n': p.endings['nom-pl'] = 'и' # end
        # end
        if _.equals(i.stem.type, ['velar', 'sibilant']):  # Replace "ы" to "и"
            if i.gender == 'n': p.endings['nom-pl'] = 'и' # end
        # end
    # end

    if _.contains(i.rest_index, ['%(2%)', '②']):
        if i.stem.base_type == 'hard':
            if i.gender == 'm': p.endings['gen-pl'] = ['', ''] # end
            if i.gender == 'n': p.endings['gen-pl'] = ['ов', 'ов'] # end
            if i.gender == 'f': p.endings['gen-pl'] = {'ей', 'ей' } # end
        # end
        if i.stem.base_type == 'soft':
            if i.gender == 'm': p.endings['gen-pl'] = ['ь', 'ь'] # end
            if i.gender == 'n': p.endings['gen-pl'] = ['ев', 'ёв']  # end
            if i.gender == 'f': p.endings['gen-pl'] = {'ей', 'ей' } # end
        # end
        if _.equals(i.stem.type, ['sibilant', 'letter-ц']):  # Replace unstressed "о" to "е"
            if i.gender == 'n': p.endings['gen-pl'][unstressed] = 'ев' # end
        # end

#        # Possibly we don't need this:
#            # Replace "ов", "ев", "ёв" and null to "ей"
#            if i.stem.type = {'sibilant'}}
#                if i.gender == 'n': p.endings['gen-pl'] = ['ей', 'ей']
#                if i.gender == 'm': p.endings['gen-pl'][stressed] = 'ей'
#            # end
#            # Replace "ь" to "й"
#            if i.stem.type = ['vowel', 'letter-и']}
#                if i.gender == 'm': p.endings['gen-pl'][stressed] = ['й', 'й']
#            # end
#            # Replace "ей" to "ев/ёв", and "ь,ей" to "й"
#            if i.stem.type = ['vowel', 'letter-и']}
#                if i.gender == 'f': p.endings['gen-pl'][unstressed] = ['ев', 'ёв']
#                if i.gender == 'm': p.endings['gen-pl'][stressed] = ['й', 'й']
#            # end
#        #
    # end

    _.ends(module, func)
# end


# return export
