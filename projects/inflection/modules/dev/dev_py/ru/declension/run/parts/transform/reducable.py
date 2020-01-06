from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.parts.transform.reducable'  # local


# Сложный алгоритм обработки всех случаев чередования
@a.starts(module)
def apply_specific_reducable(func, i, gender, rest_index, only_sg):  # export
    # local reduced, reduced_letter, f8_third, prev
    # local case_2_a, case_2_b, case_2_c, case_3_a, case_3_b
    # local skip_b_1, skip_b_2, skip_b_3, force_b
    # local case

    p = i.parts  # local

    if _.contains(rest_index, '%*'):

        reduced = '?'
        if i.adj:
            if gender == 'm':
                if _.contains(rest_index, ['%(1%)', '①']):
                    if gender == 'm' and i.adj and _.endswith(i.word.unstressed, 'ний') and p.endings['srt-sg'] == 'ь':  # fixme: temporary duplicated with the same code at the ending of function...
                        p.endings['srt-sg'] = ''  # вместо `ь` для `2*a`
                    # end
                    return _.ends(module, func)
                # end
                if _.contains(rest_index, ['%(2%)', '②']):
                    return _.ends(module, func)
                # end
                reduced = 'B'
            else:
                return _.ends(module, func)
            # end
        elif gender == 'm' or i.pronoun:
            reduced = 'A'
        elif gender == 'n':
            reduced = 'B'
        elif gender == 'f':
            if i.stem.type == '8-third':
                reduced = 'A'
            else:
                reduced = 'B'
            # end
        # end

        _.log_info('Случай чередования: ' + str(reduced))

        if reduced == 'A':
            reduced_letter = _.extract(i.word.unstressed, '({vowel+ё}){consonant}+$')
            f8_third = gender == 'f' and i.stem.type == '8-third'

            _.log_value(reduced_letter, 'reduced_letter')

            if reduced_letter == 'о':
                _.replace(p.stems, 'all-sg', '(.)о́ ?([^о]+)$', '%1%2')

#                # local stem_gen_pl
#                # У этих имён последняя гласная основы исходной формы заменяется на нуль, о или й во всех формах, не совпадающих с исходной (кроме Т. ед. на -ью).
#                # if p.endings['gen-pl'] == '':  -- ботинок, глазок
#                if _.contains(rest_index, ['%(2%)', '②']):
#                    stem_gen_pl = p.stems['gen-pl']
#                # end

                if not only_sg:
                    _.replace(p.stems, 'all-pl', '(.)о́ ?([^о]+)$', '%1%2')
                # end

#                if stem_gen_pl:  # ботинок, глазок
#                    p.stems['gen-pl'] = stem_gen_pl
#                # end

                if not f8_third:
                    _.replace(p.stems, 'ins-sg', '(.)о́ ?([^о]+)$', '%1%2')
                # end

            elif reduced_letter == 'и':  # бывает только в подтипе мс 6*
                _.replace(p.stems, 'all-sg', '(.)и́ ?([^и]+)$', '%1ь%2')
                if not only_sg:
                    _.replace(p.stems, 'all-pl', '(.)и́ ?([^и]+)$', '%1ь%2')
                # end

            elif _.In(reduced_letter, ['е', 'ё']):
                prev = _.extract(i.word.unstressed, '(.)[её][^её]+$')

                case_2_a = i.stem.type == '6-vowel'  # 2) а).
                case_2_b = i.stem.type == '3-velar' and _.contains(prev, '[^аеёиоуыэюяшжчщц]')  # 2) б).
                case_2_c = not _.equals(i.stem.type, ['6-vowel', '3-velar']) and prev == 'л'  # 2) в).

                if _.contains(prev, '{vowel+ё}'):  # 1).
                    _.log_info('Подслучай A.1).')
                    _.replace(p.stems, 'all-sg', '[её]́ ?([^её]+)$', 'й%1')
                    if not f8_third:
                        _.replace(p.stems, 'ins-sg', '[её]́ ?([^её]+)$', 'й%1')
                    # end
                    if not only_sg:
                        _.replace(p.stems, 'all-pl', '[её]́ ?([^её]+)$', 'й%1')
                    # end

                elif case_2_a or case_2_b or case_2_c:  # 2).

                    _.log_info('Подслучай A.2).')
                    _.replace(p.stems, 'all-sg', '[её]́ ?([^её]*)$', 'ь%1')
                    if not f8_third:
                        _.replace(p.stems, 'ins-sg', '[её]́ ?([^её]*)$', 'ь%1')
                    # end
                    if not only_sg:
                        _.replace(p.stems, 'all-pl', '[её]́ ?([^её]*)$', 'ь%1')
                    # end

                else:  # 3).
                    _.log_info('Подслучай A.3).')
                    _.replace(p.stems, 'all-sg', '[её]́ ?([^её]*)$', '%1')
                    if not f8_third:
                        _.replace(p.stems, 'ins-sg', '[её]́ ?([^её]*)$', '%1')
                    # end
                    if not only_sg:
                        _.replace(p.stems, 'all-pl', '[её]́ ?([^её]*)$', '%1')
                    # end
                # end
            # end
        # end  # reduced A

        if only_sg:
            return _.ends(module, func) # ниже всё равно обрабатывается только множественное число уже
        # end

        # we should ignore asterix for 2*b and 2*f (so to process it just like 2b or 2f)
        skip_b_1 = i.stem.type == '2-soft' and _.In(i.stress_type, ['b', 'f'])

        # and also the same for (2)-specific and 3,5,6 stem-types
        skip_b_2 = _.contains(rest_index, ['%(2%)', '②']) and (
            _.In(i.stem.type, {'2-soft'})  # '2-soft' из сходня 2*a(2)

            # TODO: Разобраться, почему это нужно было на самом деле?
#            _.In(i.stem.type, ['3-velar', '5-letter-ц', '6-vowel'])  # так было раньше, без прочих skip
        )

        # TODO: Разобраться, почему это нужно на самом деле?
        skip_b_3 = _.contains(rest_index, ['%(2%)', '②']) and gender == 'n'  # temp fix

        stem = i.stem.unstressed  # local

        force_b = False
        if _.contains(rest_index, ['%(2%)', '②']):
            gender = 'n'  # fixme: ????
            i.forced_stem = p.stems['gen-pl']
            stem = p.stems['gen-pl']
            _.log_info('New force stem (gen-pl): ' + str(stem))
            force_b = True
        # end

        # TODO: б) в словах прочих схем ударения — на последний слог основы, если основа не содержит беглой гласной, и на предпоследний слог основы, если основа содержит беглую гласную, на¬пример: величина, тюрьма, полотно (схема d) — И.мн. величины, тюрьмы, полотна, Р.мн. ве¬личин, тюрем, полотен.
        # это для глАзок

        if (reduced == 'B' or force_b) and not skip_b_1 and not skip_b_2 and not skip_b_3:
            if i.adj:
                case = 'srt-sg'
            else:
                case = 'gen-pl'
            # end

            _.log_info('Зашли в случай чередования B')
            if i.stem.type == '6-vowel':  # 1).
                _.log_info('Подслучай B.1).')
                if _.In(i.stress_type, {'b', 'c', 'e', 'f', "f'", "b'" }):  # gen-pl ending stressed  -- TODO: special vars for that
                    _.replace(p.stems, case, 'ь$', 'е́')
                else:
                    _.replace(p.stems, case, 'ь$', 'и')
                # end
            elif _.contains(stem, '[ьй]{consonant}$'):  # 2).
                _.log_info('Подслучай B.2).')
                if i.adj:
                    e = i.stem.type == '5-letter-ц' or not _.contains(i.stress_type, 'b') or _.endswith(i.stress_type, ['/b', "/b'"])  # todo: fix only "b" for srt...
                else:
                    e = i.stem.type == '5-letter-ц' or _.equals(i.stress_type, ['a', 'd', "d'"])  # gen_pl ending unstressed  -- TODO: special vars for that
                # end
                if e:
                    _.replace(p.stems, case, '[ьй]({consonant})$', 'е%1')
                else:
                    _.replace(p.stems, case, '[ьй]({consonant})$', 'ё%1')
                # end
            else:  # 3).
                prev = _.extract(stem, '(.){consonant}$')
                case_3_a = i.stem.type == '3-velar' and _.contains(prev, '[^жшчщц]')  # 3). а).
                case_3_b = _.contains(prev, '[кгх]')  # 3). б).
                if case_3_a or case_3_b:
                    _.log_info('Подслучай B.3). а,б).')
                    _.replace(p.stems, case, '(.)({consonant})$', '%1о%2')
                else:  # 3). в).
                    _.log_info('Подслучай B.3). в).')
                    if i.stem.type == '5-letter-ц':
                        _.log_info('i.stem.type == "letter-ц"')
                        _.replace(p.stems, case, '(.)({consonant})$', '%1е%2')
                    else:
                        if i.adj:
                            e = _.equals(i.stress_type, 'b') or _.endswith(i.stress_type, ['/b', "/b'"])  # TODO: special vars for that
                        else:
                            e = _.In(i.stress_type, {'b', 'c', 'e', 'f', "f'", "b'" })  # gen_pl ending stressed  -- TODO: special vars for that
                        # end
                        if e:
                            _.log_info('в `' + case + '` ударение на окончание')
                            p.stems[case] = stem
                            if _.contains(prev, '[жшчщ]'):
                                _.log_info('предыдущая [жшчщ]')
                                _.replace(p.stems, case, '(.)({consonant})$', '%1о́%2')
                            else:
                                _.log_info('предыдущая не [жшчщ]')
                                _.replace(p.stems, case, '(.)({consonant})$', '%1ё%2')
                            # end
                        else:
                            _.log_info('ударение на основу в ["' + case + '"] ')
                            _.replace(p.stems, case, '(.)({consonant})$', '%1е%2')
                        # end
                    # end
                # end
            # end
            if i.stem.type == '2-soft' and _.endswith(i.word.unstressed, 'ня') and i.stress_type == 'a' and p.endings['gen-pl'] == 'ь':
                p.endings['gen-pl'] = ''  # вместо `ь` для `2*a`
            # end
            if gender == 'm' and i.adj and _.endswith(i.word.unstressed, 'ний') and p.endings['srt-sg'] == 'ь':
                p.endings['srt-sg'] = ''  # вместо `ь` для `2*a`
            # end
#            if _.contains(rest_index, 'ё'):
#                if _.contains(p.stems['gen-pl'], 'ё.*е'):
#                    mw.log('% Специальный случай-исправление типа "сёстер" -> "сестёр"')
#                    _.replace(p.stems, 'gen-pl', 'ё(.*)е([^е]*)$', 'е%1ё%2')
#                # end
#            # end
        # end  # reduced B
    # end  # specific *

    _.ends(module, func)
# end


# return export
