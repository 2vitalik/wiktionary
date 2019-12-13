from projects.inflection.modules.prod.prod_py import additional
from projects.inflection.modules.prod.prod_py import mw
from projects.inflection.modules.prod.prod_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...noun import stress as noun_stress
from ...adj import stress as adj_stress
from ...pronoun import stress as pronoun_stress


def extract_stress_type(rest_index):  # export
    _.log_func('stress', 'extract_stress_type')

    #    OLD: Старая версия кода:
#    # local stress_regexp = "([abcdef][′']?[′']?)"
#    # local stress_regexp2 = '(' + stress_regexp + '.*//.*' + stress_regexp + ')'
#    stress_regexp = '(' + stress_regexp + '(% ?.*))'
#    data.stress_type = _.extract(rest_index, stress_regexp2)
#    if not data.stress_type:
#        data.stress_type = _.extract(rest_index, stress_regexp)
#    # end
    # local stress_type, allowed_stress_types

    # INFO: Извлечение ударения из оставшейся части индекса:
    stress_type = _.extract(rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

    # INFO: Замена особых апострофов в ударении на обычные:
    if stress_type:
        stress_type = _.replaced(stress_type, '′', "'")
    # end

    # INFO: Список допустимых схем ударений:
    allowed_stress_types = {
        'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
        'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
        'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
    }

    # INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
    if stress_type and not _.equals(stress_type, allowed_stress_types):
        return stress_type, dict(error='Ошибка: Неправильная схема ударения: ' + stress_type)  # dict
    # end
    return stress_type, None  # INFO: `None` здесь -- признак, что нет ошибок
# end



def get_stress_schema(stress_type, adj, pronoun):  # export  # Пока не используется
    _.log_func('stress', 'get_stress_schema')

    if adj:
        return adj_stress.get_adj_stress_schema(stress_type)
    elif pronoun:
        return pronoun_stress.get_pronoun_stress_schema(stress_type)
    else:
        return noun_stress.get_noun_stress_schema(stress_type)
    # end
# end


# TODO: вместо "endings" может передавать просто data
def add_stress(endings, case):
    _.log_func('stress', 'add_stress')

    endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
# end


def apply_stress_type(data):  # export
    _.log_func('stress', 'apply_stress_type')

    # If we have "ё" specific
    if _.contains(data.rest_index, 'ё') and data.stem_type != 'n-3rd':  # Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
        data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
    # end

    if data.stress_schema['stem']['sg']:
        data.stems['nom_sg'] = data.stem_stressed
    else:
        data.stems['nom_sg'] = data.stem
        add_stress(data.endings, 'nom_sg')
    # end

    # TODO: Remove redundant duplicated code (with above)
    # If we have "ё" specific
    # _.log_value(data.stem_type, 'data.stem_type')
    # if _.contains(data.rest_index, 'ё') and data.stem_type != 'n-3rd':  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
    #     data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
    # # end

    # TODO: process this individually !!!
    if data.stress_schema['stem']['sg']:
        data.stems['gen_sg'] = data.stem_stressed
        data.stems['dat_sg'] = data.stem_stressed
        data.stems['prp_sg'] = data.stem_stressed
    else:
        data.stems['gen_sg'] = data.stem
        data.stems['dat_sg'] = data.stem
        data.stems['prp_sg'] = data.stem
        add_stress(data.endings, 'gen_sg')
        add_stress(data.endings, 'dat_sg')
        add_stress(data.endings, 'prp_sg')
    # end

    if data.stress_schema['stem']['ins_sg']:
        data.stems['ins_sg'] = data.stem_stressed
    else:
        data.stems['ins_sg'] = data.stem
        add_stress(data.endings, 'ins_sg')
    # end

    if data.gender == 'f':
        if data.stress_schema['stem']['acc_sg']:
            data.stems['acc_sg'] = data.stem_stressed
        else:
            data.stems['acc_sg'] = data.stem
            add_stress(data.endings, 'acc_sg')
        # end
    # end

    if data.stress_schema['stem']['nom_pl']:
        data.stems['nom_pl'] = data.stem_stressed
    else:
        data.stems['nom_pl'] = data.stem
        add_stress(data.endings, 'nom_pl')
    # end

    if data.stress_schema['stem']['pl']:
        data.stems['gen_pl'] = data.stem_stressed
        data.stems['dat_pl'] = data.stem_stressed
        data.stems['ins_pl'] = data.stem_stressed
        data.stems['prp_pl'] = data.stem_stressed
    else:
        data.stems['gen_pl'] = data.stem
        data.stems['dat_pl'] = data.stem
        data.stems['ins_pl'] = data.stem
        data.stems['prp_pl'] = data.stem
        add_stress(data.endings, 'gen_pl')
        add_stress(data.endings, 'dat_pl')
        add_stress(data.endings, 'ins_pl')
        add_stress(data.endings, 'prp_pl')
    # end

    if data.adj:
        data.stems['srt_sg'] = data.stem
        data.stems['srt_pl'] = data.stem

        if data.gender == 'm':
            if not _.contains(data.stem_stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem_stressed изначально?
                _.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
            else:
                data.stems['srt_sg'] = data.stem_stressed
            # end
        elif data.gender == 'n':
            if data.stress_schema['stem']['srt_sg_n']:
                if not _.contains(data.stem_stressed, '[ ́ё]'):  # todo: возможно мы должны также менять stem_stressed изначально?
                    _.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
                else:
                    data.stems['srt_sg'] = data.stem_stressed
                # end
            # end
            if data.stress_schema['ending']['srt_sg_n']:
                add_stress(data.endings, 'srt_sg')
            # end
        elif data.gender == 'f':
            if data.stress_schema['stem']['srt_sg_f']:
                data.stems['srt_sg'] = data.stem_stressed
            # end
            if data.stress_schema['ending']['srt_sg_f']:
                add_stress(data.endings, 'srt_sg')
            # end
        # end

        if data.stress_schema['stem']['srt_pl']:
            data.stems['srt_pl'] = data.stem_stressed
        # end
        if data.stress_schema['ending']['srt_pl']:
            add_stress(data.endings, 'srt_pl')
        # end
    # end
# end


# return export
