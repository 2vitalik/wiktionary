from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .declension.init.parse import common as parse
from .declension.init import stress
from .declension.init import endings
from .declension.init import stem_type
from .declension.modify.circles import adj as adj_circles
from .declension.modify import reducable
from .declension.modify import degree
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
def main_sub_algorithm(func, data):
    _.log_info('Вычисление схемы ударения')

    # local stem_stress_schema

    data.stress_schema = stress.get_stress_schema(data.stress_type, data.adj, data.pronoun)

    _.log_table(data.stress_schema['stem'], "data.stress_schema['stem']")
    _.log_table(data.stress_schema['ending'], "data.stress_schema['ending']")

    data.endings = endings.get_endings(data)

    data.stems = dict()  # dict
    stress.apply_stress_type(data)
    _.log_table(data.stems, 'data.stems')
    _.log_table(data.endings, 'data.endings')

    # apply special cases (1) or (2) in index
    if data.adj:
        adj_circles.apply_adj_specific_1_2(data.stems, data.gender, data.rest_index)
    # end

#    # *** для случая с расстановкой ударения  (см. ниже)
#    # local orig_stem = data.stem.unstressed
#    if _.contains(data.rest_index, ['%(2%)', '②']):
#        orig_stem = _.replaced(data.stems['gen_pl'], '́ ', '')  # удаляем ударение для случая "сапожок *d(2)"
#        mw.log('> Another `orig_stem`: ' + str(orig_stem))
#    # end

    # reducable
    data.rest_index = degree.apply_specific_degree(data.stems, data.endings, data.word.unstressed, data.stem.unstressed, data.stem.type, data.gender, data.stress_type, data.rest_index, data)
    reducable.apply_specific_reducable(data.stems, data.endings, data.word.unstressed, data.stem.unstressed, data.stem.type, data.gender, data.stress_type, data.rest_index, data, False)

    if not _.equals(data.stress_type, ["f", "f'"]) and _.contains(data.rest_index, '%*'):
        mw.log('# Обработка случая на препоследний слог основы при чередовании')
        orig_stem = data.stem.unstressed
        if data.forced_stem:
            orig_stem = data.forced_stem
        # end
        for key, stem in data.stems.items():
#            mw.log(' - ' + key + ' -> ' + stem)
#            mw.log('Ударение на основу?')
#            mw.log(data.stress_schema['stem'][key])
            stem_stress_schema = data.stress_schema['stem']
            if not _.contains(stem, '[́ ё]') and _.has_key(stem_stress_schema, key) and stem_stress_schema[key]:
                # *** случай с расстановкой ударения  (см. выше)
                # "Дополнительные правила об ударении", стр. 34
                old_value = data.stems[key]
                # mw.log('> ' + key + ' (old): ' + str(old_value))
                if data.stems[key] != orig_stem:  # попытка обработать наличие беглой гласной (не знаю, сработает ли всегда)
                    data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)({vowel})({consonant}*)$', '%1́ %2%3%4')
                    if not _.contains(data.stems[key], '[́ ё]'): # если предпоследнего слога попросту нет
                        # сделаем хоть последний ударным
                        data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
                    # end
                else:
                    data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
                # end
                # mw.log('> ' + key + ' (new): ' + str(data.stems[key]))
                mw.log('  - ' + key + ': "' + str(old_value) + '" -> "' + str(data.stems[key]) + '"')
            # end
        # end
    # end

    # Специфика по "ё"
    if _.contains(data.rest_index, 'ё') and not _.contains(data.endings['gen_pl'], '{vowel+ё}') and not _.contains(data.stems['gen_pl'], 'ё'):
        data.stems['gen_pl'] = _.replaced(data.stems['gen_pl'], 'е́?([^е]*)$', 'ё%1')
        data.rest_index = data.rest_index + 'ё'  # ???
    # end

    _.ends(module, func)
# end


@a.starts(module)
def main_algorithm(func, data):
    # local error, keys, out_args, orig_stem, for_category, old_value, cases

    _.log_value(data.rest_index, 'data.rest_index')

    # -------------------------------------------------------------------------

    _.log_info('Извлечение информации об ударении')
    data.stress_type, error = stress.extract_stress_type(data.rest_index)

    if error:
        out_args = result.finalize(data, error)
        _.ends(module, func)
        return out_args
    # end

    _.log_value(data.stress_type, 'data.stress_type')

    # INFO: Если ударение не указано:
    if not data.stress_type:

        # INFO: Может быть это просто несклоняемая схема:
        if _.contains(data.rest_index, '^0'):
            keys = [
                'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
                'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
            ]  # list
            out_args = dict()  # dict
            out_args['зализняк'] = '0'
            out_args['скл'] = 'не'
            for i, key in enumerate(keys):
                out_args[key] = data.word.stressed
            # end
            _.ends(module, func)
            return result.finalize(data, out_args)

        # INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
        elif _.has_value(data.rest_index):
            _.ends(module, func)
            return result.finalize(data, dict(error='Нераспознанная часть индекса: ' + data.rest_index))  # b-dict

        # INFO: Если индекса вообще нет, то и формы просто не известны:
        else:
            _.ends(module, func)
            return result.finalize(data, dict())  # b-dict
        # end
    # end

    # INFO: Итак, ударение мы получили.

    # INFO: Добавление ударения для `stem.stressed` (если его не было)
    # INFO: Например, в слове только один слог, или ударение было на окончание
    if not _.contains(data.stem.stressed, '[́ ё]'):  # and not data.absent_stress ??
        if _.equals(data.stress_type, ["f", "f'"]):
            data.stem.stressed = _.replaced(data.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
        elif _.contains(data.rest_index, '%*'):
            pass  # *** поставим ударение ниже, после чередования
        else:
            data.stem.stressed = _.replaced(data.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
        # end
    # end

    _.log_value(data.stem.stressed, 'data.stem.stressed')

    # -------------------------------------------------------------------------

    _.log_info('Определение типа основы')
    data.stem.type, data.stem.base_type = stem_type.get_stem_type(data.stem.unstressed, data.word.unstressed, data.gender, data.adj, data.rest_index)
    _.log_value(data.stem.type, 'data.stem.type')
    _.log_value(data.stem.base_type, 'data.stem.base_type')

    if not data.stem.type:
        _.ends(module, func)
        return result.finalize(data, dict(error='Неизвестный тип основы'))  # b-dict
    # end

    # -------------------------------------------------------------------------

    if data.noun:
        main_sub_algorithm(data)
        out_args = form.generate_forms(data)  # TODO: Rename to `out_args` ?

    elif data.adj:
        out_args = {}
        cases = [
            'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
            'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
            'srt_sg', 'srt_pl',
        ]  # list

        genders = ['', 'm', 'n', 'f']
        for i, gender in enumerate(genders):
            data.gender = gender
            _.log_value(data.gender, 'data.gender')

            main_sub_algorithm(data)

            if gender == '':
                out_args = form.generate_forms(data)  # TODO: Rename to `out_args` ?
            else:
                sub_forms = form.generate_forms(data)
                for i, case in enumerate(cases):
                    key = case + '_' + gender
                    out_args[key] = sub_forms[case]
                # end
                if gender == 'f':
                    out_args['ins_sg2_f'] = sub_forms['ins_sg2']
                # end
            # end
        # end
        out_args['acc_sg_m_a'] = out_args['gen_sg_m']
        out_args['acc_sg_m_n'] = out_args['nom_sg_m']
        out_args['acc_pl_a'] = out_args['gen_pl']
        out_args['acc_pl_n'] = out_args['nom_pl']

        data.gender = ''  # redundant?
    # end

    out_args['зализняк1'] = index.get_zaliznyak(data.stem.type, data.stress_type, data.rest_index)

    for_category = out_args['зализняк1']
    for_category = _.replaced(for_category, '①', '(1)')
    for_category = _.replaced(for_category, '②', '(2)')
    for_category = _.replaced(for_category, '③', '(3)')
    out_args['зализняк'] = for_category

    _.ends(module, func)
    return out_args
# end


@a.starts(module)
def forms(func, base, args, frame):  # export
    # INFO: `base` здесь нигде не используется,
    #  но теоретически может понадобиться для других языков

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
    out_args = dict()  # dict  # local
    if info.variations:
        _.log_info("Случай с вариациями '//'")
        info_1 = info.variations[0]  # local
        info_2 = info.variations[1]  # local
        out_args_1 = main_algorithm(info_1)  # local
        out_args_2 = main_algorithm(info_2)  # local
        out_args = form.join_forms(out_args_1, out_args_2)
    elif info.plus:
        _.log_info("Случай с '+'")
        out_args_plus = []  # list  # local
        for i, sub_info in info.plus.items():
            out_args_plus.append(main_algorithm(sub_info))
        # end
        out_args = form.plus_forms(out_args_plus)
    else:
        _.log_info('Стандартный случай без вариаций')
        out_args = main_algorithm(info)
    # end

    if info.noun:
        noun_forms.special_cases(out_args, args, info.index, info.word.unstressed)
    # end

    result.finalize(info, out_args)

    _.log_table(out_args, "out_args")
    _.ends(module, func)
    return out_args
# end


# return export
