from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'modify.prepare.stress_apply'  # local


# TODO: вместо "endings" может передавать просто data
@a.call(module)
def add_stress(endings, case):
    endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
# end


@a.starts(module)
def apply_stress_type(func, i):  # export
    d = i.data  # local

    # If we have "ё" specific    -- fixme: ???
    if _.contains(i.rest_index, 'ё') and i.stem.type != 'n-3rd':  # Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
        i.stem.stressed = _.replaced(i.stem.stressed, 'е́?([^е]*)$', 'ё%1')
    # end

    if i.stress_schema['stem']['sg']:
        d.stems['nom_sg'] = i.stem.stressed
    else:
        d.stems['nom_sg'] = i.stem.unstressed
        add_stress(i.data.endings, 'nom_sg')
    # end

    # TODO: Remove redundant duplicated code (with above)
    # If we have "ё" specific
    # _.log_value(info.stem.type, 'info.stem.type')
    # if _.contains(info.rest_index, 'ё') and info.stem.type != 'n-3rd':  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
    #     info.stem.stressed = _.replaced(info.stem.stressed, 'е́?([^е]*)$', 'ё%1')
    # # end

    # TODO: process this individually !!!!
    if i.stress_schema['stem']['sg']:
        d.stems['gen_sg'] = i.stem.stressed
        d.stems['dat_sg'] = i.stem.stressed
        d.stems['prp_sg'] = i.stem.stressed
    else:
        d.stems['gen_sg'] = i.stem.unstressed
        d.stems['dat_sg'] = i.stem.unstressed
        d.stems['prp_sg'] = i.stem.unstressed
        add_stress(d.endings, 'gen_sg')
        add_stress(d.endings, 'dat_sg')
        add_stress(d.endings, 'prp_sg')
    # end

    if i.stress_schema['stem']['ins_sg']:
        d.stems['ins_sg'] = i.stem.stressed
    else:
        d.stems['ins_sg'] = i.stem.unstressed
        add_stress(d.endings, 'ins_sg')
    # end

    if i.gender == 'f':
        if i.stress_schema['stem']['acc_sg']:
            d.stems['acc_sg'] = i.stem.stressed
        else:
            d.stems['acc_sg'] = i.stem.unstressed
            add_stress(d.endings, 'acc_sg')
        # end
    # end

    if i.stress_schema['stem']['nom_pl']:
        d.stems['nom_pl'] = i.stem.stressed
    else:
        d.stems['nom_pl'] = i.stem.unstressed
        add_stress(d.endings, 'nom_pl')
    # end

    # TODO: process this individually !!!! and just in the common loop for all cases :)
    if i.stress_schema['stem']['pl']:
        d.stems['gen_pl'] = i.stem.stressed
        d.stems['dat_pl'] = i.stem.stressed
        d.stems['ins_pl'] = i.stem.stressed
        d.stems['prp_pl'] = i.stem.stressed
    else:
        d.stems['gen_pl'] = i.stem.unstressed
        d.stems['dat_pl'] = i.stem.unstressed
        d.stems['ins_pl'] = i.stem.unstressed
        d.stems['prp_pl'] = i.stem.unstressed
        add_stress(d.endings, 'gen_pl')
        add_stress(d.endings, 'dat_pl')
        add_stress(d.endings, 'ins_pl')
        add_stress(d.endings, 'prp_pl')
    # end

    if i.adj:
        d.stems['srt_sg'] = i.stem.unstressed
        d.stems['srt_pl'] = i.stem.unstressed

        if i.gender == 'm':
            if not _.contains(i.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                _.replace(d.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
            else:
                d.stems['srt_sg'] = i.stem.stressed
            # end
        elif i.gender == 'n':
            if i.stress_schema['stem']['srt_sg_n']:
                if not _.contains(i.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                    _.replace(d.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
                else:
                    d.stems['srt_sg'] = i.stem.stressed
                # end
            # end
            if i.stress_schema['ending']['srt_sg_n']:
                add_stress(d.endings, 'srt_sg')
            # end
        elif i.gender == 'f':
            if i.stress_schema['stem']['srt_sg_f']:
                d.stems['srt_sg'] = i.stem.stressed
            # end
            if i.stress_schema['ending']['srt_sg_f']:
                add_stress(d.endings, 'srt_sg')
            # end
        # end

        if i.stress_schema['stem']['srt_pl']:
            d.stems['srt_pl'] = i.stem.stressed
        # end
        if i.stress_schema['ending']['srt_pl']:
            add_stress(d.endings, 'srt_pl')
        # end
    # end

    _.ends(module, func)
# end


# return export
