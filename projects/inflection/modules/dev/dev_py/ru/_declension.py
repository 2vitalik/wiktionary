from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .declension.init.parse import common as parse
from .declension import _modify as m
from .declension.output import result
from .declension.output.forms import common as form
from .declension.output.forms import noun as noun_forms
from .declension.output import result as r

module = 'declension'  # local


def prepare_stash():  # todo rename to `prepare_regexp_templates` or patterns
    _.clear_stash()
    _.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
    _.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
    _.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
# end


@a.starts(module)
def run_gender(func, i):
    o = i.out_args  # local

    if _.startswith(i.rest_index, '0'):
        # todo: move to special function
        # local keys
        keys = [
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
        ]  # list
        for j, key in enumerate(keys):
            o[key] = i.word.stressed
        # end
        return _.ends(module, func)
    # end

    m.modify(i)
    form.generate_out_args(i)

    if i.adj:
        # todo: move to special function
        if i.gender != '':
            # local cases
            cases = [
                'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
                'srt-sg', 'srt-pl',
            ]  # list

            for c, case in enumerate(cases):
                key = case + '-' + i.gender
                o[key] = o[case]
            # end
            if i.gender == 'f':
                o['ins-sg2-f'] = o['ins-sg2']
            # end
        # end

        if i.gender == 'm':
            o['acc-sg-m-a'] = o['gen-sg-m']
            o['acc-sg-m-n'] = o['nom-sg-m']
        elif i.gender == '':
            o['acc-pl-a'] = o['gen-pl']
            o['acc-pl-n'] = o['nom-pl']
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def run_info(func, i):  # todo rename to `run_info`
    if not i.has_index:
        return
    # end

    if i.noun:
        run_gender(i)
    elif i.adj:
        genders = ['m', 'n', 'f', '']  # plural (without gender) should be last one?
        for j, gender in enumerate(genders):
            # todo: copy info?
            i.gender = gender
            _.log_value(i.gender, 'info.gender')
            run_gender(i)
        # end
    # end

    _.ends(module, func)
# end


@a.starts(module)
def forms(func, base, args, frame):  # export  # todo: rename to `out_args`

    # todo: move this to another place?
    mw.log('=================================================================')

    prepare_stash()  # INFO: Заполняем шаблоны для регулярок

    # INFO: Достаём всю информацию из аргументов (args):
    #   основа, род, одушевлённость и т.п.
    info = parse.parse(base, args)  # local
    if r.has_error(info):
        _.ends(module, func)
        return info.out_args
    # end

    info.frame = frame  # todo: move to `parse`

    # INFO: Запуск основного алгоритма и получение результирующих словоформ:
    # todo: move this `if` block inside `run_info` and run it recursively :)
    if info.variations:
        _.log_info("Случай с вариациями '//'")
        info_1 = info.variations[0]  # local
        info_2 = info.variations[1]  # local
        # todo: ... = o.output(m.modify(info_1))
        run_info(info_1)
        run_info(info_2)
        info.out_args = form.join_forms(info_1.out_args, info_2.out_args)
        # todo: form.join_variations()
        # todo: check for errors inside variations
    elif info.plus:
        _.log_info("Случай с '+'")
        out_args_plus = []  # list  # local
        for i, sub_info in enumerate(info.plus):
            run_info(sub_info)
            out_args_plus.append(sub_info.out_args)
        # end
        info.out_args = form.plus_forms(out_args_plus)
        # todo: form.plus_out_args()
    else:
        _.log_info('Стандартный случай без вариаций')
        run_info(info)
    # end

    if info.noun:
        noun_forms.special_cases(info)
    # end

    result.forward_args(info)

    _.log_table(info.out_args, "info.out_args")
    _.ends(module, func)
    return info.out_args
# end


# return export
