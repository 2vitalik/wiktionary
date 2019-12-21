from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ..modify.transform import degree as degree
from ..modify.transform import reducable as reducable
from ..modify.transform.circles import adj as adj_circles


module = 'modify.transform'  # local


@a.starts(module)
def transform(func, data):  # export
    # local stem_stress_schema

    # apply special cases (1) or (2) in index
    if data.adj:
        adj_circles.apply_adj_specific_1_2(data.stems, data.gender, data.rest_index)
    # end

    #    *** для случая с расстановкой ударения  (см. ниже)
    #    # local orig_stem = data.stem.unstressed
    #    if _.contains(data.rest_index, ['%(2%)', '②']):
    #        orig_stem = _.replaced(data.stems['gen_pl'], '́ ', '')  -- удаляем ударение для случая "сапожок *d(2)"
    #        mw.log('> Another `orig_stem`: ' + str(orig_stem))
    #    # end

    # reducable
    data.rest_index = degree.apply_specific_degree(data.stems, data.endings, data.word.unstressed, data.stem.unstressed, data.stem.type, data.gender, data.stress_type, data.rest_index, data)
    reducable.apply_specific_reducable(data.stems, data.endings, data.word.unstressed, data.stem.unstressed, data.stem.type, data.gender, data.stress_type, data.rest_index, data, False)
    if not _.equals(data.stress_type, ["f", "f'"]) and _.contains(data.rest_index, '%*'):
        mw.log('# Обработка случая на препоследний слог основы при чередовании'); orig_stem = data.stem.unstressed
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
                    if not _.contains(data.stems[key], '[́ ё]'):  # если предпоследнего слога попросту нет
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


# return export
