local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


function export.apply_specific_degree(stems, endings, word, stem, stem_type, gender, stress_type, rest_index, data)
	_.log_func('reducable', 'apply_specific_degree')

	-- If degree sign °

	if _.contains(rest_index, '°') and _.endswith(word, '[ая]нин') then
		_.replace(stems, 'all_pl', '([ая])ни́ н$', '%1́ н')
		_.replace(stems, 'all_pl', '([ая]́ ?н)ин$', '%1')
		endings['nom_pl'] = 'е'
		endings['gen_pl'] = ''
		return rest_index
	end

	if _.contains(rest_index, '°') and _.endswith(word, 'ин') then
		_.replace(stems, 'all_pl', 'и́ ?н$', '')
		if not _.contains(rest_index, {'%(1%)', '①'}) then
			endings['nom_pl'] = 'е'
		end
		endings['gen_pl'] = ''
	end

	if _.contains(rest_index, '°') and _.endswith(word, {'ёнок', 'онок'}) then
		_.replace(stems, 'all_pl', 'ёнок$', 'я́т')
		_.replace(stems, 'all_pl', 'о́нок$', 'а́т')

--		INFO: Эмуляция среднего рода `1a` для форм мн. числа
		endings['nom_pl'] = 'а'
		endings['gen_pl'] = ''

		export.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index .. '*', data, true)
		return rest_index
	end

	if _.contains(rest_index, '°') and _.endswith(word, {'ёночек', 'оночек'}) then

		_.replace(stems, 'all_pl', 'ёночек$', 'я́тк')
		_.replace(stems, 'all_pl', 'о́ночек$', 'а́тк')

--		INFO: Черездование для единичной формы (возможно применится также и для множественной, но это не страшно, потом заменится по идее)
		export.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index .. '*', data, false)

--		INFO: По сути должно примениться только к мн. формам (случай `B`)
		export.apply_specific_reducable(stems, endings, word, stem, stem_type, 'f', stress_type, rest_index .. '*', data, false)

		endings['gen_pl'] = ''  -- INFO: Странный фикс, но он нужен.. <_<

		return rest_index
	end

	if _.contains(rest_index, '°') and gender == 'n' and _.endswith(word, 'мя') then
		_.replace(stems, 'all_sg', 'м$', 'мен')
		_.replace(stems, 'ins_sg', 'м$', 'мен')
		_.replace(stems, 'all_pl', 'м$', 'мен')

		endings['nom_sg'] = 'я'
		endings['gen_sg'] = 'и'
		endings['dat_sg'] = 'и'
		endings['ins_sg'] = 'ем'
		endings['prp_sg'] = 'и'
	end

	return rest_index
end


-- Сложный алгоритм обработки всех случаев чередования
function export.apply_specific_reducable(stems, endings, word, stem, stem_type, gender, stress_type, rest_index, data, only_sg)
	_.log_func('reducable', 'apply_specific_reducable')

	local reduced, reduced_letter, f_3rd, prev
	local case_2_a, case_2_b, case_2_c, case_3_a, case_3_b
	local skip_b_1, skip_b_2, skip_b_3, force_b
	local case

	if _.contains(rest_index, '%*') then

		reduced = '?'
		if data.adj then
			if gender == 'm' then
				if _.contains(rest_index, {'%(1%)', '①'}) then
					if gender == 'm' and data.adj and _.endswith(word, 'ний') and endings['srt_sg'] == 'ь' then  -- fixme: temporary duplicated with the same code at the ending of function...
						endings['srt_sg'] = ''  -- вместо `ь` для `2*a`
					end
					return
				end
				if _.contains(rest_index, {'%(2%)', '②'}) then
					return
				end
				reduced = 'B'
			else
				return
			end
		elseif gender == 'm' or data.pronoun then
			reduced = 'A'
		elseif gender == 'n' then
			reduced = 'B'
		elseif gender == 'f' then
			if _.equals(stem_type, {'f-3rd', 'f-3rd-sibilant'}) then
				reduced = 'A'
			else
				reduced = 'B'
			end
		end

		mw.log('# Случай чередования: ' .. tostring(reduced))

		if reduced == 'A' then
			reduced_letter = _.extract(word, '({vowel+ё}){consonant}+$')
			f_3rd = _.In(stem_type, {'f-3rd', 'f-3rd-sibilant'})

			_.log_value(reduced_letter, 'reduced_letter')

			if reduced_letter == 'о' then
				_.replace(stems, 'all_sg', '(.)о́ ?([^о]+)$', '%1%2')

--				local stem_gen_pl
--				-- У этих имён последняя гласная основы исходной формы заменяется на нуль, о или й во всех формах, не совпадающих с исходной (кроме Т. ед. на -ью).
--				-- if endings['gen_pl'] == '' then  -- ботинок, глазок
--				if _.contains(rest_index, {'%(2%)', '②'}) then
--					stem_gen_pl = stems['gen_pl']
--				end

				if not only_sg then
					_.replace(stems, 'all_pl', '(.)о́ ?([^о]+)$', '%1%2')
				end

--				if stem_gen_pl then  -- ботинок, глазок
--					stems['gen_pl'] = stem_gen_pl
--				end

				if not f_3rd then
					_.replace(stems, 'ins_sg', '(.)о́ ?([^о]+)$', '%1%2')
				end

			elseif reduced_letter == 'и' then  -- бывает только в подтипе мс 6*
				_.replace(stems, 'all_sg', '(.)и́ ?([^и]+)$', '%1ь%2')
				if not only_sg then
					_.replace(stems, 'all_pl', '(.)и́ ?([^и]+)$', '%1ь%2')
				end

			elseif _.In(reduced_letter, {'е', 'ё'}) then
				prev = _.extract(word, '(.)[её][^её]+$')

				case_2_a = stem_type == 'vowel'  -- 2) а).
				case_2_b = stem_type == 'velar' and _.contains(prev, '[^аеёиоуыэюяшжчщц]')  -- 2) б).
				case_2_c = not _.equals(stem_type, {'vowel', 'velar'}) and prev == 'л'  -- 2) в).

				if _.contains(prev, '{vowel+ё}') then  -- 1).
					mw.log('  -- Подслучай A.1).')
					_.replace(stems, 'all_sg', '[её]́ ?([^её]+)$', 'й%1')
					if not f_3rd then
						_.replace(stems, 'ins_sg', '[её]́ ?([^её]+)$', 'й%1')
					end
					if not only_sg then
						_.replace(stems, 'all_pl', '[её]́ ?([^её]+)$', 'й%1')
					end

				elseif case_2_a or case_2_b or case_2_c then  -- 2).

					mw.log('  -- Подслучай A.2).')
					_.replace(stems, 'all_sg', '[её]́ ?([^её]*)$', 'ь%1')
					if not f_3rd then
						_.replace(stems, 'ins_sg', '[её]́ ?([^её]*)$', 'ь%1')
					end
					if not only_sg then
						_.replace(stems, 'all_pl', '[её]́ ?([^её]*)$', 'ь%1')
					end

				else  -- 3).
					mw.log('  -- Подслучай A.3).')
					_.replace(stems, 'all_sg', '[её]́ ?([^её]*)$', '%1')
					if not f_3rd then
						_.replace(stems, 'ins_sg', '[её]́ ?([^её]*)$', '%1')
					end
					if not only_sg then
						_.replace(stems, 'all_pl', '[её]́ ?([^её]*)$', '%1')
					end
				end
			end
		end  -- reduced A

		if only_sg then
			return  -- ниже всё равно обрабатывается только множественное число уже
		end

		-- we should ignore asterix for 2*b and 2*f (so to process it just like 2b or 2f)
		skip_b_1 = stem_type == 'soft' and _.In(stress_type, {'b', 'f'})

		-- and also the same for (2)-specific and 3,5,6 stem-types
		skip_b_2 = _.contains(rest_index, {'%(2%)', '②'}) and (
			_.In(stem_type, {'soft'})  -- 'soft' из сходня 2*a(2)

			-- TODO: Разобраться, почему это нужно было на самом деле?
--			_.In(stem_type, {'velar', 'letter-ц', 'vowel'})  -- так было раньше, без прочих skip
		)

		-- TODO: Разобраться, почему это нужно на самом деле?
		skip_b_3 = _.contains(rest_index, {'%(2%)', '②'}) and gender == 'n'  -- temp fix

		force_b = false
		if _.contains(rest_index, {'%(2%)', '②'}) then
			gender = 'n'
			data.forced_stem = stems['gen_pl']
			stem = stems['gen_pl']
			mw.log('  -- New force stem (gen_pl): ' .. tostring(stem))
			force_b = true
		end

		-- TODO: б) в словах прочих схем ударения — на последний слог основы, если основа не содержит беглой гласной, и на предпоследний слог основы, если основа содержит беглую гласную, на¬пример: величина, тюрьма, полотно (схема d) — И.мн. величины, тюрьмы, полотна, Р.мн. ве¬личин, тюрем, полотен.
		-- это для глАзок

		if (reduced == 'B' or force_b) and not skip_b_1 and not skip_b_2 and not skip_b_3 then
			if data.adj then
				case = 'srt_sg'
			else
				case = 'gen_pl'
			end

			mw.log('  -- Зашли в случай чередования B')
			if stem_type == 'vowel' then  -- 1).
				mw.log('  -- Подслучай B.1).')
				if _.In(stress_type, {'b', 'c', 'e', 'f', "f'", "b'" }) then  -- gen_pl ending stressed  -- TODO: special vars for that
					_.replace(stems, case, 'ь$', 'е́')
				else
					_.replace(stems, case, 'ь$', 'и')
				end
			elseif _.contains(stem, '[ьй]{consonant}$') then  -- 2).
				mw.log('  -- Подслучай B.2).')
				if data.adj then
					e = stem_type == 'letter-ц' or not _.contains(stress_type, 'b')  -- todo: fix only "b" for srt...
				else
					e = stem_type == 'letter-ц' or _.equals(stress_type, {'a', 'd', "d'"})  -- gen_pl ending unstressed  -- TODO: special vars for that
				end
				if e then
					_.replace(stems, case, '[ьй]({consonant})$', 'е%1')
				else
					_.replace(stems, case, '[ьй]({consonant})$', 'ё%1')
				end
			else  -- 3).
				prev = _.extract(stem, '(.){consonant}$')
				case_3_a = stem_type == 'velar' and _.contains(prev, '[^жшчщц]')  -- 3). а).
				case_3_b = _.contains(prev, '[кгх]')  -- 3). б).
				if case_3_a or case_3_b then
					mw.log('  -- Подслучай B.3). а,б).')
					_.replace(stems, case, '(.)({consonant})$', '%1о%2')
				else  -- 3). в).
					mw.log('  -- Подслучай B.3). в).')
					if stem_type == 'letter-ц' then
						mw.log('  -- stem_type == "letter-ц"')
						_.replace(stems, case, '(.)({consonant})$', '%1е%2')
					else
						if data.adj then
							e = _.contains(stress_type, 'b')  -- todo: fix only "b" for srt...
						else
							e = _.In(stress_type, {'b', 'c', 'e', 'f', "f'", "b'" })  -- gen_pl ending stressed  -- TODO: special vars for that
						end
						if e then
							mw.log('  -- в `' .. case .. '` ударение на окончание')
							if _.contains(prev, '[жшчщ]') then
								mw.log('  -- предыдущая [жшчщ]')
								_.replace(stems, case, '(.)({consonant})$', '%1о́%2')
							else
								mw.log('  -- предыдущая не [жшчщ]')
								_.replace(stems, case, '(.)({consonant})$', '%1ё%2')
							end
						else
							mw.log('    -- ударение на основу в ["' .. case .. '"] ')
							_.replace(stems, case, '(.)({consonant})$', '%1е%2')
						end
					end
				end
			end
			if stem_type == 'soft' and _.endswith(word, 'ня') and stress_type == 'a' and endings['gen_pl'] == 'ь' then
				endings['gen_pl'] = ''  -- вместо `ь` для `2*a`
			end
			if gender == 'm' and data.adj and _.endswith(word, 'ний') and endings['srt_sg'] == 'ь' then
				endings['srt_sg'] = ''  -- вместо `ь` для `2*a`
			end
--			if _.contains(rest_index, 'ё') then
--				if _.contains(stems['gen_pl'], 'ё.*е') then
--					mw.log('% Специальный случай-исправление типа "сёстер" -> "сестёр"')
--					_.replace(stems, 'gen_pl', 'ё(.*)е([^е]*)$', 'е%1ё%2')
--				end
--			end
		end  -- reduced B
	end  -- specific *
end


return export
