from projects.inflection.modules.prod.prod_py import additional
from projects.inflection.modules.prod.prod_py import mw
from projects.inflection.modules.prod.prod_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


def apply_specific_degree(stems, endings, word, stem, stem_type, gender, stress_type, rest_index, data):  # export
    _.log_func('reducable', 'apply_specific_degree')

    # If degree sign °

    if _.contains(rest_index, '°') and _.endswith(word, '[ая]нин'):
        _.replace(stems, 'all_pl', '([ая])ни́ н$', '%1́ н')
        _.replace(stems, 'all_pl', '([ая]́ ?н)ин$', '%1')
        endings['nom_pl'] = 'е'
        endings['gen_pl'] = ''
        return rest_index
    # end

    if _.contains(rest_index, '°') and _.endswith(word, 'ин'):
        _.replace(stems, 'all_pl', 'и́ ?н$', '')
        if not _.contains(rest_index, ['%(1%)', '①']):
            endings['nom_pl'] = 'е'
        # end
        endings['gen_pl'] = ''
    # end

    if _.contains(rest_index, '°') and _.endswith(word, ['ёнок', 'онок']):
        _.replace(stems, 'all_pl', 'ёнок$', 'я́т')
        _.replace(stems, 'all_pl', 'о́нок$', 'а́т')

        # INFO: Эмуляция среднего рода `1a` для форм мн. числа
        endings['nom_pl'] = 'а'
        endings['gen_pl'] = ''

        apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index + '*', data, True)  # export.
        return rest_index
    # end

    if _.contains(rest_index, '°') and _.endswith(word, ['ёночек', 'оночек']):

        _.replace(stems, 'all_pl', 'ёночек$', 'я́тк')
        _.replace(stems, 'all_pl', 'о́ночек$', 'а́тк')

        # INFO: Черездование для единичной формы (возможно применится также и для множественной, но это не страшно, потом заменится по идее)
        apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index + '*', data, False)  # export.

        # INFO: По сути должно примениться только к мн. формам (случай `B`)
        apply_specific_reducable(stems, endings, word, stem, stem_type, 'f', stress_type, rest_index + '*', data, False)  # export.

        endings['gen_pl'] = ''  # INFO: Странный фикс, но он нужен.. <_<

        return rest_index
    # end

    if _.contains(rest_index, '°') and gender == 'n' and _.endswith(word, 'мя'):
        _.replace(stems, 'all_sg', 'м$', 'мен')
        _.replace(stems, 'ins_sg', 'м$', 'мен')
        _.replace(stems, 'all_pl', 'м$', 'мен')

        endings['nom_sg'] = 'я'
        endings['gen_sg'] = 'и'
        endings['dat_sg'] = 'и'
        endings['ins_sg'] = 'ем'
        endings['prp_sg'] = 'и'
    # end

    return rest_index
# end


# Сложный алгоритм обработки всех случаев чередования
def apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index, data, only_sg):  # export
    _.log_func('reducable', 'apply_specific_reducable')

    # local reduced, reduced_letter, f_3rd, prev
    # local case_2_a, case_2_b, case_2_c, case_3_a, case_3_b
    # local skip_b_1, skip_b_2, skip_b_3, force_b
    # local case

    if _.contains(rest_index, '%*'):

        reduced = '?'
        if data.adj:
            if gender == 'm':
                if _.contains(rest_index, ['%(1%)', '①']):
                    if gender == 'm' and data.adj and _.endswith(word, 'ний') and endings['srt_sg'] == 'ь':  # fixme: temporary duplicated with the same code at the ending of function...
                        endings['srt_sg'] = ''  # вместо `ь` для `2*a`
                    # end
                    return
                # end
                if _.contains(rest_index, ['%(2%)', '②']):
                    return
                # end
                reduced = 'B'
            else:
                return
            # end
        elif gender == 'm' or data.pronoun:
            reduced = 'A'
        elif gender == 'n':
            reduced = 'B'
        elif gender == 'f':
            if _.equals(stem_type, ['f-3rd', 'f-3rd-sibilant']):
                reduced = 'A'
            else:
                reduced = 'B'
            # end
        # end

        mw.log('# Случай чередования: ' + str(reduced))

        if reduced == 'A':
            reduced_letter = _.extract(word, '({vowel+ё}){consonant}+$')
            f_3rd = _.In(stem_type, ['f-3rd', 'f-3rd-sibilant'])

            _.log_value(reduced_letter, 'reduced_letter')

            if reduced_letter == 'о':
                _.replace(stems, 'all_sg', '(.)о́ ?([^о]+)$', '%1%2')

#                # local stem_gen_pl
#                # У этих имён последняя гласная основы исходной формы заменяется на нуль, о или й во всех формах, не совпадающих с исходной (кроме Т. ед. на -ью).
#                # if endings['gen_pl'] == '':  -- ботинок, глазок
#                if _.contains(rest_index, ['%(2%)', '②']):
#                    stem_gen_pl = stems['gen_pl']
#                # end

                if not only_sg:
                    _.replace(stems, 'all_pl', '(.)о́ ?([^о]+)$', '%1%2')
                # end

#                if stem_gen_pl:  # ботинок, глазок
#                    stems['gen_pl'] = stem_gen_pl
#                # end

                if not f_3rd:
                    _.replace(stems, 'ins_sg', '(.)о́ ?([^о]+)$', '%1%2')
                # end

            elif reduced_letter == 'и':  # бывает только в подтипе мс 6*
                _.replace(stems, 'all_sg', '(.)и́ ?([^и]+)$', '%1ь%2')
                if not only_sg:
                    _.replace(stems, 'all_pl', '(.)и́ ?([^и]+)$', '%1ь%2')
                # end

            elif _.In(reduced_letter, ['е', 'ё']):
                prev = _.extract(word, '(.)[её][^её]+$')

                case_2_a = stem_type == 'vowel'  # 2) а).
                case_2_b = stem_type == 'velar' and _.contains(prev, '[^аеёиоуыэюяшжчщц]')  # 2) б).
                case_2_c = not _.equals(stem_type, ['vowel', 'velar']) and prev == 'л'  # 2) в).

                if _.contains(prev, '{vowel+ё}'):  # 1).
                    mw.log('  # Подслучай A.1).')
                    _.replace(stems, 'all_sg', '[её]́ ?([^её]+)$', 'й%1')
                    if not f_3rd:
                        _.replace(stems, 'ins_sg', '[её]́ ?([^её]+)$', 'й%1')
                    # end
                    if not only_sg:
                        _.replace(stems, 'all_pl', '[её]́ ?([^её]+)$', 'й%1')
                    # end

                elif case_2_a or case_2_b or case_2_c:  # 2).

                    mw.log('  # Подслучай A.2).')
                    _.replace(stems, 'all_sg', '[её]́ ?([^её]*)$', 'ь%1')
                    if not f_3rd:
                        _.replace(stems, 'ins_sg', '[её]́ ?([^её]*)$', 'ь%1')
                    # end
                    if not only_sg:
                        _.replace(stems, 'all_pl', '[её]́ ?([^её]*)$', 'ь%1')
                    # end

                else:  # 3).
                    mw.log('  # Подслучай A.3).')
                    _.replace(stems, 'all_sg', '[её]́ ?([^её]*)$', '%1')
                    if not f_3rd:
                        _.replace(stems, 'ins_sg', '[её]́ ?([^её]*)$', '%1')
                    # end
                    if not only_sg:
                        _.replace(stems, 'all_pl', '[её]́ ?([^её]*)$', '%1')
                    # end
                # end
            # end
        # end  # reduced A

        if only_sg:
            return  # ниже всё равно обрабатывается только множественное число уже
        # end

        # we should ignore asterix for 2*b and 2*f (so to process it just like 2b or 2f)
        skip_b_1 = stem_type == 'soft' and _.In(stress_type, ['b', 'f'])

        # and also the same for (2)-specific and 3,5,6 stem-types
        skip_b_2 = _.contains(rest_index, ['%(2%)', '②']) and (
            _.In(stem_type, {'soft'})  # 'soft' из сходня 2*a(2)

            # TODO: Разобраться, почему это нужно было на самом деле?
#            _.In(stem_type, ['velar', 'letter-ц', 'vowel'])  # так было раньше, без прочих skip
        )

        # TODO: Разобраться, почему это нужно на самом деле?
        skip_b_3 = _.contains(rest_index, ['%(2%)', '②']) and gender == 'n'  # temp fix

        force_b = False
        if _.contains(rest_index, ['%(2%)', '②']):
            gender = 'n'
            data.forced_stem = stems['gen_pl']
            stem = stems['gen_pl']
            mw.log('  # New force stem (gen_pl): ' + str(stem))
            force_b = True
        # end

        # TODO: б) в словах прочих схем ударения — на последний слог основы, если основа не содержит беглой гласной, и на предпоследний слог основы, если основа содержит беглую гласную, на¬пример: величина, тюрьма, полотно (схема d) — И.мн. величины, тюрьмы, полотна, Р.мн. ве¬личин, тюрем, полотен.
        # это для глАзок

        if (reduced == 'B' or force_b) and not skip_b_1 and not skip_b_2 and not skip_b_3:
            if data.adj:
                case = 'srt_sg'
            else:
                case = 'gen_pl'
            # end

            mw.log('  # Зашли в случай чередования B')
            if stem_type == 'vowel':  # 1).
                mw.log('  # Подслучай B.1).')
                if _.In(stress_type, {'b', 'c', 'e', 'f', "f'", "b'" }):  # gen_pl ending stressed  -- TODO: special vars for that
                    _.replace(stems, case, 'ь$', 'е́')
                else:
                    _.replace(stems, case, 'ь$', 'и')
                # end
            elif _.contains(stem, '[ьй]{consonant}$'):  # 2).
                mw.log('  # Подслучай B.2).')
                if data.adj:
                    e = stem_type == 'letter-ц' or not _.contains(stress_type, 'b') or _.endswith(stress_type, ['/b', "/b'"])  # todo: fix only "b" for srt...
                else:
                    e = stem_type == 'letter-ц' or _.equals(stress_type, ['a', 'd', "d'"])  # gen_pl ending unstressed  -- TODO: special vars for that
                # end
                if e:
                    _.replace(stems, case, '[ьй]({consonant})$', 'е%1')
                else:
                    _.replace(stems, case, '[ьй]({consonant})$', 'ё%1')
                # end
            else:  # 3).
                prev = _.extract(stem, '(.){consonant}$')
                case_3_a = stem_type == 'velar' and _.contains(prev, '[^жшчщц]')  # 3). а).
                case_3_b = _.contains(prev, '[кгх]')  # 3). б).
                if case_3_a or case_3_b:
                    mw.log('  # Подслучай B.3). а,б).')
                    _.replace(stems, case, '(.)({consonant})$', '%1о%2')
                else:  # 3). в).
                    mw.log('  # Подслучай B.3). в).')
                    if stem_type == 'letter-ц':
                        mw.log('  # stem_type == "letter-ц"')
                        _.replace(stems, case, '(.)({consonant})$', '%1е%2')
                    else:
                        if data.adj:
                            e = _.equals(stress_type, 'b') or _.endswith(stress_type, ['/b', "/b'"])  # TODO: special vars for that
                        else:
                            e = _.In(stress_type, {'b', 'c', 'e', 'f', "f'", "b'" })  # gen_pl ending stressed  -- TODO: special vars for that
                        # end
                        if e:
                            mw.log('  # в `' + case + '` ударение на окончание')
                            stems[case] = data.stem
                            if _.contains(prev, '[жшчщ]'):
                                mw.log('  # предыдущая [жшчщ]')
                                _.replace(stems, case, '(.)({consonant})$', '%1о́%2')
                            else:
                                mw.log('  # предыдущая не [жшчщ]')
                                _.replace(stems, case, '(.)({consonant})$', '%1ё%2')
                            # end
                        else:
                            mw.log('    # ударение на основу в ["' + case + '"] ')
                            _.replace(stems, case, '(.)({consonant})$', '%1е%2')
                        # end
                    # end
                # end
            # end
            if stem_type == 'soft' and _.endswith(word, 'ня') and stress_type == 'a' and endings['gen_pl'] == 'ь':
                endings['gen_pl'] = ''  # вместо `ь` для `2*a`
            # end
            if gender == 'm' and data.adj and _.endswith(word, 'ний') and endings['srt_sg'] == 'ь':
                endings['srt_sg'] = ''  # вместо `ь` для `2*a`
            # end
#            if _.contains(rest_index, 'ё'):
#                if _.contains(stems['gen_pl'], 'ё.*е'):
#                    mw.log('% Специальный случай-исправление типа "сёстер" -> "сестёр"')
#                    _.replace(stems, 'gen_pl', 'ё(.*)е([^е]*)$', 'е%1ё%2')
#                # end
#            # end
        # end  # reduced B
    # end  # specific *
# end


# return export
