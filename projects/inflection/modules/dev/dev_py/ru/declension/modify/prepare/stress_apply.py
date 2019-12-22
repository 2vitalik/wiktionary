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
def apply_stress_type(func, info):  # export
    data = info.data  # local

    # If we have "ё" specific    -- fixme: ???
    if _.contains(info.rest_index, 'ё') and info.stem.type != 'n-3rd':  # Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
        info.stem.stressed = _.replaced(info.stem.stressed, 'е́?([^е]*)$', 'ё%1')
    # end

    if info.stress_schema['stem']['sg']:
        data.stems['nom_sg'] = info.stem.stressed
    else:
        data.stems['nom_sg'] = data.stem.unstressed
        add_stress(info.data.endings, 'nom_sg')
    # end

    # TODO: Remove redundant duplicated code (with above)
    # If we have "ё" specific
    # _.log_value(info.stem.type, 'info.stem.type')
    # if _.contains(info.rest_index, 'ё') and info.stem.type != 'n-3rd':  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
    #     info.stem.stressed = _.replaced(info.stem.stressed, 'е́?([^е]*)$', 'ё%1')
    # # end

    # TODO: process this individually !!!!
    if info.stress_schema['stem']['sg']:
        data.stems['gen_sg'] = info.stem.stressed
        data.stems['dat_sg'] = info.stem.stressed
        data.stems['prp_sg'] = info.stem.stressed
    else:
        data.stems['gen_sg'] = info.stem.unstressed
        data.stems['dat_sg'] = info.stem.unstressed
        data.stems['prp_sg'] = info.stem.unstressed
        add_stress(data.endings, 'gen_sg')
        add_stress(data.endings, 'dat_sg')
        add_stress(data.endings, 'prp_sg')
    # end

    if info.stress_schema['stem']['ins_sg']:
        data.stems['ins_sg'] = info.stem.stressed
    else:
        data.stems['ins_sg'] = info.stem.unstressed
        add_stress(data.endings, 'ins_sg')
    # end

    if info.gender == 'f':
        if info.stress_schema['stem']['acc_sg']:
            data.stems['acc_sg'] = info.stem.stressed
        else:
            data.stems['acc_sg'] = info.stem.unstressed
            add_stress(data.endings, 'acc_sg')
        # end
    # end

    if info.stress_schema['stem']['nom_pl']:
        data.stems['nom_pl'] = info.stem.stressed
    else:
        data.stems['nom_pl'] = info.stem.unstressed
        add_stress(data.endings, 'nom_pl')
    # end

    # TODO: process this individually !!!! and just in the common loop for all cases :)
    if info.stress_schema['stem']['pl']:
        data.stems['gen_pl'] = info.stem.stressed
        data.stems['dat_pl'] = info.stem.stressed
        data.stems['ins_pl'] = info.stem.stressed
        data.stems['prp_pl'] = info.stem.stressed
    else:
        data.stems['gen_pl'] = info.stem.unstressed
        data.stems['dat_pl'] = info.stem.unstressed
        data.stems['ins_pl'] = info.stem.unstressed
        data.stems['prp_pl'] = info.stem.unstressed
        add_stress(data.endings, 'gen_pl')
        add_stress(data.endings, 'dat_pl')
        add_stress(data.endings, 'ins_pl')
        add_stress(data.endings, 'prp_pl')
    # end

    if info.adj:
        data.stems['srt_sg'] = info.stem.unstressed
        data.stems['srt_pl'] = info.stem.unstressed

        if info.gender == 'm':
            if not _.contains(info.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                _.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
            else:
                data.stems['srt_sg'] = info.stem.stressed
            # end
        elif info.gender == 'n':
            if info.stress_schema['stem']['srt_sg_n']:
                if not _.contains(info.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                    _.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
                else:
                    data.stems['srt_sg'] = info.stem.stressed
                # end
            # end
            if info.stress_schema['ending']['srt_sg_n']:
                add_stress(data.endings, 'srt_sg')
            # end
        elif info.gender == 'f':
            if info.stress_schema['stem']['srt_sg_f']:
                data.stems['srt_sg'] = info.stem.stressed
            # end
            if info.stress_schema['ending']['srt_sg_f']:
                add_stress(data.endings, 'srt_sg')
            # end
        # end

        if info.stress_schema['stem']['srt_pl']:
            data.stems['srt_pl'] = info.stem.stressed
        # end
        if info.stress_schema['ending']['srt_pl']:
            add_stress(data.endings, 'srt_pl')
        # end
    # end

    _.ends(module, func)
# end


# return export
