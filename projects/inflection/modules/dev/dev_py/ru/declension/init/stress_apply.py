from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'init.stress_apply'  # local


# TODO: вместо "endings" может передавать просто data
@a.call(module)
def add_stress(endings, case):
    endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
# end


@a.starts(module)
def apply_stress_type(func, data):  # export
    # If we have "ё" specific
    if _.contains(data.rest_index, 'ё') and data.stem.type != 'n-3rd':  # Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
        data.stem.stressed = _.replaced(data.stem.stressed, 'е́?([^е]*)$', 'ё%1')
    # end

    if data.stress_schema['stem']['sg']:
        data.stems['nom_sg'] = data.stem.stressed
    else:
        data.stems['nom_sg'] = data.stem.unstressed
        add_stress(data.endings, 'nom_sg')
    # end

    # TODO: Remove redundant duplicated code (with above)
    # If we have "ё" specific
    # _.log_value(data.stem.type, 'data.stem.type')
    # if _.contains(data.rest_index, 'ё') and data.stem.type != 'n-3rd':  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
    #     data.stem.stressed = _.replaced(data.stem.stressed, 'е́?([^е]*)$', 'ё%1')
    # # end

    # TODO: process this individually !!!
    if data.stress_schema['stem']['sg']:
        data.stems['gen_sg'] = data.stem.stressed
        data.stems['dat_sg'] = data.stem.stressed
        data.stems['prp_sg'] = data.stem.stressed
    else:
        data.stems['gen_sg'] = data.stem.unstressed
        data.stems['dat_sg'] = data.stem.unstressed
        data.stems['prp_sg'] = data.stem.unstressed
        add_stress(data.endings, 'gen_sg')
        add_stress(data.endings, 'dat_sg')
        add_stress(data.endings, 'prp_sg')
    # end

    if data.stress_schema['stem']['ins_sg']:
        data.stems['ins_sg'] = data.stem.stressed
    else:
        data.stems['ins_sg'] = data.stem.unstressed
        add_stress(data.endings, 'ins_sg')
    # end

    if data.gender == 'f':
        if data.stress_schema['stem']['acc_sg']:
            data.stems['acc_sg'] = data.stem.stressed
        else:
            data.stems['acc_sg'] = data.stem.unstressed
            add_stress(data.endings, 'acc_sg')
        # end
    # end

    if data.stress_schema['stem']['nom_pl']:
        data.stems['nom_pl'] = data.stem.stressed
    else:
        data.stems['nom_pl'] = data.stem.unstressed
        add_stress(data.endings, 'nom_pl')
    # end

    if data.stress_schema['stem']['pl']:
        data.stems['gen_pl'] = data.stem.stressed
        data.stems['dat_pl'] = data.stem.stressed
        data.stems['ins_pl'] = data.stem.stressed
        data.stems['prp_pl'] = data.stem.stressed
    else:
        data.stems['gen_pl'] = data.stem.unstressed
        data.stems['dat_pl'] = data.stem.unstressed
        data.stems['ins_pl'] = data.stem.unstressed
        data.stems['prp_pl'] = data.stem.unstressed
        add_stress(data.endings, 'gen_pl')
        add_stress(data.endings, 'dat_pl')
        add_stress(data.endings, 'ins_pl')
        add_stress(data.endings, 'prp_pl')
    # end

    if data.adj:
        data.stems['srt_sg'] = data.stem.unstressed
        data.stems['srt_pl'] = data.stem.unstressed

        if data.gender == 'm':
            if not _.contains(data.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                _.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
            else:
                data.stems['srt_sg'] = data.stem.stressed
            # end
        elif data.gender == 'n':
            if data.stress_schema['stem']['srt_sg_n']:
                if not _.contains(data.stem.stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem.stressed изначально?
                    _.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
                else:
                    data.stems['srt_sg'] = data.stem.stressed
                # end
            # end
            if data.stress_schema['ending']['srt_sg_n']:
                add_stress(data.endings, 'srt_sg')
            # end
        elif data.gender == 'f':
            if data.stress_schema['stem']['srt_sg_f']:
                data.stems['srt_sg'] = data.stem.stressed
            # end
            if data.stress_schema['ending']['srt_sg_f']:
                add_stress(data.endings, 'srt_sg')
            # end
        # end

        if data.stress_schema['stem']['srt_pl']:
            data.stems['srt_pl'] = data.stem.stressed
        # end
        if data.stress_schema['ending']['srt_pl']:
            add_stress(data.endings, 'srt_pl')
        # end
    # end

    _.ends(module, func)
# end


# return export
