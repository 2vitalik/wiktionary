from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .declension.init.parse import common as parse
from .declension import _modify as m
from .declension.output import result
from .declension.output.forms import common as form
from .declension.output.forms import noun as noun_forms
from .declension.output import index

module = 'declension'  # local


def prepare_stash():
    _.clear_stash()
    _.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
    _.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
    _.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
# end


@a.starts(module)
def main_algorithm(func, info):
    # local error, keys, out_args, orig_stem, for_category, old_value, cases

    # todo: Инициализировать `forms` прямо здесь, чтобы не вызывать потом постоянно finalize...

    # ... = extract_stress_type(...)
    # if error:
    #     out_args = result.finalize(info, error)
    #     _.ends(module, func)
    #     return out_args
    # # end

    # INFO: Если ударение не указано:
    if not info.stress_type:

        # INFO: Может быть это просто несклоняемая схема:
        if _.contains(info.rest_index, '^0'):  # todo: put this somewhere upper? before checking stress? or inside sub-algorithm?
            keys = [
                'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
            ]  # list
            out_args = dict()  # dict
            out_args['зализняк'] = '0'
            out_args['скл'] = 'не'
            for i, key in enumerate(keys):
                out_args[key] = info.word.stressed
            # end
            _.ends(module, func)
            return result.finalize(info, out_args)

        # INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
        elif _.has_value(info.rest_index):
            _.ends(module, func)
            return result.finalize(info, dict(error='Нераспознанная часть индекса: ' + info.rest_index))  # b-dict

        # INFO: Если индекса вообще нет, то и формы просто не известны:
        else:  # todo: put this somewhere upper?
            _.ends(module, func)
            return result.finalize(info, dict())  # b-dict
        # end
    # end

    # INFO: Итак, ударение мы получили.

    # INFO: Добавление ударения для `stem.stressed` (если его не было)
    # INFO: Например, в слове только один слог, или ударение было на окончание
    if not _.contains(info.stem.stressed, '[́ ё]'):  # and not info.absent_stress ??
        if _.equals(info.stress_type, ["f", "f'"]):
            info.stem.stressed = _.replaced(info.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
        elif _.contains(info.rest_index, '%*'):
            pass  # *** поставим ударение ниже, после чередования
        else:
            info.stem.stressed = _.replaced(info.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
        # end
    # end

    _.log_value(info.stem.stressed, 'info.stem.stressed')

    # -------------------------------------------------------------------------

    # fixme: Здесь раньше было определение типа основы

    if not info.stem.type:
        _.ends(module, func)
        return result.finalize(info, dict(error='Неизвестный тип основы'))  # b-dict
    # end

    # -------------------------------------------------------------------------

    # todo: `main_algo` will have only further lines?

    if info.noun:
        m.modify(info)
        form.generate_out_args(info)

    elif info.adj:
        cases = [
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
            'srt-sg', 'srt-pl',
        ]  # list

        genders = ['m', 'n', 'f', '']  # plural (without gender) should be last one?
        for i, gender in enumerate(genders):
            # todo: copy info?
            info.gender = gender
            _.log_value(info.gender, 'info.gender')

            m.modify(info)

            if gender == '':  # todo: move all this logic inside `generate_out_args` ?
                form.generate_out_args(info)
            else:
                form.generate_out_args(info)
                for i, case in enumerate(cases):
                    key = case + '-' + gender
                    info.out_args[key] = info.out_args[case]
                # end
                if gender == 'f':
                    info.out_args['ins-sg2-f'] = info.out_args['ins-sg2']
                # end
            # end
        # end

        info.out_args['acc-sg-m-a'] = info.out_args['gen-sg-m']
        info.out_args['acc-sg-m-n'] = info.out_args['nom-sg-m']
        info.out_args['acc-pl-a'] = info.out_args['gen-pl']
        info.out_args['acc-pl-n'] = info.out_args['nom-pl']

        info.gender = ''  # redundant?
    # end

    info.out_args['зализняк1'] = index.get_zaliznyak(info.stem.type, info.stress_type, info.rest_index)

    for_category = info.out_args['зализняк1']
    for_category = _.replaced(for_category, '①', '(1)')
    for_category = _.replaced(for_category, '②', '(2)')
    for_category = _.replaced(for_category, '③', '(3)')
    info.out_args['зализняк'] = for_category

    _.ends(module, func)
# end


@a.starts(module)
def forms(func, base, args, frame):  # export  # todo: rename to `out_args`
    # todo: move this to another place?
    mw.log('=================================================================')

    prepare_stash()  # INFO: Заполняем шаблоны для регулярок

    # INFO: Достаём всю информацию из аргументов (args):
    #   основа, род, одушевлённость и т.п.
    # local info, error
    info, error = parse.parse(base, args)
    if error:
        out_args = result.finalize(info, error)
        _.ends(module, func)
        return out_args
    # end

    info.frame = frame

    # INFO: Запуск основного алгоритма и получение результирующих словоформ:
    if info.variations:
        _.log_info("Случай с вариациями '//'")
        info_1 = info.variations[0]  # local
        info_2 = info.variations[1]  # local
        # todo: ... = o.output(m.modify(info_1))
        main_algorithm(info_1)
        main_algorithm(info_2)
        info.out_args = form.join_forms(info_1.out_args, info_2.out_args)
    elif info.plus:
        _.log_info("Случай с '+'")
        out_args_plus = []  # list  # local
        for i, sub_info in enumerate(info.plus):
            main_algorithm(sub_info)
            out_args_plus.append(sub_info.out_args)
        # end
        info.out_args = form.plus_forms(out_args_plus)
    else:
        _.log_info('Стандартный случай без вариаций')
        main_algorithm(info)
    # end

    if info.noun:
        noun_forms.special_cases(info.out_args, args, info.index, info.word.unstressed)
    # end

    result.finalize(info, info.out_args)
    # todo: put `forward_args` here instead of `finalize`

    _.log_table(info.out_args, "info.out_args")
    _.ends(module, func)
    return info.out_args
# end


# return export
