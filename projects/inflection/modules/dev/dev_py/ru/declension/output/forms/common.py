from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...output.forms import noun as noun_forms
from ...output.forms import adj as adj_forms


module = 'output.forms.common'  # local


@a.call(module)
def init_forms(i):  # Генерация словоформ
    o = i.out_args  # local
    d = i.data  # local

    o['nom_sg'] = d.stems['nom_sg'] + d.endings['nom_sg']
    o['gen_sg'] = d.stems['gen_sg'] + d.endings['gen_sg']
    o['dat_sg'] = d.stems['dat_sg'] + d.endings['dat_sg']
    o['acc_sg'] = ''
    o['ins_sg'] = d.stems['ins_sg'] + d.endings['ins_sg']
    o['prp_sg'] = d.stems['prp_sg'] + d.endings['prp_sg']
    o['nom_pl'] = d.stems['nom_pl'] + d.endings['nom_pl']
    o['gen_pl'] = d.stems['gen_pl'] + d.endings['gen_pl']
    o['dat_pl'] = d.stems['dat_pl'] + d.endings['dat_pl']
    o['acc_pl'] = ''
    o['ins_pl'] = d.stems['ins_pl'] + d.endings['ins_pl']
    o['prp_pl'] = d.stems['prp_pl'] + d.endings['prp_pl']

    # TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
# end


@a.starts(module)
def init_srt_forms(func, o, stems, endings):  # todo move to `init_forms` (with if i.adj) ?
    o['srt_sg'] = stems['srt_sg'] + endings['srt_sg']
    o['srt_pl'] = stems['srt_pl'] + endings['srt_pl']
    _.ends(module, func)
# end


@a.starts(module)
def fix_stress(func, o):
    # Add stress if there is no one
    if _.contains_several(o['nom_sg'], '{vowel}') and not _.contains(o['nom_sg'], '[́ ё]'):
        # perhaps this is redundant for nom_sg?
        _.replace(o, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if _.contains_several(o['gen_pl'], '{vowel+ё}') and not _.contains(o['gen_pl'], '[́ ё]'):
        _.replace(o, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    _.ends(module, func)
# end


# Выбор винительного падежа
@a.starts(module)
def choose_accusative_forms(func, i):
    o = i.out_args  # local
    d = i.data  # local

    o['acc_sg_in'] = ''
    o['acc_sg_an'] = ''
    o['acc_pl_in'] = ''
    o['acc_pl_an'] = ''

    if i.gender == 'm' or (i.gender == 'n' and i.output_gender == 'm'):
        if i.animacy == 'in':
            o['acc_sg'] = o['nom_sg']
        elif i.animacy == 'an':
            o['acc_sg'] = o['gen_sg']
        else:
            o['acc_sg_in'] = o['nom_sg']
            o['acc_sg_an'] = o['gen_sg']
        # end
    elif i.gender == 'f':
        if _.equals(i.stem.type, ['f-3rd', 'f-3rd-sibilant']):
            o['acc_sg'] = o['nom_sg']
        else:
            o['acc_sg'] = d.stems['acc_sg'] + d.endings['acc_sg']  # todo: don't use `data` here?
        # end
    elif i.gender == 'n':
        o['acc_sg'] = o['nom_sg']
    # end

    if i.animacy == 'in':
        o['acc_pl'] = o['nom_pl']
    elif i.animacy == 'an':
        o['acc_pl'] = o['gen_pl']
    else:
        o['acc_pl_in'] = o['nom_pl']
        o['acc_pl_an'] = o['gen_pl']
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
def generate_out_args(func, i):  # export
    o = i.out_args  # local

    init_forms(i)
    if i.adj:
        init_srt_forms(o, i.data.stems, i.data.endings)
        if _.contains(i.rest_index, ['⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)']):
            o['краткая'] = '⊠'
        elif _.contains(i.rest_index, ['✕', '×', 'x', 'х', 'X', 'Х']):
            o['краткая'] = '✕'
        elif _.contains(i.rest_index, ['%-', '—', '−']):
            o['краткая'] = '−'
        else:
            o['краткая'] = '1'
        # end
    # end

    fix_stress(o)

    for key, value in o.items():
        # replace 'ё' with 'е' when unstressed
        # if _.contains_once(info.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(info.rest_index, 'ё'):  -- trying to bug-fix
        if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё'):
            if i.adj and _.contains(i.stress_type, "a'") and i.gender == 'f' and key == 'srt_sg':
                o[key] = _.replaced(value, 'ё', 'е') + ' // ' + _.replaced(value, '́', '')
            else:
                o[key] = _.replaced(value, 'ё', 'е')  # обычный случай
            # end
        # end
    # end

    if i.noun:
        noun_forms.apply_obelus(o, i.rest_index)
    # end

    choose_accusative_forms(i)

    second_ins_case(o, i.gender)

    if i.noun:
        noun_forms.apply_specific_3(o, i.gender, i.rest_index)
    # end

    if i.adj:
        adj_forms.add_comparative(o, i.rest_index, i.stress_type, i.stem.type, i.stem)
    # end

    for key, value in o.items():
#        INFO Удаляем ударение, если только один слог:
        o[key] = noun_forms.remove_stress_if_one_syllable(value)
    # end

    if i.adj:
        if i.postfix:
            # local keys
            keys = [
                'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
                'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
            ]  # list
            for j, key in enumerate(keys):
                o[key] = o[key] + 'ся'
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
