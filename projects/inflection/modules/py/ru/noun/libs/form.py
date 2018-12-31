from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


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


def remove_stress_if_one_syllable(value):
    if _.contains_once(value, '{vowel+ё}'):
        return _.replaced(value, '́ ', '')
    # end
    return value
# end


def fix_stress(forms):

    # Add stress if there is no one
    if _.contains_several(forms['nom_sg'], '{vowel}') and not _.contains(forms['nom_sg'], '[́ ё]'):
        # perhaps this is redundant for nom_sg?
        _.replace(forms, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if _.contains_several(forms['gen_pl'], '{vowel+ё}') and not _.contains(forms['gen_pl'], '[́ ё]'):
        _.replace(forms, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    for key, value in forms.items():
#        INFO Удаляем ударение, если только один слог:
        forms[key] = remove_stress_if_one_syllable(value)

        # replace 'ё' with 'е' when unstressed
        if _.contains_once(value, 'ё') and _.contains(value, '́ '):
            forms[key] = _.replaced(value, 'ё', 'е')
        # end
    # end
# end


def apply_obelus(forms, rest_index, frame):
    if _.contains(rest_index, '÷'):
        if frame:
            forms['gen_pl'] = "{{expandTemplate}}"
        else:
            forms['gen_pl'] = '{{incorrect|' + forms['gen_pl'] + '}}'
        # end
        forms['коммент'] = 'образование род. п. мн. ч. затруднительно'
    # end
# end


# Выбор винительного падежа
def choose_accusative_forms(forms, data):
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
# end


def second_ins_case(forms, gender):
    # local ins_sg2

    # Второй творительный
    if gender == 'f':
        ins_sg2 = _.replaced(forms['ins_sg'], 'й$', 'ю')
        if ins_sg2 != forms['ins_sg']:
            forms['ins_sg2'] = ins_sg2
        # end
    # end
# end


def apply_specific_3(forms, gender, rest_index):
    # Специфика по (3)
    if _.contains(rest_index, '%(3%)') or _.contains(rest_index, '③'):
        if _.endswith(forms['prp_sg'], 'и'):
            forms['prp_sg'] = forms['prp_sg'] + ' // ' + _.replaced(forms['prp_sg'], 'и$', 'е')
        # end
        if gender == 'f' and _.endswith(forms['dat_sg'], 'и'):
            forms['dat_sg'] = forms['dat_sg'] + ' // ' + _.replaced(forms['dat_sg'], 'и$', 'е')
        # end
    # end
# end


def generate_forms(data):  # export
    # local forms, keys

    mw.log('> Запуск `generate_forms`')

    forms = init_forms(data.stems, data.endings)

    fix_stress(forms)

    apply_obelus(forms, data.rest_index, data.frame)

    choose_accusative_forms(forms, data)

    second_ins_case(forms, data.gender)

    apply_specific_3(forms, data.gender, data.rest_index)

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

    return forms
# end


#------------------------------------------------------------------------------


def prt_case(forms, args, index):  # Разделительный падеж
    if _.contains(index, 'Р2') or _.contains(index, 'Р₂'):
        forms['prt_sg'] = forms['dat_sg']
    # end
    if _.has_value(args, 'Р'):
        forms['prt_sg'] = args['Р']
    # end
# end


def loc_case(forms, args, index):  # Местный падеж
    # local loc, loc_prep

    if _.contains(index, 'П2') or _.contains(index, 'П₂'):
        loc = forms['dat_sg']
        loc = _.replaced(loc, '́ ', '')
        loc = _.replaced(loc, 'ё', 'е')
        loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
        loc = remove_stress_if_one_syllable(loc)
        forms['loc_sg'] = loc
        loc_prep = '?'
        loc_prep = _.extract(index, 'П2%((.+)%)')
        if not loc_prep:
            loc_prep = _.extract(index, 'П₂%((.+)%)')
        # end
        if not loc_prep:
            loc_prep = 'в, на'
        # end
        forms['loc_sg'] = '(' + loc_prep + ') ' + forms['loc_sg']
        if _.contains(index, '%[П'):
            forms['loc_sg'] = forms['loc_sg'] + ' // ' + forms['prp_sg']
        # end
    # end
    if _.has_value(args, 'М'):
        forms['loc_sg'] = args['М']
    # end
# end


def voc_case(forms, args, index, word):  # Звательный падеж
    if _.has_value(args, 'З'):
        forms['voc_sg'] = args['З']
    elif _.contains(index, 'З'):
        if _.endswith(word, ['а', 'я']):
            forms['voc_sg'] = forms['gen_pl']
        else:
            forms['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
        # end
    # end
# end


def special_cases(forms, args, index, word):  # export
    prt_case(forms, args, index)
    loc_case(forms, args, index)
    voc_case(forms, args, index, word)
# end


#------------------------------------------------------------------------------


def join_forms(forms1, forms2):  # export
    # local keys, forms, delim

    keys = [
        'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
        'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
        'ins_sg2',
        'зализняк1', 'зализняк',
        'error',
    ]  # list

    forms = forms1
    forms['зализняк-1'] = forms1['зализняк']
    forms['зализняк-2'] = forms2['зализняк']
    for i, key in enumerate(keys):
        if not forms[key] and forms2[key]:  # INFO: Если forms[key] == None
            forms[key] = forms2[key]
        elif forms[key] != forms2[key] and forms2[key]:
            delim = '<br/>'
            if _.equals(key, ['зализняк1', 'зализняк']):
                delim = '&nbsp;'
            # end
            # TODO: <br/> только для падежей
            forms[key] = forms[key] + '&nbsp;//' + delim + forms2[key]
        # end
        if not forms[key]:  # INFO: Если forms[key] == None
            forms[key] = ''
        # end
    # end
    return forms
# end


def plus_forms(sub_forms):  # export
    # local keys, forms, delim

    keys = [
        'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
        'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
        'ins_sg2',
        'зализняк1', 'зализняк',
        'error',
    ]  # list
    forms = sub_forms[1]
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
    return forms
# end


# return export
