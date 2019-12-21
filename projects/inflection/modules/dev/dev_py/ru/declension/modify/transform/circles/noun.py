from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


# constants:
unstressed = 0  # local
stressed = 1  # local
module = 'modify.transform.circles.noun'  # local


@a.starts(module)
def apply_noun_specific_1_2(func, endings, gender, stem_type, stem_base_type, rest_index):  # export
    if _.contains(rest_index, ['%(1%)', '①']):
        if stem_base_type == 'hard':
            if gender == 'm': endings['nom_pl'] = 'а' # end
            if gender == 'n': endings['nom_pl'] = 'ы' # end
        # end
        if stem_base_type == 'soft':
            if gender == 'm': endings['nom_pl'] = 'я' # end
            if gender == 'n': endings['nom_pl'] = 'и' # end
        # end
        if _.equals(stem_type, ['velar', 'sibilant']):  # Replace "ы" to "и"
            if gender == 'n': endings['nom_pl'] = 'и' # end
        # end
    # end

    if _.contains(rest_index, ['%(2%)', '②']):
        if stem_base_type == 'hard':
            if gender == 'm': endings['gen_pl'] = ['', ''] # end
            if gender == 'n': endings['gen_pl'] = ['ов', 'ов'] # end
            if gender == 'f': endings['gen_pl'] = {'ей', 'ей' } # end
        # end
        if stem_base_type == 'soft':
            if gender == 'm': endings['gen_pl'] = ['ь', 'ь'] # end
            if gender == 'n': endings['gen_pl'] = ['ев', 'ёв']  # end
            if gender == 'f': endings['gen_pl'] = {'ей', 'ей' } # end
        # end
        if _.equals(stem_type, ['sibilant', 'letter-ц']):  # Replace unstressed "о" to "е"
            if gender == 'n': endings['gen_pl'][unstressed] = 'ев' # end
        # end

#        # Possibly we don't need this:
#            # Replace "ов", "ев", "ёв" and null to "ей"
#            if stem_type = {'sibilant'}}
#                if gender == 'n': endings['gen_pl'] = ['ей', 'ей']
#                if gender == 'm': endings['gen_pl'][stressed] = 'ей'
#            # end
#            # Replace "ь" to "й"
#            if stem_type = ['vowel', 'letter-и']}
#                if gender == 'm': endings['gen_pl'][stressed] = ['й', 'й']
#            # end
#            # Replace "ей" to "ев/ёв", and "ь,ей" to "й"
#            if stem_type = ['vowel', 'letter-и']}
#                if gender == 'f': endings['gen_pl'][unstressed] = ['ев', 'ёв']
#                if gender == 'm': endings['gen_pl'][stressed] = ['й', 'й']
#            # end
#        #
    # end

    _.ends(module, func)
# end


# return export
