from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.parts.transform import degree as degree
from ...run.parts.transform import reducable as reducable
from ...run.parts.transform.circles import adj as adj_circles


module = 'run.parts.transform'  # local


@a.starts(module)
def transform(func, i):  # export
    # local stem_stress_schema
    p = i.parts  # local

    # apply special cases (1) or (2) in index
    if i.adj:
        adj_circles.apply_adj_specific_1_2(i)
    # end

    #    *** для случая с расстановкой ударения  (см. ниже)
    #    # local orig_stem = i.stem.unstressed
    #    if _.contains(i.rest_index, ['%(2%)', '②']):
    #        orig_stem = _.replaced(p.stems['gen-pl'], '́ ', '')  -- удаляем ударение для случая "сапожок *d(2)"
    #        mw.log('> Another `orig_stem`: ' + str(orig_stem))
    #    # end

    # reducable
    i.rest_index = degree.apply_specific_degree(i)
    reducable.apply_specific_reducable(i, i.gender, i.rest_index, False)
    if not _.equals(i.stress_type, ["f", "f'"]) and _.contains(i.rest_index, '%*'):
        _.log_info('Обработка случая на препоследний слог основы при чередовании')
        orig_stem = i.stem.unstressed
        if i.forced_stem:
            orig_stem = i.forced_stem
        # end
        for key, stem in p.stems.items():
            # mw.log(' - ' + key + ' -> ' + stem)
            # mw.log('Ударение на основу?')
            # mw.log(i.stress_schema['stem'][key])
            stem_stress_schema = i.stress_schema['stem']
            if not _.contains(stem, '[́ ё]') and _.has_key(stem_stress_schema, key) and stem_stress_schema[key]:
                # *** случай с расстановкой ударения  (см. выше)
                # "Дополнительные правила об ударении", стр. 34
                old_value = p.stems[key]
                # mw.log('> ' + key + ' (old): ' + str(old_value))
                if p.stems[key] != orig_stem:  # попытка обработать наличие беглой гласной (не знаю, сработает ли всегда)
                    p.stems[key] = _.replaced(stem, '({vowel})({consonant}*)({vowel})({consonant}*)$', '%1́ %2%3%4')
                    if not _.contains(p.stems[key], '[́ ё]'):  # если предпоследнего слога попросту нет
                        # сделаем хоть последний ударным
                        p.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
                    # end
                else:
                    p.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
                # end
                # mw.log('> ' + key + ' (new): ' + str(p.stems[key]))
                mw.log('  - ' + key + ': "' + str(old_value) + '" -> "' + str(p.stems[key]) + '"')
            # end
        # end
    # end

    if i.calc_pl:
        # Специфика по "ё"
        if _.contains(i.rest_index, 'ё') and not _.contains(p.endings['gen-pl'], '{vowel+ё}') and not _.contains(p.stems['gen-pl'], 'ё'):
            p.stems['gen-pl'] = _.replaced(p.stems['gen-pl'], 'е́?([^е]*)$', 'ё%1')
            i.rest_index = i.rest_index + 'ё'  # ???
        # end
    # end

    _.ends(module, func)
# end


# return export
