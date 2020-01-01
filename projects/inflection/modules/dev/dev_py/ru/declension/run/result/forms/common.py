from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ....run.result.forms import noun as noun_forms
from ....run.result.forms import adj as adj_forms


module = 'run.result.forms.common'  # local


@a.call(module)
def init_forms(i):  # Генерация словоформ
    r = i.result  # local
    p = i.parts  # local

    r['nom-sg'] = p.stems['nom-sg'] + p.endings['nom-sg']
    r['gen-sg'] = p.stems['gen-sg'] + p.endings['gen-sg']
    r['dat-sg'] = p.stems['dat-sg'] + p.endings['dat-sg']
    r['acc-sg'] = ''
    r['ins-sg'] = p.stems['ins-sg'] + p.endings['ins-sg']
    r['prp-sg'] = p.stems['prp-sg'] + p.endings['prp-sg']
    r['nom-pl'] = p.stems['nom-pl'] + p.endings['nom-pl']
    r['gen-pl'] = p.stems['gen-pl'] + p.endings['gen-pl']
    r['dat-pl'] = p.stems['dat-pl'] + p.endings['dat-pl']
    r['acc-pl'] = ''
    r['ins-pl'] = p.stems['ins-pl'] + p.endings['ins-pl']
    r['prp-pl'] = p.stems['prp-pl'] + p.endings['prp-pl']

    # TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
# end


@a.starts(module)
def init_srt_forms(func, i):  # todo move to `init_forms` (with if i.adj) ?
    p = i.parts  # local
    r = i.result  # local

    r['srt-sg'] = p.stems['srt-sg'] + p.endings['srt-sg']
    r['srt-pl'] = p.stems['srt-pl'] + p.endings['srt-pl']
    _.ends(module, func)
# end


@a.starts(module)
def fix_stress(func, o):
    # Add stress if there is no one
    if _.contains_several(o['nom-sg'], '{vowel}') and not _.contains(o['nom-sg'], '[́ ё]'):
        # perhaps this is redundant for nom-sg?
        _.replace(o, 'nom-sg', '({vowel})({consonant}*)$', '%1́ %2')
    # end
    if _.contains_several(o['gen-pl'], '{vowel+ё}') and not _.contains(o['gen-pl'], '[́ ё]'):
        _.replace(o, 'gen-pl', '({vowel})({consonant}*)$', '%1́ %2')
    # end

    _.ends(module, func)
# end


# Выбор винительного падежа
@a.starts(module)
def choose_accusative_forms(func, i):
    p = i.parts  # local
    r = i.result  # local

    r['acc-sg-in'] = ''
    r['acc-sg-an'] = ''
    r['acc-pl-in'] = ''
    r['acc-pl-an'] = ''

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
        if _.equals(i.stem.type, ['f-3rd', 'f-3rd-sibilant']):
            r['acc-sg'] = r['nom-sg']
        else:
            r['acc-sg'] = p.stems['acc-sg'] + p.endings['acc-sg']  # todo: don't use `data` here?
        # end
    elif i.gender == 'n':
        r['acc-sg'] = r['nom-sg']
    # end

    if i.animacy == 'in':
        r['acc-pl'] = r['nom-pl']
    elif i.animacy == 'an':
        r['acc-pl'] = r['gen-pl']
    else:
        r['acc-pl-in'] = r['nom-pl']
        r['acc-pl-an'] = r['gen-pl']
    # end

    _.ends(module, func)
# end


@a.starts(module)
def second_ins_case(func, i):
    r = i.result  # local

    # Второй творительный
    if i.gender == 'f':
        ins_sg2 = _.replaced(r['ins-sg'], 'й$', 'ю')  # local
        if ins_sg2 != r['ins-sg']:
            r['ins-sg2'] = ins_sg2
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def generate_out_args(func, i):  # export
    r = i.result  # local

    init_forms(i)
    if i.adj:
        init_srt_forms(i)
    # end

    fix_stress(r)

    if i.adj:
        adj_forms.add_comparative(i)
    # end

    for key, value in r.items():
        # replace 'ё' with 'е' when unstressed
        # if _.contains_once(i.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё'):  -- trying to bug-fix
        if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё'):
            if i.adj and _.contains(i.stress_type, "a'") and i.gender == 'f' and key == 'srt-sg':
                r[key] = _.replaced(value, 'ё', 'е') + ' // ' + _.replaced(value, '́', '')
            else:
                r[key] = _.replaced(value, 'ё', 'е')  # обычный случай
            # end
        # end
    # end

    if i.noun:
        noun_forms.apply_obelus(i)
    # end

    choose_accusative_forms(i)

    second_ins_case(i)

    if i.noun:
        noun_forms.apply_specific_3(i)
    # end

    for key, value in r.items():
#        INFO Удаляем ударение, если только один слог:
        r[key] = noun_forms.remove_stress_if_one_syllable(value)
    # end

    if i.adj:
        if i.postfix:
            # local keys
            keys = [
                'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
            ]  # list
            for j, key in enumerate(keys):
                r[key] = r[key] + 'ся'
            # end
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def join_forms(func, out_args_1, out_args_2):  # export  # todo: rename to `out_args`
    # local keys, out_args, delim

    keys = [
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
        'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
        'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
        'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
        'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
        'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
        'ins-sg2',
        'ins-sg2-f',
        'зализняк1', 'зализняк',
        'error',
    ]  # list

    out_args = out_args_1
    out_args['зализняк-1'] = out_args_1['зализняк']
    out_args['зализняк-2'] = out_args_2['зализняк']
    for j, key in enumerate(keys):
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
        'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
        'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
        'ins-sg2',
        'зализняк1', 'зализняк',
        'error',
    ]  # list
    out_args = sub_forms[0]  # todo: rename to `out_args`
    for j, forms2 in enumerate(sub_forms):  # todo: rename to `out_args`
        if j != 0:
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