from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.forms.common'  # local


@a.starts(module)
def fix_stress(func, i):  # export
    r = i.result  # local

    # Add stress if there is no one
    if i.calc_sg and _.contains_several(r['nom-sg'], '{vowel}') and not _.contains(r['nom-sg'], '[́ ё]'):
        # perhaps this is redundant for nom-sg?
        _.replace(r, 'nom-sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if i.calc_pl and _.contains_several(r['gen-pl'], '{vowel+ё}') and not _.contains(r['gen-pl'], '[́ ё]'):
        _.replace(r, 'gen-pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    _.ends(module, func)
# end


# Выбор винительного падежа
@a.starts(module)
def choose_accusative_forms(func, i):  # export
    p = i.parts  # local
    r = i.result  # local

    if i.calc_sg:
        r['acc-sg-in'] = ''  # todo: remove this?
        r['acc-sg-an'] = ''

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
            if i.stem.type == '8-third':
                r['acc-sg'] = r['nom-sg']
            else:
                r['acc-sg'] = p.stems['acc-sg'] + p.endings['acc-sg']  # todo: don't use `parts` here?
            # end
        elif i.gender == 'n':
            r['acc-sg'] = r['nom-sg']
        # end
    # end

    if i.calc_pl:
        r['acc-pl-in'] = ''  # todo: remove this?
        r['acc-pl-an'] = ''

        if i.animacy == 'in':
            r['acc-pl'] = r['nom-pl']
        elif i.animacy == 'an':
            r['acc-pl'] = r['gen-pl']
        else:
            r['acc-pl-in'] = r['nom-pl']
            r['acc-pl-an'] = r['gen-pl']
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def second_ins_case(func, i):  # export
    r = i.result  # local

    # Второй творительный
    if i.gender == 'f' and i.calc_sg:
        ins_sg2 = _.replaced(r['ins-sg'], 'й$', 'ю')  # local
        if ins_sg2 != r['ins-sg']:
            _.log_info('Замена "й" на "ю" для второго творительного женского рода')
            r['ins-sg2'] = ins_sg2
        # end
    # end

    _.ends(module, func)
# end


# return export
