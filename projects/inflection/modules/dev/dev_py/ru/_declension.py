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
from .declension.output import result as r

module = 'declension'  # local


def prepare_stash():  # todo rename to `prepare_regexp_templates` or patterns
    _.clear_stash()
    _.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
    _.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
    _.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
# end


@a.starts(module)
def main_algorithm(func, i):
    o = i.out_args  # local

    # INFO: Если ударение не указано:
    if not i.stress_type:

        # INFO: Может быть это просто несклоняемая схема:
        if _.contains(i.rest_index, '^0'):  # todo: put this somewhere upper? before checking stress? or inside sub-algorithm?
            # local keys
            keys = [
                'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
                'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
            ]  # list
            o['зализняк'] = '0'
            o['скл'] = 'не'
            for j, key in enumerate(keys):
                o[key] = i.word.stressed
            # end
            return _.ends(module, func)

        # INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
        elif _.has_value(i.rest_index):
            r.add_error(i, 'Нераспознанная часть индекса: ' + i.rest_index)
            return _.ends(module, func)

        # INFO: Если индекса вообще нет, то и формы просто не известны:
        else:  # todo: put this somewhere upper?
            return _.ends(module, func)
        # end
    # end

    # INFO: Итак, ударение мы получили.

    # INFO: Добавление ударения для `stem.stressed` (если его не было)
    # INFO: Например, в слове только один слог, или ударение было на окончание
    if not _.contains(i.stem.stressed, '[́ ё]'):  # and not info.absent_stress ??
        if _.equals(i.stress_type, ["f", "f'"]):
            i.stem.stressed = _.replaced(i.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
        elif _.contains(i.rest_index, '%*'):
            pass  # *** поставим ударение ниже, после чередования
        else:
            i.stem.stressed = _.replaced(i.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
        # end
    # end

    _.log_value(i.stem.stressed, 'info.stem.stressed')

    # -------------------------------------------------------------------------

    # fixme: Здесь раньше было определение типа основы

    if not i.stem.type:
        r.add_error(i, 'Неизвестный тип основы')
        return _.ends(module, func)
    # end

    # -------------------------------------------------------------------------

    # todo: `main_algo` will have only further lines?

    if i.noun:
        m.modify(i)
        form.generate_out_args(i)

    elif i.adj:
        # local cases
        cases = [
            'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
            'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
            'srt-sg', 'srt-pl',
        ]  # list

        genders = ['m', 'n', 'f', '']  # plural (without gender) should be last one?
        for j, gender in enumerate(genders):
            # todo: copy info?
            i.gender = gender
            _.log_value(i.gender, 'info.gender')

            m.modify(i)

            if gender == '':  # todo: move all this logic inside `generate_out_args` ?
                form.generate_out_args(i)
            else:
                form.generate_out_args(i)
                for c, case in enumerate(cases):
                    key = case + '-' + gender
                    o[key] = o[case]
                # end
                if gender == 'f':
                    o['ins-sg2-f'] = o['ins-sg2']
                # end
            # end
        # end

        o['acc-sg-m-a'] = o['gen-sg-m']
        o['acc-sg-m-n'] = o['nom-sg-m']
        o['acc-pl-a'] = o['gen-pl']
        o['acc-pl-n'] = o['nom-pl']

        i.gender = ''  # redundant?
    # end

    o['зализняк1'] = index.get_zaliznyak(i)

    value = o['зализняк1']  # local  # for category
    value = _.replaced(value, '①', '(1)')
    value = _.replaced(value, '②', '(2)')
    value = _.replaced(value, '③', '(3)')
    o['зализняк'] = value

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
        noun_forms.special_cases(info)
    # end

    result.forward_args(info)

    _.log_table(info.out_args, "info.out_args")
    _.ends(module, func)
    return info.out_args
# end


# return export
