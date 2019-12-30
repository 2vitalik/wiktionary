from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.parts.transform import degree as degree
from ...run.parts.transform import reducable as reducable
from ...run.parts.transform.circles import adj as adj_circles


module = 'modify.transform'  # local


@a.starts(module)
def transform(func, info):  # export
    # local stem_stress_schema

    # apply special cases (1) or (2) in index
    if info.adj:
        adj_circles.apply_adj_specific_1_2(info.data.stems, info.gender, info.rest_index)
    # end

    #    *** для случая с расстановкой ударения  (см. ниже)
    #    # local orig_stem = info.stem.unstressed
    #    if _.contains(info.rest_index, ['%(2%)', '②']):
    #        orig_stem = _.replaced(info.data.stems['gen-pl'], '́ ', '')  -- удаляем ударение для случая "сапожок *d(2)"
    #        mw.log('> Another `orig_stem`: ' + str(orig_stem))
    #    # end

    # reducable
    info.rest_index = degree.apply_specific_degree(info.data.stems, info.data.endings, info.word.unstressed, info.stem.unstressed, info.stem.type, info.gender, info.stress_type, info.rest_index, info)
    reducable.apply_specific_reducable(info.data.stems, info.data.endings, info.word.unstressed, info.stem.unstressed, info.stem.type, info.gender, info.stress_type, info.rest_index, info, False)
    if not _.equals(info.stress_type, ["f", "f'"]) and _.contains(info.rest_index, '%*'):
        mw.log('# Обработка случая на препоследний слог основы при чередовании'); orig_stem = info.stem.unstressed
        if info.forced_stem:
            orig_stem = info.forced_stem
        # end
        for key, stem in info.data.stems.items():
            #            mw.log(' - ' + key + ' -> ' + stem)
            #            mw.log('Ударение на основу?')
            #            mw.log(info.stress_schema['stem'][key])
            stem_stress_schema = info.stress_schema['stem']
            if not _.contains(stem, '[́ ё]') and _.has_key(stem_stress_schema, key) and stem_stress_schema[key]:
                # *** случай с расстановкой ударения  (см. выше)
                # "Дополнительные правила об ударении", стр. 34
                old_value = info.data.stems[key]
                # mw.log('> ' + key + ' (old): ' + str(old_value))
                if info.data.stems[key] != orig_stem:  # попытка обработать наличие беглой гласной (не знаю, сработает ли всегда)
                    info.data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)({vowel})({consonant}*)$', '%1́ %2%3%4')
                    if not _.contains(info.data.stems[key], '[́ ё]'):  # если предпоследнего слога попросту нет
                        # сделаем хоть последний ударным
                        info.data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
                    # end
                else:
                    info.data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
                # end
                # mw.log('> ' + key + ' (new): ' + str(info.data.stems[key]))
                mw.log('  - ' + key + ': "' + str(old_value) + '" -> "' + str(info.data.stems[key]) + '"')
            # end
        # end
    # end

    # Специфика по "ё"
    if _.contains(info.rest_index, 'ё') and not _.contains(info.data.endings['gen-pl'], '{vowel+ё}') and not _.contains(info.data.stems['gen-pl'], 'ё'):
        info.data.stems['gen-pl'] = _.replaced(info.data.stems['gen-pl'], 'е́?([^е]*)$', 'ё%1')
        info.rest_index = info.rest_index + 'ё'  # ???
    # end

    _.ends(module, func)
# end


# return export
