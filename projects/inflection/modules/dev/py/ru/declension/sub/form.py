from projects.inflection.modules.dev.py import a
from projects.inflection.modules.dev.py import mw
from projects.inflection.modules.dev.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...noun import form as noun_form


module = 'declension.forms'  # local


@a.call(module)
def init_forms(stems, endings):  # Генерация словоформ
    return dict(
        nom_sg = stems['nom_sg'] + endings['nom_sg'],
        gen_sg = stems['gen_sg'] + endings['gen_sg'],
        dat_sg = stems['dat_sg'] + endings['dat_sg'],
        acc_sg = '',
        ins_sg = stems['ins_sg'] + endings['ins_sg'],
        prp_sg = stems['prp_sg'] + endings['prp_sg'],
        nom_pl = stems['nom_pl'] + endings['nom_pl'],
        gen_pl = stems['gen_pl'] + endings['gen_pl'],
        dat_pl = stems['dat_pl'] + endings['dat_pl'],
        acc_pl = '',
        ins_pl = stems['ins_pl'] + endings['ins_pl'],
        prp_pl = stems['prp_pl'] + endings['prp_pl'],
    )  # dict
    # TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
# end


@a.starts(module)
def init_srt_forms(func, forms, stems, endings):
    forms['srt_sg'] = stems['srt_sg'] + endings['srt_sg']
    forms['srt_pl'] = stems['srt_pl'] + endings['srt_pl']
    _.ends(module, func)
# end


@a.starts(module)
def fix_stress(func, forms):
    # Add stress if there is no one
    if _.contains_several(forms['nom_sg'], '{vowel}') and not _.contains(forms['nom_sg'], '[́ ё]'):
        # perhaps this is redundant for nom_sg?
        _.replace(forms, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if _.contains_several(forms['gen_pl'], '{vowel+ё}') and not _.contains(forms['gen_pl'], '[́ ё]'):
        _.replace(forms, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    _.ends(module, func)
# end


# Выбор винительного падежа
@a.starts(module)
def choose_accusative_forms(func, forms, data):
    forms['acc_sg_in'] = ''
    forms['acc_sg_an'] = ''
    forms['acc_pl_in'] = ''
    forms['acc_pl_an'] = ''

    if data.gender == 'm' or (data.gender == 'n' and data.output_gender == 'm'):
        if data.animacy == 'in':
            forms['acc_sg'] = forms['nom_sg']
        elif data.animacy == 'an':
            forms['acc_sg'] = forms['gen_sg']
        else:
            forms['acc_sg_in'] = forms['nom_sg']
            forms['acc_sg_an'] = forms['gen_sg']
        # end
    elif data.gender == 'f':
        if _.equals(data.stem_type, ['f-3rd', 'f-3rd-sibilant']):
            forms['acc_sg'] = forms['nom_sg']
        else:
            forms['acc_sg'] = data.stems['acc_sg'] + data.endings['acc_sg']
        # end
    elif data.gender == 'n':
        forms['acc_sg'] = forms['nom_sg']
    # end

    if data.animacy == 'in':
        forms['acc_pl'] = forms['nom_pl']
    elif data.animacy == 'an':
        forms['acc_pl'] = forms['gen_pl']
    else:
        forms['acc_pl_in'] = forms['nom_pl']
        forms['acc_pl_an'] = forms['gen_pl']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def second_ins_case(func, forms, gender):
    # local ins_sg2

    # Второй творительный
    if gender == 'f':
        ins_sg2 = _.replaced(forms['ins_sg'], 'й$', 'ю')
        if ins_sg2 != forms['ins_sg']:
            forms['ins_sg2'] = ins_sg2
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def generate_forms(func, data):  # export
    # local forms, keys

    forms = init_forms(data.stems, data.endings)
    if data.adj:
        init_srt_forms(forms, data.stems, data.endings)
        if _.contains(data.rest_index, ['×', '⊠', 'x', 'х']):
            forms['краткая'] = ''
        else:
            forms['краткая'] = '1'
        # end
    # end

    fix_stress(forms)

    for key, value in forms.items():
        # replace 'ё' with 'е' when unstressed
        # if _.contains_once(data.stem, 'ё') and _.contains(value, '́ ') and _.contains(data.rest_index, 'ё'):  -- trying to bug-fix
        if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(data.rest_index, 'ё'):
            if data.adj and _.contains(data.stress_type, "a'") and data.gender == 'f' and key == 'srt_sg':
                forms[key] = _.replaced(value, 'ё', 'е') + ' // ' + _.replaced(value, '́', '')
            else:
                forms[key] = _.replaced(value, 'ё', 'е')  # обычный случай
            # end
        # end
    # end

    if data.noun:
        noun_form.apply_obelus(forms, data.rest_index)
    # end

    choose_accusative_forms(forms, data)

    second_ins_case(forms, data.gender)

    if data.noun:
        noun_form.apply_specific_3(forms, data.gender, data.rest_index)
    # end

    for key, value in forms.items():
#        INFO Удаляем ударение, если только один слог:
        forms[key] = noun_form.remove_stress_if_one_syllable(value)
    # end

    if data.adj:
        if data.postfix:
            keys = [
                'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
                'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
            ]  # list
            for i, key in enumerate(keys):
                forms[key] = forms[key] + 'ся'
            # end
        # end
    # end

    _.ends(module, func)
    return forms
# end


@a.starts(module)
def join_forms(func, forms1, forms2):  # export
    # local keys, forms, delim

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

    forms = forms1
    forms['зализняк-1'] = forms1['зализняк']
    forms['зализняк-2'] = forms2['зализняк']
    for i, key in enumerate(keys):
        if not _.has_key(forms, key) and not _.has_key(forms2, key):
            pass
        elif not _.has_key(forms, key) and _.has_key(forms2, key):  # INFO: Если forms[key] == None
            forms[key] = forms2[key]
        elif forms[key] != forms2[key] and forms2[key]:
            delim = '<br/>'
            if _.equals(key, ['зализняк1', 'зализняк']):
                delim = '&nbsp;'
            # end
            # TODO: <br/> только для падежей
            forms[key] = forms[key] + '&nbsp;//' + delim + forms2[key]
        # end
        if not _.has_key(forms, key) or not forms[key]:  # INFO: Если forms[key] == None
            forms[key] = ''
        # end
    # end

    _.ends(module, func)
    return forms
# end


@a.starts(module)
def plus_forms(func, sub_forms):  # export
    # local keys, forms, delim

    keys = [
        'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
        'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
        # 'ins_sg2',
        'зализняк1', 'зализняк',
        'error',
    ]  # list
    forms = sub_forms[0]
    for i, forms2 in enumerate(sub_forms):
        if i != 1:
            for j, key in enumerate(keys):
                if not forms[key] and forms2[key]:  # INFO: Если forms[key] == None
                    forms[key] = forms2[key]
                elif forms[key] != forms2[key] and forms2[key]:
                    delim = '-'
                    if _.equals(key, ['зализняк1', 'зализняк']):
                        delim = ' + '
                    # end
                    forms[key] = forms[key] + delim + forms2[key]
                # end
                if not forms[key]:  # INFO: Если forms[key] == None
                    forms[key] = ''
                # end
            # end
        # end
    # end

    _.ends(module, func)
    return forms
# end


# return export
