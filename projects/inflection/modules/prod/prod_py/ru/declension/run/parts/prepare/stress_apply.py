from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.parts.prepare.stress_apply'  # local


# TODO: вместо "endings" может передавать просто data
@a.call(module)
def add_stress(endings, case):
    endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
# end


@a.starts(module)
def apply_stress_type(func, i):  # export
    p = i.parts  # local

    # If we have "ё" specific
    if _.contains(i.rest_index, 'ё'):
        if i.gender == 'n' and i.stem.type == '8-third':
            pass  # fixme: Не уверен насчёт необходимости проверки 'n' и '8-third' здесь, сделал для "время °"
        else:
            i.stem.stressed = _.replaced(i.stem.stressed, 'е́?([^е]*)$', 'ё%1')
        # end
    # end

    sg_cases = ['nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg']  # list  # local
    pl_cases = ['nom-pl', 'gen-pl', 'dat-pl', 'ins-pl', 'prp-pl']  # list  # local

    if i.calc_sg:
        for j, case in enumerate(sg_cases):
            if i.stress_schema['stem'][case]:
                p.stems[case] = i.stem.stressed
            else:
                p.stems[case] = i.stem.unstressed
                add_stress(p.endings, case)
            # end
        # end

        if i.gender == 'f':
            if i.stress_schema['stem']['acc-sg']:
                p.stems['acc-sg'] = i.stem.stressed
            else:
                p.stems['acc-sg'] = i.stem.unstressed
                add_stress(p.endings, 'acc-sg')
            # end
        # end
    # end

    if i.calc_pl:
        for j, case in enumerate(pl_cases):
            if i.stress_schema['stem'][case]:
                p.stems[case] = i.stem.stressed
            else:
                p.stems[case] = i.stem.unstressed
                add_stress(p.endings, case)
            # end
        # end
    # end

    if i.adj:
        if i.calc_sg:
            p.stems['srt-sg'] = i.stem.unstressed

            if i.gender == 'm':
                if not _.contains(i.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                    _.replace(p.stems, 'srt-sg', '({vowel})({consonant}*)$', '%1́ %2')
                else:
                    p.stems['srt-sg'] = i.stem.stressed
                # end
            elif i.gender == 'n':
                if i.stress_schema['stem']['srt-sg-n']:
                    if not _.contains(i.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                        _.replace(p.stems, 'srt-sg', '({vowel})({consonant}*)$', '%1́ %2')
                    else:
                        p.stems['srt-sg'] = i.stem.stressed
                    # end
                # end
                if i.stress_schema['ending']['srt-sg-n']:
                    add_stress(p.endings, 'srt-sg')
                # end
            elif i.gender == 'f':
                if i.stress_schema['stem']['srt-sg-f']:
                    p.stems['srt-sg'] = i.stem.stressed
                # end
                if i.stress_schema['ending']['srt-sg-f']:
                    add_stress(p.endings, 'srt-sg')
                # end
            # end
        # end

        if i.calc_pl:
            p.stems['srt-pl'] = i.stem.unstressed

            if i.stress_schema['stem']['srt-pl']:
                p.stems['srt-pl'] = i.stem.stressed
            # end
            if i.stress_schema['ending']['srt-pl']:
                add_stress(p.endings, 'srt-pl')
            # end
        # end
    # end

    _.ends(module, func)
# end


# return export
