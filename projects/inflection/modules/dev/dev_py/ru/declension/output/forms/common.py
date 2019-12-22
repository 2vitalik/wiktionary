from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...output.forms import noun as noun_forms
from ...output.forms import adj as adj_forms


module = 'output.forms.common'  # local


@a.call(module)
def init_forms(info, stems, endings):  # Генерация словоформ
    info.out_args['nom_sg'] = stems['nom_sg'] + endings['nom_sg']
    info.out_args['gen_sg'] = stems['gen_sg'] + endings['gen_sg']
    info.out_args['dat_sg'] = stems['dat_sg'] + endings['dat_sg']
    info.out_args['acc_sg'] = ''
    info.out_args['ins_sg'] = stems['ins_sg'] + endings['ins_sg']
    info.out_args['prp_sg'] = stems['prp_sg'] + endings['prp_sg']
    info.out_args['nom_pl'] = stems['nom_pl'] + endings['nom_pl']
    info.out_args['gen_pl'] = stems['gen_pl'] + endings['gen_pl']
    info.out_args['dat_pl'] = stems['dat_pl'] + endings['dat_pl']
    info.out_args['acc_pl'] = ''
    info.out_args['ins_pl'] = stems['ins_pl'] + endings['ins_pl']
    info.out_args['prp_pl'] = stems['prp_pl'] + endings['prp_pl']

    # TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
# end


@a.starts(module)
def init_srt_forms(func, out_args, stems, endings):
    out_args['srt_sg'] = stems['srt_sg'] + endings['srt_sg']
    out_args['srt_pl'] = stems['srt_pl'] + endings['srt_pl']
    _.ends(module, func)
# end


@a.starts(module)
def fix_stress(func, out_args):
    # Add stress if there is no one
    if _.contains_several(out_args['nom_sg'], '{vowel}') and not _.contains(out_args['nom_sg'], '[́ ё]'):
        # perhaps this is redundant for nom_sg?
        _.replace(out_args, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if _.contains_several(out_args['gen_pl'], '{vowel+ё}') and not _.contains(out_args['gen_pl'], '[́ ё]'):
        _.replace(out_args, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    _.ends(module, func)
# end


# Выбор винительного падежа
@a.starts(module)
def choose_accusative_forms(func, info):
    out_args = info.out_args  # local
    data = info.data  # local

    out_args['acc_sg_in'] = ''
    out_args['acc_sg_an'] = ''
    out_args['acc_pl_in'] = ''
    out_args['acc_pl_an'] = ''

    if info.gender == 'm' or (info.gender == 'n' and info.output_gender == 'm'):
        if info.animacy == 'in':
            out_args['acc_sg'] = out_args['nom_sg']
        elif info.animacy == 'an':
            out_args['acc_sg'] = out_args['gen_sg']
        else:
            out_args['acc_sg_in'] = out_args['nom_sg']
            out_args['acc_sg_an'] = out_args['gen_sg']
        # end
    elif info.gender == 'f':
        if _.equals(info.stem.type, ['f-3rd', 'f-3rd-sibilant']):
            out_args['acc_sg'] = out_args['nom_sg']
        else:
            out_args['acc_sg'] = data.stems['acc_sg'] + data.endings['acc_sg']  # todo: don't use `data` here?
        # end
    elif info.gender == 'n':
        out_args['acc_sg'] = out_args['nom_sg']
    # end

    if info.animacy == 'in':
        out_args['acc_pl'] = out_args['nom_pl']
    elif info.animacy == 'an':
        out_args['acc_pl'] = out_args['gen_pl']
    else:
        out_args['acc_pl_in'] = out_args['nom_pl']
        out_args['acc_pl_an'] = out_args['gen_pl']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def second_ins_case(func, out_args, gender):
    # local ins_sg2

    # Второй творительный
    if gender == 'f':
        ins_sg2 = _.replaced(out_args['ins_sg'], 'й$', 'ю')
        if ins_sg2 != out_args['ins_sg']:
            out_args['ins_sg2'] = ins_sg2
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def generate_out_args(func, info):  # export
    # local keys

    init_forms(info, info.data.stems, info.data.endings)
    if info.adj:
        init_srt_forms(info.out_args, info.data.stems, info.data.endings)
        if _.contains(info.rest_index, ['⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)']):
            info.out_args['краткая'] = '⊠'
        elif _.contains(info.rest_index, ['✕', '×', 'x', 'х', 'X', 'Х']):
            info.out_args['краткая'] = '✕'
        elif _.contains(info.rest_index, ['%-', '—', '−']):
            info.out_args['краткая'] = '−'
        else:
            info.out_args['краткая'] = '1'
        # end
    # end

    fix_stress(info.out_args)

    for key, value in info.out_args.items():
        # replace 'ё' with 'е' when unstressed
        # if _.contains_once(info.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(info.rest_index, 'ё'):  -- trying to bug-fix
        if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(info.rest_index, 'ё'):
            if info.adj and _.contains(info.stress_type, "a'") and info.gender == 'f' and key == 'srt_sg':
                info.out_args[key] = _.replaced(value, 'ё', 'е') + ' // ' + _.replaced(value, '́', '')
            else:
                info.out_args[key] = _.replaced(value, 'ё', 'е')  # обычный случай
            # end
        # end
    # end

    if info.noun:
        noun_forms.apply_obelus(info.out_args, info.rest_index)
    # end

    choose_accusative_forms(info)

    second_ins_case(info.out_args, info.gender)

    if info.noun:
        noun_forms.apply_specific_3(info.out_args, info.gender, info.rest_index)
    # end

    if info.adj:
        adj_forms.add_comparative(info.out_args, info.rest_index, info.stress_type, info.stem.type, info.stem)
    # end

    for key, value in info.out_args.items():
#        INFO Удаляем ударение, если только один слог:
        info.out_args[key] = noun_forms.remove_stress_if_one_syllable(value)
    # end

    if info.adj:
        if info.postfix:
            keys = [
                'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
                'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
            ]  # list
            for i, key in enumerate(keys):
                info.out_args[key] = info.out_args[key] + 'ся'
            # end
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def join_forms(func, out_args_1, out_args_2):  # export  # todo: rename to `out_args`
    # local keys, out_args, delim

    keys = [
        'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
        'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
        'nom_sg_m', 'gen_sg_m', 'dat_sg_m', 'acc_sg_m', 'ins_sg_m', 'prp_sg_m',
        'nom_sg_n', 'gen_sg_n', 'dat_sg_n', 'acc_sg_n', 'ins_sg_n', 'prp_sg_n',
        'nom_sg_f', 'gen_sg_f', 'dat_sg_f', 'acc_sg_f', 'ins_sg_f', 'prp_sg_f',
        'srt_sg',  'srt_sg_m',  'srt_sg_n',  'srt_sg_f',  'srt_pl',
        'acc_sg_m_a', 'acc_sg_m_n', 'acc_pl_a', 'acc_pl_n',
        'ins_sg2',
        'ins_sg2_f',
        'зализняк1', 'зализняк',
        'error',
    ]  # list

    out_args = out_args_1
    out_args['зализняк-1'] = out_args_1['зализняк']
    out_args['зализняк-2'] = out_args_2['зализняк']
    for i, key in enumerate(keys):
        if not _.has_key(out_args, key) and not _.has_key(out_args_2, key):
            pass
        elif not _.has_key(out_args, key) and _.has_key(out_args_2, key):  # INFO: Если out_args[key] == None
            out_args[key] = out_args_2[key]
        elif out_args[key] != out_args_2[key] and out_args_2[key]:
            delim = '<br/>'
            if _.equals(key, ['зализняк1', 'зализняк']):
                delim = '&nbsp;'
            # end
            # TODO: <br/> только для падежей
            out_args[key] = out_args[key] + '&nbsp;//' + delim + out_args_2[key]
        # end
        if not _.has_key(out_args, key) or not out_args[key]:  # INFO: Если out_args[key] == None
            out_args[key] = ''
        # end
    # end

    _.ends(module, func)
    return out_args
# end


@a.starts(module)
def plus_forms(func, sub_forms):  # export  # todo: rename to `out_args`
    # local keys, out_args, delim

    keys = [
        'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
        'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
        # 'ins_sg2',
        'зализняк1', 'зализняк',
        'error',
    ]  # list
    out_args = sub_forms[0]  # todo: rename to `out_args`
    for i, forms2 in enumerate(sub_forms):  # todo: rename to `out_args`
        if i != 1:
            for j, key in enumerate(keys):
                if not out_args[key] and forms2[key]:  # INFO: Если out_args[key] == None
                    out_args[key] = forms2[key]
                elif out_args[key] != forms2[key] and forms2[key]:
                    delim = '-'
                    if _.equals(key, ['зализняк1', 'зализняк']):
                        delim = ' + '
                    # end
                    out_args[key] = out_args[key] + delim + forms2[key]
                # end
                if not out_args[key]:  # INFO: Если out_args[key] == None
                    out_args[key] = ''
                # end
            # end
        # end
    # end

    _.ends(module, func)
    return out_args
# end


# return export
