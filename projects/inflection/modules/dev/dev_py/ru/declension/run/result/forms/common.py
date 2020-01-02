from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.forms.common'  # local


@a.starts(module)
def fix_stress(func, o):  # export
    # Add stress if there is no one
    if _.contains_several(o['nom-sg'], '{vowel}') and not _.contains(o['nom-sg'], '[́ ё]'):
        # perhaps this is redundant for nom-sg?
        _.replace(o, 'nom-sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if _.contains_several(o['gen-pl'], '{vowel+ё}') and not _.contains(o['gen-pl'], '[́ ё]'):
        _.replace(o, 'gen-pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    _.ends(module, func)
# end


# Выбор винительного падежа
@a.starts(module)
def choose_accusative_forms(func, i):  # export
    p = i.parts  # local
    r = i.result  # local

    r['acc-sg-in'] = ''
    r['acc-sg-an'] = ''
    r['acc-pl-in'] = ''
    r['acc-pl-an'] = ''

    if i.gender == 'm' or (i.gender == 'n' and i.output_gender == 'm'):
        if i.animacy == 'in':
            r['acc-sg'] = r['nom-sg']
        elif i.animacy == 'an':
            r['acc-sg'] = r['gen-sg']
        else:
            r['acc-sg-in'] = r['nom-sg']
            r['acc-sg-an'] = r['gen-sg']
        # end
    elif i.gender == 'f':
        if _.equals(i.stem.type, ['f-3rd', 'f-3rd-sibilant']):
            r['acc-sg'] = r['nom-sg']
        else:
            r['acc-sg'] = p.stems['acc-sg'] + p.endings['acc-sg']  # todo: don't use `data` here?
        # end
    elif i.gender == 'n':
        r['acc-sg'] = r['nom-sg']
    # end

    if i.animacy == 'in':
        r['acc-pl'] = r['nom-pl']
    elif i.animacy == 'an':
        r['acc-pl'] = r['gen-pl']
    else:
        r['acc-pl-in'] = r['nom-pl']
        r['acc-pl-an'] = r['gen-pl']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def second_ins_case(func, i):  # export
    r = i.result  # local

    # Второй творительный
    if i.gender == 'f':
        ins_sg2 = _.replaced(r['ins-sg'], 'й$', 'ю')  # local
        if ins_sg2 != r['ins-sg']:
            r['ins-sg2'] = ins_sg2
        # end
    # end

    _.ends(module, func)
# end


# return export
